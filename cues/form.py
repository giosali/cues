"""
cues.form
=========

A module for demonstrating the Form class in cues.cues.
"""

from .cues import Form


def main(test=0):
    name = 'basic_info'
    message = 'Please fill out the following form:'
    fields = [
        {
            'name': 'first_name',
            'message': 'What is your first name?',
            'default': 'Giovanni'
        },
        {
            'name': 'last_name',
            'message': 'What is your last name?',
            'default': 'Salinas'
        },
        {
            'name': 'language',
            'message': 'What is your favorite programming language?'
        }
    ]

    if not test:
        prompt = Form(name, message, fields)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
