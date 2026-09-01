import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load data
df = pd.read_csv("lesson_recommendation_data.csv")

# Prepare features
features = [
    "lessons_completed",
    "quiz_score",
    "progress",
    "time_spent"
]

X = df[features]
y = df["next_lesson"]

# Encode target
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"📊 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and encoder
joblib.dump(model, "lesson_model.pkl")
joblib.dump(label_encoder, "lesson_label_encoder.pkl")

print("✅ Lesson recommendation model saved!")