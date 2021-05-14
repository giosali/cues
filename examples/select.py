"""
examples.select
===============

An example that demonstrates the Select child class.
"""

from cues.cues import Select


def main():
    name = 'programming_language'
    message = 'Which of these is your favorite programming language?'
    options = ['Python', 'JavaScript', 'C++', 'C#']

    cue = Select(name, message, options)
    answer = cue.send()
    print(answer)


if __name__ == '__main__':
    main()
