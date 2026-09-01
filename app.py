from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load skill model
skill_model = joblib.load("skill_model.pkl")
skill_label_encoder = joblib.load("label_encoder.pkl")

# Load lesson recommendation model
lesson_model = joblib.load("lesson_model.pkl")
lesson_label_encoder = joblib.load("lesson_label_encoder.pkl")

# Lesson names
LESSON_NAMES = {
    1: "Introduction to Perfumery",
    2: "Perfume Raw Materials",
    3: "The Perfume Pyramid",
    4: "Blending Techniques",
    5: "Quality Control & Finishing"
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        features = pd.DataFrame([{
            "lessons_completed": data.get("lessonsCompleted", 0),
            "total_lessons": data.get("totalLessons", 8),
            "lessons_remaining": data.get("totalLessons", 8) - data.get("lessonsCompleted", 0),
            "time_spent_minutes": data.get("timeSpent", 0),
            "quizzes_attempted": data.get("quizzesAttempted", 0),
            "average_score": data.get("averageScore", 0),
            "score_per_lesson": round(data.get("averageScore", 0) / max(data.get("lessonsCompleted", 1), 1), 1),
            "completion_rate": data.get("completionRate", 0),
            "progress": data.get("progress", 0),
            "engagement_score": round((data.get("progress", 0) + data.get("averageScore", 0)) / 2, 1)
        }])
        
        prediction = skill_model.predict(features)
        skill_level = skill_label_encoder.inverse_transform(prediction)[0]
        
        if skill_level == "Beginner":
            recommendation = "Review the basics and practice foundational lessons."
        elif skill_level == "Intermediate":
            recommendation = "Continue building your skills and try advanced lessons."
        else:
            recommendation = "Excellent! Try creating your own recipes and teaching others."
        
        return jsonify({
            "success": True,
            "skillLevel": skill_level,
            "recommendation": recommendation
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/predict-lesson", methods=["POST"])
def predict_lesson():
    try:
        data = request.json
        
        lessons_completed = data.get("lessonsCompleted", 0)
        quiz_score = data.get("averageScore", 0)
        progress = data.get("progress", 0)
        time_spent = data.get("timeSpent", 0)
        
        features = pd.DataFrame([{
            "lessons_completed": lessons_completed,
            "quiz_score": quiz_score,
            "progress": progress,
            "time_spent": time_spent
        }])
        
        prediction = lesson_model.predict(features)
        next_lesson = int(lesson_label_encoder.inverse_transform(prediction)[0])
        
        if next_lesson == lessons_completed and next_lesson < 5:
            if quiz_score < 50:
                recommendation = f"Revisit Lesson {next_lesson} - {LESSON_NAMES.get(next_lesson, 'Lesson ' + str(next_lesson))}"
            else:
                recommendation = f"Continue to Lesson {lessons_completed + 1} - {LESSON_NAMES.get(lessons_completed + 1, 'Lesson ' + str(lessons_completed + 1))}"
        elif next_lesson < lessons_completed:
            recommendation = f"Revisit Lesson {next_lesson} - {LESSON_NAMES.get(next_lesson, 'Lesson ' + str(next_lesson))}"
        elif next_lesson > lessons_completed:
            recommendation = f"Next: Lesson {next_lesson} - {LESSON_NAMES.get(next_lesson, 'Lesson ' + str(next_lesson))}"
        else:
            if lessons_completed >= 5:
                recommendation = "Course Complete! Try another course."
            else:
                recommendation = f"Continue to Lesson {lessons_completed + 1} - {LESSON_NAMES.get(lessons_completed + 1, 'Lesson ' + str(lessons_completed + 1))}"
        
        return jsonify({
            "success": True,
            "nextLesson": next_lesson,
            "recommendation": recommendation,
            "lessonName": LESSON_NAMES.get(next_lesson, "Lesson " + str(next_lesson))
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "AI service is running!"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)