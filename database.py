# Create the SQLite database engine
ENGINE = create_engine('sqlite:///neuro_lessons.db')
# Create the tables (only runs if the tables don't exist)
Base.metadata.create_all(ENGINE)
# Create a configured "Session" class
Session = sessionmaker(bind=ENGINE)

def add_new_student(name, style, barriers, interests):
    session = Session()
    new_student = Student(
        name=name, 
        preferred_learning_style=style, 
        known_barriers=barriers, 
        interests=interests
    )
    session.add(new_student)
    session.commit()
    session.close()
    
# Function to retrieve a student, save a lesson, etc.