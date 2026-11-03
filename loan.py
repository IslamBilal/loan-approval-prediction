import os
import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER", ""),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DATABASE", "loan_approval"),
)

cursor = None
try:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_applications1 (
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
            loan_status VARCHAR(50) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    print("loan_applications1 table is ready.")
finally:
    if cursor is not None:
        cursor.close()
    connection.close()
