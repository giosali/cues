"""
examples.survey
===============

An example that demonstrates the Survey child class.
"""

from cues.cues import Survey


def main():
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

    cue = Survey(name, message, scale, fields)
    answer = cue.send()
    print(answer)


if __name__ == '__main__':
    main()
