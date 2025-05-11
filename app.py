import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('combined_2021_tomato_data.csv')

# Preview the first few rows of the dataset
print("Data preview:")
print(data.head())

# Check column names to confirm the columns
print("Columns in the data:", data.columns)

# Convert 'Market Arrival Date' to datetime
data['Market Arrival Date'] = pd.to_datetime(data['Market Arrival Date'])

# Fill missing values in 'Market' column with 'Unknown' (or any appropriate strategy)
data['Market'] = data['Market'].fillna('Unknown')

# You can handle missing values for numerical columns as well if needed, for example:
# data['Minimum Price(Rs./Quintal)'].fillna(data['Minimum Price(Rs./Quintal)'].mean(), inplace=True)
# data['Maximum Price(Rs./Quintal)'].fillna(data['Maximum Price(Rs./Quintal)'].mean(), inplace=True)
# data['Modal Price(Rs./Quintal)'].fillna(data['Modal Price(Rs./Quintal)'].mean(), inplace=True)

# Selecting the relevant features for prediction
X = data[['Market', 'Market Arrival Date', 'Variety', 'Minimum Price(Rs./Quintal)', 'Maximum Price(Rs./Quintal)']]

# Convert categorical variables (like 'Market' and 'Variety') into numerical values using encoding
X = pd.get_dummies(X, drop_first=True)

# Target variable: Modal Price
y = data['Modal Price(Rs./Quintal)']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a linear regression model
model = LinearRegression()

# Fitting the model to the training data
model.fit(X_train, y_train)

# Making predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
rmse = mse**0.5
print(f"Root Mean Squared Error: {rmse}")

# Plotting the actual vs predicted values
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=y_pred)
plt.xlabel("Actual Modal Price")
plt.ylabel("Predicted Modal Price")
plt.title("Actual vs Predicted Modal Price")
plt.show()

# To see feature importance (coefficients of the linear regression model)
print("Model Coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef}")
