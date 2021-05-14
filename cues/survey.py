"""
cues.survey
===========

A module for demonstrating the Survey class in cues.cues.
"""

from .cues import Survey


def main(test=0):
    name = 'customer_satisfaction'
    message = 'Please rate your satisfaction with the following areas:'
    scale = [1, 2, 3, 4, 5]
    fields = [
        {
            'name': 'customer_service',
            'message': 'Customer service'
        },
        {
            'name': 'restaurant_service',
            'message': 'Restaurant service'
        },
        {
            'name': 'bar_service',
            'message': 'Bar service'
        },
        {
            'name': 'room_service',
            'message': 'Room service'
        }
    ]

    if not test:
        prompt = Survey(name, message, scale, fields)
        answer = prompt.send()
        print(answer)


if __name__ == '__main__':
    main()
