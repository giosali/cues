# Cues

Elegant and sophisticated prompts to inquire and ask questions at the command line.

## Compatibiliy

Windows | macOS | Linux
------- | ----- | -----
✔ | ✔ | ❌

## Installation

Install with `pip`:

```
pip install cues
```

## Examples

<h3 align="center"><i><b>Select</b></i></h3>

```python
from cues import Select


name = 'programming_language'
message = 'Which of these is your favorite programming language?'
options = ['Python', 'JavaScript', 'C++', 'C#']

cue = Select(name, message, options)
answer = cue.send()
print(answer)
```

This produces the following output:

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/select.gif" width="800">

<h3 align="center"><i><b>Confirm</b></i></h3>

```python
from cues import Confirm


name = 'continue'
message = 'Are you sure you want to continue?'

cue = Confirm(name, message)
answer = cue.send()
print(answer)
```

This produces the following output:

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/confirm.gif" width="800">

<h3 align="center"><i><b>Form</b></i></h3>

```python
from cues import Form


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
        'name': 'birthday',
        'message': 'What is your favorite programming language?'
    }
]

cue = Form(name, message, fields)
answer = cue.send()
print(answer)
```

This produces the following output:

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/form.gif" width="800">

<h3 align="center"><i><b>Survey</b></i></h3>

```python
from cues import Survey


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
```

This produces the following output:

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/survey.gif" width="800">

## To Do

 - [x] Bring support to macOS
 - [ ] Bring support to Linux
 - [ ] JSON prompt
 - [ ] Checkbox prompt

 ...*amongst other things!*
