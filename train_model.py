import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("skillcraft_training_data.csv")
print("📊 Data loaded successfully!")
print(f"📊 Total records: {len(df)}")
print(f"📊 Columns: {df.columns.tolist()}\n")

# =====================================================
# PREPARE FEATURES
# =====================================================

# Features for training
feature_columns = [
    "lessons_completed",
    "total_lessons",
    "lessons_remaining",
    "time_spent_minutes",
    "quizzes_attempted",
    "average_score",
    "score_per_lesson",
    "completion_rate",
    "progress",
    "engagement_score"
]

X = df[feature_columns]
y = df["skill_level"]  # Target: Beginner, Intermediate, Advanced

print(f"📊 Features: {X.shape[1]} columns")
print(f"📊 Target: {y.nunique()} classes ({y.unique().tolist()})\n")

# =====================================================
# ENCODE TARGET LABELS
# =====================================================

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save label encoder for later use
joblib.dump(label_encoder, "label_encoder.pkl")
print("✅ Label encoder saved!")

# =====================================================
# SPLIT DATA
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"📊 Training set: {len(X_train)} records")
print(f"📊 Test set: {len(X_test)} records\n")

# =====================================================
# TRAIN MODEL
# =====================================================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

print("🔄 Training model...")
model.fit(X_train, y_train)
print("✅ Model trained!\n")

# =====================================================
# EVALUATE MODEL
# =====================================================

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"📊 Accuracy: {accuracy * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

feature_importance = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print("\n📊 Feature Importance:")
print(feature_importance.to_string(index=False))

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(model, "skill_model.pkl")
print("\n✅ Model saved as 'skill_model.pkl'!")

# =====================================================
# TEST PREDICTION
# =====================================================

print("\n" + "="*50)
print("🔮 TEST PREDICTION")
print("="*50)

# Example student data
test_student = pd.DataFrame([{
    "lessons_completed": 6,
    "total_lessons": 8,
    "lessons_remaining": 2,
    "time_spent_minutes": 120,
    "quizzes_attempted": 4,
    "average_score": 75,
    "score_per_lesson": 12.5,
    "completion_rate": 85,
    "progress": 85,
    "engagement_score": 80
}])

prediction = model.predict(test_student)
predicted_label = label_encoder.inverse_transform(prediction)[0]

print("📊 Input data:")
print(test_student.to_string(index=False))
print(f"\n📊 Predicted Skill Level: {predicted_label}")