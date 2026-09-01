import pandas as pd
import random
import json

# =====================================================
# CONFIGURATION
# =====================================================

NUM_RECORDS = 500

# Sample lessons for each course
LESSONS = {
    1: {"title": "Introduction to Perfumery", "order": 1, "difficulty": "easy"},
    2: {"title": "Perfume Raw Materials", "order": 2, "difficulty": "easy"},
    3: {"title": "The Perfume Pyramid", "order": 3, "difficulty": "medium"},
    4: {"title": "Blending Techniques", "order": 4, "difficulty": "medium"},
    5: {"title": "Quality Control & Finishing", "order": 5, "difficulty": "hard"},
}

def get_next_lesson_recommendation(score, completed, progress, time_spent):
    """
    Determine which lesson to recommend based on student performance.
    """
    # If struggling with quiz scores
    if score < 50:
        if completed < 2:
            return 1  # Revisit Lesson 1
        elif completed < 4:
            return max(1, completed - 1)  # Go back one lesson
        else:
            return completed - 1  # Go back to previous lesson
    
    # If good progress but not advanced
    elif score < 80:
        if completed < 3:
            return completed + 1  # Next lesson
        elif completed < 5:
            return completed + 1  # Next lesson
        else:
            return 5  # Last lesson
    
    # If excelling
    else:
        if completed < 3:
            return completed + 2  # Skip ahead
        elif completed < 5:
            return completed + 1  # Next lesson
        else:
            return 5  # Last lesson

# Generate dataset
data = []

for _ in range(NUM_RECORDS):
    # Generate random student data
    lessons_completed = random.randint(0, 5)
    quiz_score = random.randint(0, 100)
    progress = min(100, int((lessons_completed / 5) * 100 + random.randint(-10, 10)))
    time_spent = random.randint(10, 300)
    
    # Determine skill level
    if quiz_score < 50:
        skill_level = "Beginner"
    elif quiz_score < 80:
        skill_level = "Intermediate"
    else:
        skill_level = "Advanced"
    
    # Get recommendation
    next_lesson = get_next_lesson_recommendation(quiz_score, lessons_completed, progress, time_spent)
    
    # Generate recommendation message
    if next_lesson == lessons_completed and next_lesson < 5:
        if quiz_score < 50:
            recommendation = f"Revisit Lesson {next_lesson} - {LESSONS[next_lesson]['title']}"
        else:
            recommendation = f"Continue to Lesson {lessons_completed + 1} - {LESSONS[lessons_completed + 1]['title']}"
    elif next_lesson < lessons_completed:
        recommendation = f"Revisit Lesson {next_lesson} - {LESSONS[next_lesson]['title']}"
    elif next_lesson > lessons_completed:
        recommendation = f"Next: Lesson {next_lesson} - {LESSONS[next_lesson]['title']}"
    else:
        if lessons_completed >= 5:
            recommendation = "Course Complete! Try another course."
        else:
            recommendation = f"Continue to Lesson {lessons_completed + 1} - {LESSONS[lessons_completed + 1]['title']}"
    
    data.append({
        "lessons_completed": lessons_completed,
        "quiz_score": quiz_score,
        "progress": progress,
        "time_spent": time_spent,
        "skill_level": skill_level,
        "next_lesson": next_lesson,
        "recommendation": recommendation
    })

df = pd.DataFrame(data)
df.to_csv("lesson_recommendation_data.csv", index=False)

print("✅ Lesson recommendation dataset generated!")
print(f"📊 Total records: {len(df)}")
print("\n📋 Sample data:")
print(df.head().to_string())