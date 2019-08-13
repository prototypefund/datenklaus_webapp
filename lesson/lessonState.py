from lesson.models import LessonSateModel
from student.models import Student


class LessonState:
    def set_previous_state(self, student: Student, state: int):
        """
        Stores the preceding state in the database
        :param student: 
        :param state:
        :return:
        """
        s, _ = LessonSateModel.objects.get_or_create(state=self.state_number(),
                                                     student=student,
                                                     room=student.room)
        s.previous_state = state
        s.save()

    def previous_state(self, student: Student):
        """
        Returns the preceding state for the given student
        :param student:
        :return:
        """
        s, _ = LessonSateModel.objects.get_or_create(state=self.state_number(),
                                                     student=student,
                                                     room=student.room)
        return s.previous_state

    def state_number(self):
        """
        :return: This state's number as integer representation
        """
        raise NotImplementedError()

    def next_state(self, student: Student) -> int:
        """
        Returns the next (numerical) state which succeeds this state
        within the lesson. Note, this returns a state based on the
        user's input. Hence this function must be called after parsing
        the associated POST request

        :param student: The student who requested the next state
        :return: Succeeding state
        :raises LessonStateError: If state is missing information from preceding state(s)
        """
        raise NotImplementedError()

    def render(self, request, student: Student, context: {}) -> str:
        """
        Renders (calls djangos render shortcut and returns the result) the given states
        :param context: context for the "lesson.html" template
        :param request: Current request
        :param student: The student who requested the next state
        :return: Whatever django's render method returns #fixme better documentation !
        :raises LessonStateError:
        """
        raise NotImplementedError()

    def post(self, post, student):
        """
        Handles an incoming post request which contains the form data generated by
        the associated card.
        :param post:
        :param student:
        :return:
        :raises InvalidCardError:
        :raises LessonStateError:
        """
        raise NotImplementedError()

    @staticmethod
    def result(room: str, student: Student):
        """
        :param room: Room to get results for
        :param student: Student for which to get results for
        :return: Result(s) for given student and room (Type is defined by the state)
        :raises LessonSateError: If state has not been finished yet
        """
        return None

    @staticmethod
    def result_svg(room: str) -> str:
        """
        Returns the results for the given room as svg string
        :param room: Room to get result
        """
        return None

    @staticmethod
    def name():
        """
        :return: Returns the name of the state
        """
        raise NotImplementedError()

    class LessonStateError(Exception):
        """
        Raised when the state is missing information from a previous
        state.
        :var fallback_state: Stores the state which has not been executed
        by the user and should therefore be returned by the request.
        """

        def __init__(self, fallback_state):
            self.fallback_state = fallback_state
