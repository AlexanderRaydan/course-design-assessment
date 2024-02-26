class Course():
  def __init__(self, id: int, name: str):
    self.id = id
    self.name = name

  def __str__(self) -> str:
    return f'{self.name}'

class Assessment():
  def __init__(self, id: int, name: str , course: Course):
    self.id = id
    self.name = name
    self.course = course

  def __str__(self) -> str:
    return f'{self.name} course: {self.course}'

class Student():
  def __init__(self, id: int, name: str):
    self.id = id
    self.name = name

  def __str__(self) -> str:
    return f'{self.name}'

class Enroll():
  def __init__(self, id: int, course: Course, student: Student):
    self.id = id
    self.course = course
    self.student = student

  def __str__(self) -> str:
    return f'Student {self.student} enrolled to course: {self.course}'

class Grade():
  def __init__(self, id: int, score: int ,assessment: Assessment , student: Student):
    self.id = id
    self.score = score
    self.assessment = assessment
    self.student = student

  def __str__(self) -> str:
    return f'Student {self.student} have a score of {self.score} in assessment {self.assessment.name}'
    






  