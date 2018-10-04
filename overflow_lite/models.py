import uuid

all_answers = []
all_questions = []


class User(object):
    """This class defines methods that will store the details of a user in a dictionary"""

    def __init__(self):
        self.users = {}
        self.user_token = {}

    def create_user_account(self, user_name, user_password, is_admin=False):
        """This method creates a new user account with a random unique global identifier"""
        user_details = {
                'id': uuid.uuid4(),
                'username': user_name,
                'password': user_password,
                'is_admin': is_admin
        }
        self.users[user_name] = user_details
        return self.users


class Questions(object):
    """This class defines methods that will handle questions
    and store the details of the questions in dictionaries"""

    def __init__(self):
        self.questions = {}

    def post_questions(self, title, description, user_id):
        """This method will add a new question to the question dictionaries"""
        new_question = {'question_id': len(self.questions) + 1,
                        'question_title': title,
                        'question_statement': description,
                        'user_id': user_id}
        self.questions[title] = new_question
        return self.questions

    def delete_questions(self, question_id):
        """This method allows a user to delete a question by supplying the id of the question"""
        if self.questions:
            for question in self.questions.values():
                if question.get('question_id') == question_id:
                    return question

    def fetch_all_questions(self, user_id):
        """This method allows a user to fetch all questions posted by themselves by supplying user id"""
        if self.questions:
            for question in self.questions.values():
                if question['user_id'] == user_id:
                    all_questions.append(question)
                    return all_questions

    def find_question_by_id(self, question_id):
        """This method allows a user to fetch a question that corresponds to the supplied question id"""
        if self.questions:
            for question in self.questions.values():
                if question.get('question_id') == question_id:
                    return question

    def update_question(self, question_id, title, description):
        """This method will allow a user to update a question by supplying the question id, title and description"""
        if self.questions:
            for question in self.questions.values():
                if question.get('question_id') == question_id:
                    question['question_title'] = title
                    question['question_statement'] = description
                    return question


class Answers(object):
    """This class defines methods that handle answers to the questions"""

    def __init__(self):
        self.answers = {}

    def post_answer(self, title, statement, user_id, question_id):
        """This method creates a new answer for a question posted by a user"""
        new_answer = {
            'answer_id': str(uuid.uuid4()),
            'answer_title': title,
            'answer_statement': statement,
            'user_id': user_id,
            'question_id': question_id
        }
        self.answers[id] = new_answer

    def fetch_all_answers(self, question_id):
        """This method gets all the answers for a particular question whose id is supplied as a parameter"""
        for answer in self.answers.values():
            if answer['question_id'] == question_id:
                all_answers.append(question_id)
                return all_questions
