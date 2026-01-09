import mysql.connector
mydb = mysql.connector.connect(
    host= 'localhost',
    user ='',
    password= ''
)
mycursor=mydb.cursor()
#mycursor.execute('create database loan_approval')
mycursor.execute('use loan_approval')
mycursor.execute('''
CREATE TABLE loan_applications1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_of_dependents INT NOT NULL,
    income_annum FLOAT NOT NULL,
    loan_amount FLOAT NOT NULL,
    loan_term FLOAT NOT NULL,
    cibil_score FLOAT NOT NULL,
    residential_assets_value FLOAT NOT NULL,
    commercial_assets_value FLOAT NOT NULL,
    luxury_assets_value FLOAT NOT NULL,
    bank_asset_value FLOAT NOT NULL,
    education VARCHAR(50) NOT NULL,
    self_employed VARCHAR(50) NOT NULL,
    loan_status VARCHAR(50) NOT NULL,  -- Add loan_status column
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
