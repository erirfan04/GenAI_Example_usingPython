import pickle

# Save trained model
model = None
pickle.dump(model, open("model.pkl", "wb"))

# Load trained model later
model = pickle.load(open("model.pkl", "rb"))