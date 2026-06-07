import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Simple dataset: hours studied → marks
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([40, 50, 60, 70, 80])

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")