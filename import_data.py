import pandas as pd
from sklearn.datasets import load_breast_cancer
from pymongo import MongoClient


# Load the Breast Cancer dataset
breast_cancer = load_breast_cancer()
data = breast_cancer.data

feature_names = breast_cancer.feature_names
print(feature_names)
print(breast_cancer.target_names)
print(breast_cancer.target)
modified_list = [string.replace(" ", "_") for string in feature_names]
# Create a pandas DataFrame from the dataset
df = pd.DataFrame(data, columns=modified_list)
# Add the target column to the DataFrame
df['target'] = breast_cancer.target
uri = "mongodbconnection String"
# Connect to MongoDB
client = MongoClient(uri)
database = client['MLProject']
collection = database["breast_cancer_data"]
# Convert DataFrame to a list of dictionaries
data_to_insert = df.to_dict(orient='records')
# Insert data into MongoDB collection
collection.insert_many(data_to_insert)
# Retrieve all data from the MongoDB collection
cursor = collection.find()

# Convert cursor data to a list of dictionaries
data_list = list(cursor)

# Create a Pandas DataFrame for verification of data
df = pd.DataFrame(data_list)
print(df.head(5))
