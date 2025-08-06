import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
data = pd.read_csv('diet_data.csv')
print("✅ Loaded diet_data.csv")
print("🧾 Columns:", data.columns)

# Create a 'Goal' column based on Calories
def assign_goal(row):
    if row['Calories'] > 300:
        return 'WeightGain'
    elif row['Calories'] < 200:
        return 'WeightLoss'
    else:
        return 'Maintenance'

# Apply the function to create the 'Goal' column
data['Goal'] = data.apply(assign_goal, axis=1)
print("✅ 'Goal' column added based on Calories")

# Separate features and label
X = data.drop(['Food_items', 'Goal'], axis=1)  # Drop 'Food_items' and 'Goal'
y = data['Goal']

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✅ Model trained")

# Save the model
joblib.dump(model, 'diet_model.pkl')
print("✅ Model saved as diet_model.pkl")
