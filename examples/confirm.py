"""
examples.confirm
===============

An example that demonstrates the Confirm child class.
"""

from cues.cues import Confirm


def main():
    name = 'continue'
    message = 'Are you sure you want to continue?'

    cue = Confirm(name, message)
    answer = cue.send()
    print(answer)


if __name__ == '__main__':
    main()
