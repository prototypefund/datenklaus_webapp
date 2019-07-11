from lesson.cards.defaultCard import DefaultCard
from lesson.internet.states import ASTATE, INITSTATE
from lesson.lessonState import LessonState
from student.models import Student


class InitState(LessonState):
    card = DefaultCard("Willkommen",
                       "Heute lernen wir etwas über das Internet",
                       "Das Internet ist sehr toll", INITSTATE)

    def next_state(self, student: Student) -> int:
        return ASTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def handle_post(self, post, student):
        return self.card.handle_post(post, student)

    def get_results(self, room, student=None):
        pass  # FIXME: Maybe add a check to see whether this state has already been executed by the student once
