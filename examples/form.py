"""
examples.form
===============

An example that demonstrates the Form child class.
"""

from cues.cues import Form


def main():
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

    cue = Form(name, message, fields)
    answer = cue.send()
    print(answer)


if __name__ == '__main__':
    main()
