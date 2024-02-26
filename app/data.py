# Define Course instances
from app.models import *

course_OOP = Course(1, "Introduction to Object Oriented Programming")
course_DBS = Course(2, "Introduction to Database Systems")

student_alex = Student(1, "Alex")
student_george = Student(2, "George")

assessment_OOP_assignment1 = Assessment(1, "Class and models", course_OOP)
assessment_OOP_assignment2 = Assessment(2, "Operators", course_OOP)
assessment_DBS_lab1 = Assessment(3, "Create tables in SQL", course_DBS)

enrollment_alex_OOP = Enroll(1, course_OOP, student_alex)
enrollment_alex_DBS = Enroll(2, course_DBS, student_alex)
enrollment_george_DBS = Enroll(3, course_DBS, student_george)

grade_alex_OOP_assignment1 = Grade(1, 85, assessment_OOP_assignment1, student_alex)
grade_alex_OOP_assignment2 = Grade(2, 90, assessment_OOP_assignment2, student_alex)
grade_alex_DBS_lab1 = Grade(3, 80, assessment_DBS_lab1, student_alex)
grade_george_DBS_lab1 = Grade(4, 75, assessment_DBS_lab1, student_george)

COURSES = "courses"
STUDENTS = "students"
ASSESSMENTS = "assessments"
ENROLLMENTS = "enrollments"
GRADES = "grades"

DATA = {
    COURSES: {
        course_OOP,
        course_DBS,
    },
    STUDENTS : {
        student_alex,
        student_george,
    },
    ASSESSMENTS : {
        assessment_OOP_assignment1,
        assessment_OOP_assignment2,
        assessment_DBS_lab1,
    },
    ENROLLMENTS : {
        enrollment_alex_OOP,
        enrollment_alex_DBS,
        enrollment_george_DBS,
    },
    GRADES : {
        grade_alex_OOP_assignment1,
        grade_alex_OOP_assignment2,
        grade_alex_DBS_lab1,
        grade_george_DBS_lab1
    }
},

