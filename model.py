# Importing necessary libraries
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the data
data = pd.read_csv('survey_data.csv')
# Dropping the timestamp column because it's not necessary
data = data.drop('Timestamp', axis=1)

# Converting the state to category variable language
data['language'] = data['Preferred state of your partner'].map({
    'Tamil Nadu':'Tamil',
    'Karnataka': 'Kannada',
    'Kerala': 'Malayalam',
    'Telangana': 'Telugu',
}).fillna('Hindi')

data['language'] = np.where(data['language'].isin(['Tamil', 'Kannada', 'Malayalam', 'Telugu']), 
                                      data['language'], 'Hindi')

data = data.drop('Preferred state of your partner', axis=1)

# Replacing null values with mode
mode_value = data['Honesty'].mode()[0].astype(int)
data['Honesty'] = data['Honesty'].fillna(mode_value)


# Dropping all null values
data_cleaned = data.dropna()

# Likability score calculation
columns = ['Financial status of your partner', 'Communication', 'Emotional Intelligence', 
           'Listening Skills', 'Looks', 'Fashion sense', 'Fitness', 'Confidence', 'Sense of Humor', 
           'Kindness', 'Open-mindedness', 'Loyalty','Generosity', 'Selfless', 'Honesty']

data_cleaned['likability_score'] = (data_cleaned[columns].sum(axis=1) / (len(columns) * 5))*100

# One-hot encoding
data_with_dummies = pd.get_dummies(data_cleaned)
data_preprocessed = data_with_dummies.replace({True:1, False:0})

# Selecting x and y
target = data_preprocessed['likability_score']
inputs = data_preprocessed.drop('likability_score', axis=1)

# Splitting the dataset
x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size=0.1, random_state=42)

# Fitting the model
model = LinearRegression()
lr = model.fit(x_train, y_train)

# Export the model as a pickle file
pickle.dump(lr, open('model.pkl', 'wb'))



cols = ['What is your age?', 'Financial status of your partner',
       'Communication', 'Emotional Intelligence', 'Listening Skills', 'Looks',
       'Fashion sense', 'Fitness', 'Confidence', 'Sense of Humor', 'Kindness',
       'Open-mindedness', 'Loyalty', 'Generosity', 'Selfless', 'Honesty',
       'What is your gender?_Female', 'What is your gender?_Male',
       'What is your sexuality?_Others',
       'What is your sexuality?_Straight as an arrow', 'language_Hindi',
       'language_Kannada', 'language_Malayalam', 'language_Tamil',
       'language_Telugu']

df = pd.DataFrame({
    'Features': cols,
    'Coef': model.coef_
})

result = {row['Features']: row['Coef'] for _, row in df.iterrows()}
with open('coefficients.json', 'w') as f:
    json.dump(result, f)

data_cleaned['likability_score'].to_json('likability_score.json', orient='records')

interept_value = model.intercept_

with open('intercept_value.txt', 'w') as txt:
    txt.write(str(interept_value))