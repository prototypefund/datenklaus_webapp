# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from lesson.lessonUtil import get_lesson
from lesson.states.lessonState import LessonState
from lexicon import lexiconUtils
from student.models import Student
from teacher.constants import RoomStates


def room_status(request):
    if not request.is_ajax():
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return JsonResponse({"redirect": reverse("index")})

    if student.room.state == RoomStates.CLOSED.value:
        return JsonResponse({"redirect": reverse("index")})

    if student.current_room_state != student.room.state:
        return JsonResponse({"redirect": reverse("lesson")})

    return JsonResponse({"redirect": None})


def lesson(request):
    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    # Check if room state has changed
    if student.current_room_state != student.room.state:
        student.current_room_state = student.room.state
        student.save()

    if student.current_room_state == RoomStates.PAUSED.value:
        return render(request, "lesson/pause.html")
    elif student.current_room_state == RoomStates.WAITING.value:
        return render(request, "lesson/waiting.html",
                      context={"sname": student.user_name, "rname": student.room.room_name})
    elif student.current_room_state == RoomStates.CLOSED.value:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)

    if student.is_finished:
        entry = lexiconUtils.get_random_entry()
        context = {"lesson_title": current_lesson.title(),
                   "entry": entry.as_html()}
        return render(request, "lesson/finished.html", context=context)

    if student.is_syncing:
        entry = lexiconUtils.get_random_entry()
        context = {"entry": entry.as_html()}
        return render(request, "lesson/sync.html", context=context)

    current_state = current_lesson.state(student.current_state)

    context = {"lname": student.room.lesson,
               "rname": student.room,
               "is_first": current_state.is_first(),
               "is_last": current_state.is_final()}

    return current_state.render(request, student, context)


def lesson_previous(request):
    # Must NOT a post request
    if request.method == 'POST':
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)
    current_state = current_lesson.state(student.current_state)

    prev_state = current_state.previous_state(student)
    if prev_state is not None:
        student.current_state = prev_state
        student.save()
    return HttpResponseRedirect(reverse("lesson"))


def lesson_next(request):
    # Must be a post request
    if not request.method == 'POST':
        return HttpResponseNotFound()

    try:
        student = Student.objects.get(session=request.session.session_key)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    current_lesson = get_lesson(student.room.lesson)
    current_state = current_lesson.state(student.current_state)

    # Handle post received from current state
    try:
        current_state.post(request.POST, student)
    except LessonState.LessonStateError as e:
        if e.fallback_state is None:
            return HttpResponseNotFound()
        student.current_state = e.fallback_state
        return HttpResponseRedirect(reverse("lesson"))

    if current_state.is_final():
        student.is_finished = True
        student.save()
        return HttpResponseRedirect(reverse("lesson"))

    # Transition to next state
    student.current_state = current_state.next_state(student)
    next_state = current_lesson.state(student.current_state)
    # Check if next state is sync state
    if next_state.is_sync():
        student.is_syncing = True
    else:
        next_state.set_previous_state(student, current_state.state_number())

    student.save()
    return HttpResponseRedirect(reverse("lesson"))
