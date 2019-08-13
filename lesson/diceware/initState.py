from django.templatetags.static import static

from lesson.cards.singleImageCard import SingleImageCard
from lesson.internet.states import ASTATE, INITSTATE
from lesson.lessonState import LessonState
from student.models import Student


class InitState(LessonState):
    card = SingleImageCard("Sicheres Passwort", static('diceware/dice-magician.png'), INITSTATE)

    def state_number(self):
        return INITSTATE

    def previous_state(self, student: Student):
        return None  # Initial state has no previous

    def next_state(self, student: Student) -> int:
        return ASTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student):
        return self.card.post(post)

    @staticmethod
    def name():
        return "Intro"
