from abc import ABC, abstractmethod
from typing import List

from app.data import *
from app.models import *

class CourseService(ABC):
  @abstractmethod
  def get_courses(self) -> List[Course]:
    """
    Returns a list of all courses.
    """
    pass
  
  @abstractmethod
  def check_id(self, id: int, model: str):
    """
    Return model object if id exist, else return None
    """
    pass
  

  def find_last_id(self, model: str):
    """
    Return last model id from model DATA 
    """
    pass
     
  @abstractmethod
  def get_course_by_id(self, course_id) -> Course:
    """
    Returns a course by its id.
    """
    pass

  @abstractmethod
  def create_course(self, course_name) -> Course:
    """
    Creates a new course.
    """
    pass

  @abstractmethod
  def delete_course(self, course_id) -> Course:
    """
    Deletes a course by its id.
    """
    pass
    

  @abstractmethod
  def create_assignment(self, course_id, assignment_name) -> Assessment:
    """
    Creates a new assignment for a course.
    """
    pass

  @abstractmethod
  def enroll_student(self, course_id, student_id) -> Enroll:
    """
    Enrolls a student in a course.
    """
    pass

  @abstractmethod
  def dropout_student(self, course_id, student_id) -> Enroll:
    """
    Drops a student from a course.
    """
    pass


  @abstractmethod
  def submit_assignment(self, course_id, student_id, assignment_id, grade: int) -> Grade:
    """
    Submits an assignment for a student. A grade of an assignment will be an integer between 0 and 100 inclusive.
    """
    pass
    

  @abstractmethod
  def get_assignment_grade_avg(self, course_id, assignment_id) -> int:
    """
    Returns the average grade for an assignment. Floors the result to the nearest integer.
    """
    pass
    

  @abstractmethod
  def get_student_grade_avg(self, course_id, student_id) -> int:
    """
    Returns the average grade for a student in a course. Floors the result to the nearest integer.
    """
    pass
    

  @abstractmethod
  def get_top_five_students(self, course_id) -> List[int]:
    """
    Returns the IDs of the top 5 students in a course based on their average grades of all assignments.
    """
    pass
    
