"""
cues.select
===========

A module for demonstrating the Select class in cues.cues.
"""

from .cues import Select


def main(test=0):
    name = 'programming_language'
    message = 'Which of these is your favorite programming language?'
    options = ['Python', 'JavaScript', 'C++', 'C#']

    if not test:
        prompt = Select(name, message, options)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
