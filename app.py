from flask import Flask, request, render_template
import os
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline
import mysql.connector
from mysql.connector import Error

# Initialize the Flask application
application = Flask(__name__)
app = application

# Function to create a connection to MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", ""),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "loan_approval")
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Route for the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# Route for handling predictions
@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        # Collect data from the form
        data = CustomData(
            no_of_dependents=int(request.form.get('no_of_dependents')),
            income_annum=float(request.form.get('income_annum')),
            loan_amount=float(request.form.get('loan_amount')),
            loan_term=float(request.form.get('loan_term')),
            cibil_score=float(request.form.get('cibil_score')),
            residential_assets_value=float(request.form.get('residential_assets_value')),
            commercial_assets_value=float(request.form.get('commercial_assets_value')),
            luxury_assets_value=float(request.form.get('luxury_assets_value')),
            bank_asset_value=float(request.form.get('bank_asset_value')),
            education=request.form.get('education'),
            self_employed=request.form.get('self_employed')
        )
        
        # Convert the collected data into a DataFrame
        final_new_data = data.get_data_as_dataframe()
        
        # Make a prediction using the prediction pipeline
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)
        
        # Map prediction result to human-readable format
        # LabelEncoder maps " Approved" to 0 and " Rejected" to 1 in the current dataset.
        if int(pred[0]) == 0:
            result_label = "Approved"
        else:
            result_label = "Rejected"
        
        # Insert the data into MySQL database
        connection = create_connection()
        if connection is not None:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO loan_applications1 (
                no_of_dependents, income_annum, loan_amount, loan_term, cibil_score, 
                residential_assets_value, commercial_assets_value, luxury_assets_value, 
                bank_asset_value, education, self_employed, loan_status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data.no_of_dependents, data.income_annum, data.loan_amount, 
                data.loan_term, data.cibil_score, data.residential_assets_value, 
                data.commercial_assets_value, data.luxury_assets_value, 
                data.bank_asset_value, data.education, data.self_employed, result_label
            ))
            connection.commit()
            cursor.close()
            connection.close()
        
        return render_template('results.html', final_result=result_label)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=int(os.getenv('PORT', '5000')), debug=False)
