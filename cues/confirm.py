"""
cues.confirm
==============

A module for demonstrating the Confirm class in cues.cues.
"""

from .cues import Confirm


def main(test=0):
    name = 'continue'
    message = 'Are you sure you want to continue?'

    if not test:
        prompt = Confirm(name, message)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
