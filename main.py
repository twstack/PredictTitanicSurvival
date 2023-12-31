import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the passenger data
passengers = pd.read_csv('passengers.csv')
print(passengers.head())

# Update sex column to numerical
passengers['Sex'] = passengers['Sex'].map({'female': 1, 'male': 0})

# Fill the nan values in the age column
passengers['Age'].fillna(value=passengers['Age'].mean(), inplace=True)

# Create a first class column
passengers['FirstClass'] = passengers['Pclass'].apply(lambda p: 1 if p == 1 else 0)

# Create a second class column
passengers['SecondClass'] = passengers['Pclass'].apply(lambda p: 1 if p == 2 else 0)
print(passengers.head())

# Select the desired features
features = passengers[['Sex', 'Age', 'FirstClass', 'SecondClass']]
survival = passengers['Survived']

# Perform train, test, split
train_features, test_features, train_labels, test_labels = train_test_split(features, survival, test_size=0.2,
                                                                            random_state=42)

# Scale the feature data so it has mean = 0 and standard deviation = 1
scaler = StandardScaler()
train_features = scaler.fit_transform(train_features)
test_features = scaler.transform(test_features)

# Create and train the model
model = LogisticRegression()
model.fit(train_features, train_labels)

# Score the model on the train data
print("Train Score: ", model.score(train_features, train_labels))

# Score the model on the test data
print("Test Score: ", model.score(test_features, test_labels))

# Analyze the coefficients
print(model.coef_)

# Sample passenger features
Jack = np.array([0.0,20.0,0.0,0.0])
Rose = np.array([1.0,17.0,1.0,0.0])
You = np.array([0.0,22.0,1.0,0.0])

# Combine passenger arrays
sample_passengers = np.array([Jack, Rose, You])

# Scale the sample passenger features
sample_passengers = scaler.transform(sample_passengers)

# Make survival predictions
prediction = model.predict(sample_passengers)
print(prediction)

prediction_proba = model.predict_proba(sample_passengers)
print(prediction_proba)

# Visualizing the data

# Correlation matrix
plt.figure(figsize=(10,10))
sns.heatmap(passengers.select_dtypes(include=[np.number]).corr(), annot=True, square=True, cmap='coolwarm')
plt.title('Correlation of Features')
plt.show()


# Age vs. Survival
plt.figure(figsize=(10,6))
sns.violinplot(x='Survived', y='Age', data=passengers)
plt.title('Age vs. Survival')
plt.show()

# Sex vs. Survival
plt.figure(figsize=(10,6))
sns.barplot(x='Sex', y='Survived', data=passengers)
plt.title('Sex vs. Survival')
plt.show()

# Pclass vs. Survival
plt.figure(figsize=(10,6))
sns.barplot(x='Pclass', y='Survived', data=passengers)
plt.title('Passenger Class vs. Survival')
plt.show()