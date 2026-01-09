import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Paths to the preprocessor and model files
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            model_path = os.path.join('artifacts', 'model.pkl')

            # Load the preprocessor and model
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            # Transform the features using the preprocessor
            data_scaled = preprocessor.transform(features)

            # Make predictions using the model
            predictions = model.predict(data_scaled)
            return predictions

        except Exception as e:
            logging.info("Exception occurred in the prediction pipeline")
            raise CustomException(e, sys)

class CustomData:
    def __init__(self, no_of_dependents, income_annum, loan_amount, loan_term,
                 cibil_score, residential_assets_value, commercial_assets_value,
                 luxury_assets_value, bank_asset_value, education, self_employed):
        self.no_of_dependents = no_of_dependents
        self.income_annum = income_annum
        self.loan_amount = loan_amount
        self.loan_term = loan_term
        self.cibil_score = cibil_score
        self.residential_assets_value = residential_assets_value
        self.commercial_assets_value = commercial_assets_value
        self.luxury_assets_value = luxury_assets_value
        self.bank_asset_value = bank_asset_value
        self.education = education
        self.self_employed = self_employed

    def get_data_as_dataframe(self):
        try:
            # Creating a dictionary from the input features
            custom_data_input_dict = {
                'no_of_dependents': [self.no_of_dependents],
                'income_annum': [self.income_annum],
                'loan_amount': [self.loan_amount],
                'loan_term': [self.loan_term],
                'cibil_score': [self.cibil_score],
                'residential_assets_value': [self.residential_assets_value],
                'commercial_assets_value': [self.commercial_assets_value],
                'luxury_assets_value': [self.luxury_assets_value],
                'bank_asset_value': [self.bank_asset_value],
                'education': [self.education],
                'self_employed': [self.self_employed]
            }

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception occurred in data preparation')
            raise CustomException(e, sys)