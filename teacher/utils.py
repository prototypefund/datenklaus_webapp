import http
from enum import Enum

from django.contrib.sessions.models import Session
from django.http import JsonResponse

from student.models import Student
from teacher.constants import LESSON_STATE_WAITING


def get_students_for_room(room_name):
    students = Student.objects.filter(room=room_name)
    student_info = []
    for student in students:
        s = Session.objects.get(session_key=student.session)
        decoded = s.get_decoded()
        lesson_state = decoded.get("lesson_state", LESSON_STATE_WAITING)
        student_info.append({"name": student.user_name,
                             "session": s.session_key,
                             "progress": lesson_state,
                             "expiry": s.expire_date})
    return student_info


def ajax_bad_request(error_msg):
    response = JsonResponse({'error': error_msg})
    response.status_code = http.HTTPStatus.BAD_REQUEST
    return response


class Cmd(Enum):
    PAUS = 0
    STOP = 1
    EVAL = 2
