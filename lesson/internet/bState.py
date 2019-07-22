from lesson.cards.barChartCard import BarChartCard
from lesson.internet.aState import AState
from lesson.internet.states import CSTATE, BSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    def get_state_number(self):
        return BSTATE

    card = BarChartCard(BSTATE,
                        list(map(lambda i: str(i), range(1, 6))),
                        title="So schätzt ihr euch ein:")

    def next_state(self, student: Student) -> int:
        return CSTATE

    def render(self, request, student: Student, context) -> str:
        results = AState().get_results(student.room)

        return self.card.render(request, context, dataset=results['knowledge'])

    def handle_post(self, post, student: Student):
        return None

    @staticmethod
    def get_name():
        return "Selbsteinschätzung: Ergebnis"
