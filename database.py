import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Student, Lesson

# 1. Database Configuration
# The database file will be named 'neuro_lessons.db' in the same directory.
DATABASE_URL = "sqlite:///neuro_lessons.db"
ENGINE = create_engine(DATABASE_URL)

# 2. Session Management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

def create_db_and_tables():
    """Creates the database and all tables defined in models.py."""
    print("Creating database and tables...")
    Base.metadata.create_all(bind=ENGINE)
    print("Done.")

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD Operations ---

def add_student(db, name, style, barriers, interests):
    """Adds a new student profile to the database."""
    new_student = Student(
        name=name,
        preferred_learning_style=style,
        known_barriers=barriers,
        interests=interests
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def get_all_students(db):
    """Retrieves a list of all students."""
    return db.query(Student).all()

def save_lesson(db, student_id, topic, content):
    """Saves a newly generated lesson to the database."""
    new_lesson = Lesson(
        student_id=student_id,
        topic=topic,
        content=content,
        date_generated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

# Run this once to initialize the DB file
if __name__ == "__main__":
    create_db_and_tables()
    # Example of how to use the functions
    db = next(get_db())
    if not get_all_students(db):
        print("Adding sample students...")
        add_student(db, "Liam (Dyslexia)", "Visual", "Reading Speed, Visual tracking", "Space, Robotics")
        add_student(db, "Chloe (ADHD)", "Kinesthetic", "Focus, Sitting still, Multi-step tasks", "Animals, Games, Art")
        print("Sample students added.")
    db.close()