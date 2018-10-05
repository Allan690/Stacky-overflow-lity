from flask import request, jsonify, Blueprint
from .models import Questions, Answers
from .user_authentication import login_token_required

quiz_obj = Questions()
ans_object = Answers()
quiz = Blueprint('v1_questions', __name__)


@quiz.route('/questions', methods=['POST'])
@login_token_required
def create_question(current_user):
    """This method allows a user who is logged in to create a question"""
    user_input = request.get_json()
    if not user_input or not user_input['question_title']:
        return jsonify({"Message": "The title of the question is required!"}), 400

    if user_input['question_title'] in quiz_obj.questions:
        return jsonify({"Message": "The title already exists!"}), 400
    user_id = current_user['username']
    quiz_obj.post_questions(user_input['question_title'],
                            user_input['question_statement'],
                            user_input[user_id])
    return jsonify({"Message": "The question was posted successfully"}), 201


@quiz.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Return a question with the id entered as question_id"""
    response = quiz_obj.find_question_by_id(question_id)
    if response:
        return jsonify({"Question Profile": response}), 200
    return jsonify({"Message": "Question was not found"}), 404


@quiz.route('/questions/<int:question_id>', methods=['PUT'])
@login_token_required
def get_update_question(current_user, question_id):
    """
    This method allows a user to login and to update a question
    """
    data = request.get_json()
    new_title = data['question_title']
    new_description = data['question_statement']
    question = quiz_obj.find_question_by_id(question_id)
    if question:
        if current_user['username'] == question['user_id']:
            response = quiz_obj.update_question(question_id, new_title, new_description)
            if response:
                if new_title not in quiz_obj.questions:
                    return jsonify({'Message': 'Question has been updated'}), 200
                return jsonify({'Message':
                                'That question title already exists'}), 400
        return jsonify({"Message":
                        "Sorry:You can only update your own" +
                        "question!!"}), 401
    return jsonify({'Message': 'Question not found'}), 404


@quiz.route('/questions', methods=['GET'])
def get_all_questions():
    return jsonify({"questions": quiz_obj.questions}), 200


@quiz.route('/questions/<int:questions_id>', methods=['DELETE'])
@login_token_required
def delete_question(current_user, question_id):
    """This method removes a question based on the id supplied"""
    question = quiz_obj.find_question_by_id(question_id)
    if question:
        if current_user['username'] == question['user_id']:
            del quiz_obj.questions[question['question_title']]
            return jsonify({"Message": "Question was deleted successfully"}), 200
        return jsonify({"Message":
                        "Sorry, You can only delete" +
                        "your own question!"}), 401
    return jsonify({"Message": "Question was not found"}), 404


@quiz.route('/questions/<int:question_id>/answers', methods=['POST'])
@login_token_required
def create_answer(current_user, question_id):
    """This method allows a user to create an answer to a question based on supplied question id after they
    have logged in"""
    input_data = request.get_json()
    if not input_data or not input_data['answer_title']:
        return jsonify({"Message": "The title of the answer is required"}), 400

    question = quiz_obj.find_question_by_id(question_id)
    if question:
        user_id = current_user['username']
        ans_object.post_answer(input_data['answer_title'],
                               input_data['answer_statement'],
                               user_id,
                               question_id)
        return jsonify({"Message": "Answer to the question has been successfully posted"}), 201

    return jsonify({"Message": "Question not found"}), 401


@quiz.route('/questions/<int:question_id>/answers', methods=['GET'])
@login_token_required
def get_question_answers(current_user, question_id):
    """This method will list all the answers to a question based on the supplied question id"""
    question = quiz_obj.find_question_by_id(question_id)
    if question:
        answers = ans_object.fetch_all_answers(question_id)
        return jsonify({"Answers": answers}), 200
    return jsonify({"Message": "Question was not found"}), 401


@quiz.route('/questions/<int:question_id>/answers/<int:answer_id', methods=['PUT'])
@login_token_required
def approve_or_update_answer(current_user, answer_id):
    """This method will allow a user to update or approve a question"""
    user_input = request.get_json()
    new_title = user_input['answer_title']
    new_description = user_input['answer_statement']
    answer = ans_object.find_answer_by_id(answer_id)
    if answer:
        if current_user['username'] == answer['user_id']:
            response = quiz_obj.update_question(answer_id, new_title, new_description)
            if response:
                if new_title not in quiz_obj.questions:
                    return jsonify({'Message': 'Answer has been updated'}), 200
                return jsonify({'Message': 'That answer title already exists'}), 400
        return jsonify({"Message": "Sorry:You can only update your own answer!!"}), 401
    return jsonify({'Message': 'Answer not found'}), 404
