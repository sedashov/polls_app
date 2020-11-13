This API uses Django authorization and admin implementation.

This API introduces Poll and Question model.

Question model has question_text field (TextField), question_type field (TextField, choices: 'T' (text), '1V' (1 answer from some list), 'MV' (multiple answers from some list),
answer_choices field (TextField, which is a json representation of answer choices for 1V and MV types), answers (ManyToMany field to User through transitional table UserQuestion)

Poll model has title, start_date, finish_date, description fields. 

Question model has also a ForeignKey field, related to Poll.

Endpoints accessible for admins only (you have to explicitly pass admin login and password to the header of a request): 
1) /users/. Method: GET Displays list of all users. Method: POST creates a user.
2) /users/<int:id>/. Method: GET displays user. Method: PUT updates a user. Method: PATCH partially updates a user. Method: DELETE destroys a user
3) /polls/ Method: GET displays list of all polls with its questions, POST creates a poll. Note that you have to create questions here (e.g. pass this to request body):
```
"questions": [
        {
            "question_text": "Who is a president?",
            "question_type": "MV",
            "answer_choices": ["Me", "you", "both", "none"]
        },
        {
            "question_text": "What is your name?",
            "question_type": "T"
        }
    ],
```
Note that if question_type is 1V or MV, you have to provide answer_choices in a format of list of strings

4) /polls/<int:id>/. Method: GET displays a poll, PUT updates a poll (everything except for start_date), PATCH partially updates a poll, DELETE deletes it
5) /questions/ Method: GET displays all questions, POST creates a question
6) /questions/<int:id>/. Method: GET displays a question, PUT updated a question, PATCH partially updates a question, DELETE deletes it 


Endpoints accessible for everyone (even for unauthorized users):

7) /polls/active/ Method: GET displays all active polls
8) /polls/answer/ Method: POST requires fields user_id (may be blank to answer anonymously), poll_id, answers (dict {str(question_id): answer}, answers to all questions in a poll), writes an answer to a specified pool by a specified user
Method: GET requires user_id and (optionally) poll_id, displays all user's answers to a specified poll (if poll_id is blank, to all polls)
