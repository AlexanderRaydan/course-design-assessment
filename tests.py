import pytest
from app.course_service_impl import CourseServiceImpl
from app.data import *

service = CourseServiceImpl()

INVALID_ID = 9999
INVALID_SCORE_UP = 101
INVALID_SCORE_FLOOR = -1

def test_get_courses():
    courses = service.get_courses()
    assert len(courses) == 2

def test_check_id():

    # Valid ID
    student_check = DATA[STUDENTS][0]
    student = service.check_id(DATA[STUDENTS][0].id, STUDENTS)
    assert student.id == student_check.id

    # Invalid ID
    student = service.check_id(INVALID_ID, STUDENTS)
    assert student == None

def test_find_last_id():

    last_id = service.find_last_id(COURSES)
    assert last_id == 2

    last_id = service.find_last_id(ASSESSMENTS)
    assert last_id == 3


def test_get_course_by_id():

    # Valid ID
    course_check = DATA[COURSES][0]
    course = service.get_course_by_id(DATA[COURSES][0].id)
    assert course.id == course_check.id

    # Invalid ID
    course = service.get_course_by_id(INVALID_ID)
    assert course == None


def test_create_and_delete_course():

    # Create
    previous_courses_len = len(service.get_courses())
    course = service.create_course("Software Testing")
    current_courses_len = len(service.get_courses())

    assert previous_courses_len + 1  == current_courses_len
    assert course.name == "Software Testing"

    # Delete course created before
    previous_courses_len = len(service.get_courses())
    service.delete_course(course.id)
    current_courses_len = len(service.get_courses())

    assert previous_courses_len - 1 == current_courses_len

    # Invalid id 
    with pytest.raises(Exception) as e:
        service.delete_course(INVALID_ID)

    assert str(e.value) == "Invalid course ID"

def test_create_assignment():
    course_id = DATA[COURSES][1].id
    previous_assessment_len = len(DATA[ASSESSMENTS])
    new_assessment = service.create_assignment(course_id , "Joins and Views in SQL")
    current_assessment_len = len(DATA[ASSESSMENTS])

    assert previous_assessment_len + 1 == current_assessment_len
    assert new_assessment.course.id == course_id

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.create_assignment(INVALID_ID , "Joins and Views in SQL")

    assert str(e.value) == "Invalid course ID"

    DATA[ASSESSMENTS].remove(new_assessment)


def test_enroll_and_dropout_student():

    # Enroll student
    course_id = DATA[COURSES][0].id
    student_id = DATA[STUDENTS][1].id

    previous_enroll_len = len(DATA[ENROLLMENTS])
    new_enroll = service.enroll_student(course_id , student_id)
    current_enroll_len = len(DATA[ENROLLMENTS])
    
    assert previous_enroll_len + 1  == current_enroll_len
    assert new_enroll.course.id == course_id
    assert new_enroll.student.id == student_id

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.enroll_student(INVALID_ID , student_id)

    assert str(e.value) == "Invalid course ID"

    # Invalid student id 
    with pytest.raises(Exception) as e:
        service.enroll_student(course_id , INVALID_ID)

    assert str(e.value) == "Invalid student ID"

    # Drop student

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.dropout_student(INVALID_ID , student_id)

    assert str(e.value) == "Invalid course ID"

    # Invalid student id 
    with pytest.raises(Exception) as e:
        service.dropout_student(course_id , INVALID_ID)

    assert str(e.value) == "Invalid student ID"

    # Enroll did not found
    with pytest.raises(Exception) as e:
        service.dropout_student(course_id, student_id + 1)

    assert str(e.value) == "Enroll did not found"

    previous_enroll_len = len(DATA[ENROLLMENTS])
    service.dropout_student(new_enroll.course.id , new_enroll.student.id)
    current_enroll_len = len(DATA[ENROLLMENTS])
    
    assert previous_enroll_len - 1 == current_enroll_len


def test_submit_assignment():
    course_id = DATA[COURSES][0].id
    student_id = DATA[STUDENTS][0].id
    assessment_id = DATA[ASSESSMENTS][0].id

    score = 90

    previous_grades_len = len(DATA[GRADES])
    new_grade = service.submit_assignment(course_id , student_id, assessment_id , score)
    current_grades_len = len(DATA[GRADES])

    assert previous_grades_len + 1 == current_grades_len
    assert new_grade.assessment.id == assessment_id
    assert new_grade.student.id == student_id
    assert new_grade.score == score

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.submit_assignment(INVALID_ID, student_id, assessment_id , score)

    assert str(e.value) == "Invalid course ID"

    # Invalid student id 
    with pytest.raises(Exception) as e:
        service.submit_assignment(course_id, INVALID_ID, assessment_id , score)

    assert str(e.value) == "Invalid student ID"

    # Invalid assessment id 
    with pytest.raises(Exception) as e:
        service.submit_assignment(course_id, student_id, INVALID_ID , score)

    assert str(e.value) == "Invalid assessment ID"

    # Invalid score UP 
    with pytest.raises(Exception) as e:
        service.submit_assignment(course_id, student_id, assessment_id , INVALID_SCORE_UP)

    assert str(e.value) == "Invalid score, have to be be from 0 to 100, inclusive"

    # Invalid score FLOOR 
    with pytest.raises(Exception) as e:
        service.submit_assignment(course_id, student_id, assessment_id , INVALID_SCORE_FLOOR)

    assert str(e.value) == "Invalid score, have to be be from 0 to 100, inclusive"

    DATA[GRADES].remove(new_grade)


def test_get_assignment_grade_avg():
    course_id = DATA[COURSES][1].id
    assessment_id = DATA[ASSESSMENTS][2].id

    avg = service.get_assignment_grade_avg(course_id, assessment_id)
    assert avg == 90

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.get_assignment_grade_avg(INVALID_ID, assessment_id)
    assert str(e.value) == "Invalid course ID"


    # Invalid assessment id 
    with pytest.raises(Exception) as e:
        service.get_assignment_grade_avg(course_id , INVALID_ID)

    assert str(e.value) == "Invalid assessment ID"


def test_get_student_grade_avg():
    course_id = DATA[COURSES][0].id
    student_id = DATA[STUDENTS][0].id

    avg = service.get_student_grade_avg(course_id, student_id)
    assert avg == 87

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.get_student_grade_avg(INVALID_ID, student_id)
    assert str(e.value) == "Invalid course ID"

    # Invalid student id 
    with pytest.raises(Exception) as e:
        service.get_student_grade_avg(course_id , INVALID_ID)

    assert str(e.value) == "Invalid student ID"


def test_get_student_grade_avg():
    course_id = DATA[COURSES][1].id

    avg = service.get_top_five_students(course_id)
    assert avg == [2,1,3]

    # Invalid course id 
    with pytest.raises(Exception) as e:
        service.get_top_five_students(INVALID_ID)
    assert str(e.value) == "Invalid course ID"

   






















