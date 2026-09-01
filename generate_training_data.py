import pandas as pd
import random
from datetime import datetime, timedelta

# =====================================================
# CONFIGURATION
# =====================================================

NUM_STUDENTS = 100
NUM_COURSES = 5
LESSONS_PER_COURSE = 8
QUIZZES_PER_COURSE = 4

# Course categories
COURSES = [
    {"id": 1, "title": "Cream Making", "difficulty": "Beginner"},
    {"id": 2, "title": "Soap Making", "difficulty": "Beginner"},
    {"id": 3, "title": "Perfume Making", "difficulty": "Intermediate"},
    {"id": 4, "title": "Baking", "difficulty": "Intermediate"},
    {"id": 5, "title": "Chemical Making", "difficulty": "Advanced"},
]

# Sample first names and last names
FIRST_NAMES = [
    "Ali", "Ahmed", "Fatima", "Zainab", "Amina", "Muhammad", "Ibrahim",
    "Khadija", "Omar", "Sara", "Hassan", "Hussein", "Rashid", "Nura",
    "Sani", "Bala", "Musa", "Abdullahi", "Maryam", "Hauwa", "Aisha",
    "Zara", "Nadia", "Layla", "Samira", "Khalid", "Yusuf", "Idris"
]

LAST_NAMES = [
    "Mu'az", "Bello", "Suleiman", "Abdullahi", "Ahmad", "Hassan", "Adam",
    "Aliyu", "Khalifa", "Muhammad", "Baba", "Garba", "Shehu", "Jibril",
    "Uthman", "Khalil", "Nasir", "Faruq", "Hadi", "Zakariyya"
]

def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_student(index):
    """Generate a realistic student profile."""
    name = get_random_name()
    email = f"{name.lower().replace(' ', '.')}@email.com"
    return {
        "student_id": f"STU{str(index+1).zfill(4)}",
        "name": name,
        "email": email,
        "joined": datetime.now() - timedelta(days=random.randint(1, 90))
    }

def generate_enrollment_data(student, course):
    """Generate realistic learning data for a student in a course."""
    
    enrolled_date = datetime.now() - timedelta(days=random.randint(1, 60))
    
    max_lessons = LESSONS_PER_COURSE
    lessons_completed = random.randint(0, max_lessons)
    
    base_time = lessons_completed * random.randint(5, 15)
    time_spent = max(10, base_time + random.randint(-10, 30))
    
    quizzes_attempted = min(
        random.randint(0, lessons_completed // 2 + 1),
        QUIZZES_PER_COURSE
    )
    
    if quizzes_attempted > 0:
        base_score = 30 + (lessons_completed / max_lessons) * 50
        quiz_scores = []
        for _ in range(quizzes_attempted):
            score = max(0, min(100, base_score + random.randint(-20, 20)))
            quiz_scores.append(score)
        average_score = round(sum(quiz_scores) / len(quiz_scores))
    else:
        average_score = 0
    
    completion_rate = min(100, max(0, (lessons_completed / max_lessons) * 100 + random.randint(-10, 10)))
    progress = completion_rate
    
    if average_score >= 80 and lessons_completed >= max_lessons * 0.7:
        skill_level = "Advanced"
    elif average_score >= 50 and lessons_completed >= max_lessons * 0.4:
        skill_level = "Intermediate"
    else:
        skill_level = "Beginner"
    
    completed = progress >= 90 and average_score >= 60
    
    return {
        "course_id": course["id"],
        "course_title": course["title"],
        "student_id": student["student_id"],
        "student_name": student["name"],
        "enrolled_date": enrolled_date,
        "lessons_completed": lessons_completed,
        "total_lessons": max_lessons,
        "time_spent_minutes": time_spent,
        "quizzes_attempted": quizzes_attempted,
        "average_score": average_score,
        "completion_rate": round(completion_rate),
        "progress": round(progress),
        "skill_level": skill_level,
        "completed": completed,
        "difficulty": course["difficulty"]
    }

# =====================================================
# GENERATE STUDENTS
# =====================================================

print(f"Generating {NUM_STUDENTS} students...")
students = [generate_student(i) for i in range(NUM_STUDENTS)]

# =====================================================
# GENERATE ENROLLMENTS
# =====================================================

print(f"Generating enrollments...")
all_enrollments = []

for student in students:
    num_courses = random.randint(2, min(4, len(COURSES)))
    enrolled_courses = random.sample(COURSES, num_courses)
    
    for course in enrolled_courses:
        enrollment = generate_enrollment_data(student, course)
        all_enrollments.append(enrollment)

# =====================================================
# EXPORT TO CSV
# =====================================================

df = pd.DataFrame(all_enrollments)

df["lessons_remaining"] = df["total_lessons"] - df["lessons_completed"]
df["score_per_lesson"] = df.apply(
    lambda row: round(row["average_score"] / max(row["lessons_completed"], 1), 1),
    axis=1
)
df["engagement_score"] = df.apply(
    lambda row: round((row["progress"] + row["average_score"]) / 2, 1),
    axis=1
)

columns = [
    "student_id", "student_name", "course_id", "course_title", "difficulty",
    "lessons_completed", "total_lessons", "lessons_remaining",
    "time_spent_minutes", "quizzes_attempted", "average_score",
    "score_per_lesson", "completion_rate", "progress", "engagement_score",
    "skill_level", "completed", "enrolled_date"
]
df = df[columns]

# Save to CSV
output_file = "skillcraft_training_data.csv"
df.to_csv(output_file, index=False)

# =====================================================
# SUMMARY
# =====================================================

print("\n" + "="*50)
print("✅ TRAINING DATA GENERATED SUCCESSFULLY")
print("="*50)
print(f"📊 Total students: {NUM_STUDENTS}")
print(f"📊 Total enrollments: {len(all_enrollments)}")
print(f"📊 Average enrollments per student: {len(all_enrollments)/NUM_STUDENTS:.1f}")
print(f"📊 Skill level distribution:")
for level in ["Beginner", "Intermediate", "Advanced"]:
    count = df[df["skill_level"] == level].shape[0]
    print(f"   - {level}: {count} ({count/len(all_enrollments)*100:.1f}%)")
print(f"\n📁 File saved: {output_file}")
print("\n✅ Ready for AI training!")

print("\n📋 Sample data (first 5 rows):")
print(df.head().to_string())