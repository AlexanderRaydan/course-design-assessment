from typing import List

from app.course_service import CourseService
from app.data import *
from app.models import *

class CourseServiceImpl(CourseService):
  def get_courses(self) -> List[Course]:
    """
    Returns a list of all courses.
    """
    return DATA[COURSES]
  
  def check_id(self, id: int, model: str):
    """
    Return model object if id exist, else return None
    """
    filtered_model = list(filter(lambda e: e.id == id, DATA[model]))

    if len(filtered_model) != 1:
      return None
    
    return filtered_model[0]
  

  def find_last_id(self, model: str) -> int:
    """
    Return last model id from model DATA 
    """
    last_model_id = max(e.id for e in DATA[model])
    return last_model_id


  def get_course_by_id(self, course_id) -> Course:
    """
    Returns a course by its id.
    """
    return self.check_id(course_id, COURSES)


  def create_course(self, course_name) -> Course:
    """
    Creates a new course.
    """
    last_course_id = self.find_last_id(COURSES)
    new_course = Course(last_course_id + 1, course_name)
    DATA[COURSES].append(new_course)

    return new_course

  def delete_course(self, course_id) -> Course:
    """
    Deletes a course by its id.
    """
    course = self.check_id(course_id , COURSES)

    if course is None:
      raise Exception("Invalid course ID")
    
    DATA[COURSES].remove(course)

    return course
    

  def create_assignment(self, course_id, assignment_name) -> Assessment:
    """
    Creates a new assignment for a course.
    """

    course = self.check_id(course_id , COURSES)
    if course is None:
      raise Exception("Invalid course ID")

    last_assessment_id = self.find_last_id(ASSESSMENTS)
    new_assessment = Assessment(last_assessment_id + 1, assignment_name , course)
    DATA[ASSESSMENTS].append(new_assessment)

    return new_assessment

  def enroll_student(self, course_id, student_id) -> Enroll:
    """
    Enrolls a student in a course.
    """

    course = self.check_id(course_id , COURSES)
    student = self.check_id(student_id , STUDENTS)

    if course is None:
      raise Exception("Invalid course ID")
    
    if student is None:
      raise Exception("Invalid student ID")

    last_enroll_id = self.find_last_id(ENROLLMENTS)
    new_enroll = Enroll(last_enroll_id + 1, course , student)
    DATA[ENROLLMENTS].append(new_enroll)

    return new_enroll

  def dropout_student(self, course_id, student_id) -> Enroll:
    """
    Drops a student from a course.
    """

    course = self.check_id(course_id , COURSES)
    student = self.check_id(student_id , STUDENTS)

    if course is None:
      raise Exception("Invalid course ID")
    
    if student is None:
      raise Exception("Invalid student ID")
    
    enroll = list(filter(lambda e : e.course.id == course_id and e.student.id == student_id, DATA[ENROLLMENTS]))

    if len(enroll) != 1:
      raise Exception("Enroll did not found")
    
    DATA[ENROLLMENTS].remove(enroll[0])

    return enroll[0]


  def submit_assignment(self, course_id, student_id, assignment_id, grade: int) -> Grade:
    """
    Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
    """

    if grade < 0 or grade > 100:
      raise Exception("Invalid score, have to be be from 0 to 100, inclusive")


    course = self.check_id(course_id , COURSES)
    student = self.check_id(student_id , STUDENTS)
    assessment = self.check_id(assignment_id , ASSESSMENTS)

    if course is None:
      raise Exception("Invalid course ID")
    
    if student is None:
      raise Exception("Invalid student ID")
    
    if assessment is None:
      raise Exception("Invalid assessment ID")
    
    # Check is the student is enrolled in the course
    enroll = list(filter(lambda e : e.course.id == course_id and e.student.id == student_id, DATA[ENROLLMENTS]))
    if len(enroll) == 0:
      raise Exception(f"The student {student} is not enrolled to the course {course}")
    
    # check if this course contain this assessment
    course_assessments = list(filter(lambda assessment: assessment.course.id == course_id, DATA[ASSESSMENTS]))
    filtered_assessment = list(filter(lambda assessment: assessment.id == assignment_id, course_assessments))
    
    if len(filtered_assessment) == 0:
      raise Exception("this course does not contain that assessment")

    last_grade_id = self.find_last_id(GRADES)
    new_grade = Grade(last_grade_id + 1, grade, assessment, student)
    DATA[GRADES].append(new_grade)

    return new_grade
    

  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
    """
    Returns the average grade for an assignment. Floors the result to the nearest integer.
    """

    course = self.check_id(course_id , COURSES)
    assessment = self.check_id(assignment_id , ASSESSMENTS)

    if course is None:
      raise Exception("Invalid course ID")
    
    if assessment is None:
      raise Exception("Invalid assessment ID")
    
    filtered_grades = list(filter(
      lambda grade: grade.assessment.id == assignment_id and 
      grade.assessment.course.id == course_id, 
    DATA[GRADES]))
    
    avg = 0

    if len(filtered_grades) == 0:
      return avg
    
    for grades in filtered_grades:
      avg = avg + grades.score

    return avg // 2
    

  def get_student_grade_avg(self, course_id, student_id) -> int:
    """
    Returns the average grade for a student in a course. Floors the result to the nearest integer.
    """

    course = self.check_id(course_id , COURSES)
    student = self.check_id(student_id , STUDENTS)

    if course is None:
      raise Exception("Invalid course ID")
    
    if student is None:
      raise Exception("Invalid student ID")
    
    filtered_grades = list(filter(
      lambda grade: grade.student.id == student_id and 
      grade.assessment.course.id == course_id, 
    DATA[GRADES]))

    avg = 0

    if len(filtered_grades) == 0:
      return avg
    
    for grades in filtered_grades:
      avg = avg + grades.score

    return avg // 2
    

  def get_top_five_students(self, course_id) -> List[int]:
    """
    Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
    """
    all_grades = []

    for student in DATA[STUDENTS]:
      avg = self.get_student_grade_avg(course_id, student.id)

      obj = {
        'id' : student.id,
        'gradeAvg' : avg,
      }

      all_grades.append(obj)

    sorted_grades = sorted(all_grades, key=lambda x: x['gradeAvg'], reverse=True)

    if len(sorted_grades) >= 5:
      first_five_ids = [obj['id'] for obj in sorted_grades[:5]]
    else :
      first_five_ids = [obj['id'] for obj in sorted_grades]

    return first_five_ids
