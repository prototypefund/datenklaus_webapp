from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render

from student.models import Student
from teacher.models import Room
from .forms import JoinRoomForm


def index(request):
    if request.is_ajax():
        rooms = Room.objects.all()
        room_names = []
        for r in rooms:
            room_names.append(r.room_name)
        return JsonResponse({'rooms': room_names})
    form = JoinRoomForm()
    context = {'form': form}
    return render(request, 'student/index.html', context)


def join_room(request):
    form = JoinRoomForm(request.POST)
    if not form.is_valid():
        raise KeyError()  # TODO FIX ME

    # Make sure we only have one existing client per session
    for client in Student.objects.filter(session=request.session.session_key):
        client.delete()

    Student.objects.get_or_create(
        user_name=form.cleaned_data['username'],
        room=form.cleaned_data['room'],
        session=Session.objects.get(session_key=request.session.session_key),
    )

    context = {'sname': form.cleaned_data['username'], 'rname': form.cleaned_data['room']}
    return render(request, 'student/join_room.html', context)


def leave_room(request):
    for s in Student.objects.filter(session=request.session.session_key):
        s.delete()

    return index(request)

# def poll(request, question_id):
#     q = Question.objects.get(id=question_id)
#     context = {'question': q, 'choices_list': q.choice_set.all()}
#     return render(request, 'student/question_view.html', context)
#
#
# def poll_results(request, question_id, illegal_vote=False):
#     q = Question.objects.get(id=question_id)
#     choice_labels = []
#     choice_votes = []
#     for c in q.choice_set.all():
#         choice_labels.append(c.choice_text)
#         choice_votes.append(c.votes)
#
#     context = {'question': q, 'choice_labels': json.dumps(choice_labels), 'choice_votes': choice_votes,
#                'illegal_vote': illegal_vote}
#     return render(request, 'student/poll_results.html', context)
#
#
# def poll_vote(request, question_id, choice_id):
#     has_voted = request.session.get('has_voted', default={})
#
#     if has_voted.get(str(question_id), False):
#         return poll_results(request, question_id, illegal_vote=True)
#
#     has_voted[str(question_id)] = True
#     request.session['has_voted'] = has_voted
#
#     request.session.modified = True
#
#     choice = Choice.objects.get(id=choice_id)
#     choice.votes += 1
#     choice.save()
#
#     return poll_results(request, question_id)
