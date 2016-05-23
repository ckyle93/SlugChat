# Helper functions for interacting with login


class QuizObj(object):

    def __init__(self):
        self.id = -1
        self.question_text = 'N/A'
        self.choices = []


def logged_in(request):
    if 'email_address' in request.session:
        return True
    else:
        return False
