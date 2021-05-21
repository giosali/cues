# Cues

![Python Version](https://img.shields.io/pypi/pyversions/cues) ![PyPI](https://img.shields.io/pypi/v/cues) ![Development Status](https://img.shields.io/badge/development%20status-alpha-red) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/GBS3/cues/cues) [![codecov](https://codecov.io/gh/GBS3/cues/branch/main/graph/badge.svg)](https://codecov.io/gh/GBS3/cues) ![License](https://img.shields.io/pypi/l/cues)


Elegant and sophisticated prompts to inquire and ask questions at the command line.

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/snapshot.png" width="600">

## Compatibility

Windows | macOS | Linux
------- | ----- | -----
✔ | ✔ | ✔

## Installation

You can install Cues by using `pip`:

```
pip install cues
```

## Examples

<h3 align="center"><i><b>Select</b></i></h3>

You can use the `Select` class to create a prompt that asks the user to select a single option among a list of them, allowing the user to shuffle through them by using the arrow keys.

If you would like to to see an example of this in action, you can run the following command in your terminal:

```
python -m cues.select
```

Here's some example code showing how you could create a `Select` prompt:

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

You can use the `Confirm` class to create a prompt that displays a message to the user and then asks them to enter y (Yes) or N (No).

If you would like to to see an example of this in action, you can run the following command in your terminal:

```
python -m cues.confirm
```

Here's some example code showing how you could create a `Confirm` prompt:

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

You can use the `Form` prompt to display a series of fields for the user to answer and fill out.

If you would like to to see an example of this in action, you can run the following command in your terminal:

```
python -m cues.form
```

Here's some example code showing how you could create a `Form` prompt:

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

You can use the `Survey` class to display a series of questions to the user and have them give a rating based on a scale that you provide.

If you would like to to see an example of this in action, you can run the following command in your terminal:

```
python -m cues.survey
```

Here's some example code showing how you could create a `Survey` prompt:

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

<h3 align="center"><i><b>Checkbox</b></i></h3>

You can use the `Checkbox` class to give a user a list of options and have them select as many as they would like by using the spacebar.

If you would like to to see an example of this in action, you can run the following command in your terminal:

```
python -m cues.checkbox
```

Here's some example code showing how you could create a `Checkbox` prompt:

```python
from cues import Checkbox


name = 'guitars'
message = 'Pick your favorite guitars:'
options = [
    'Les Paul',
    'Stratocaster',
    'Telecaster',
    'SG',
    'Flying V',
    'Acoustic',
    'Classical',
]

cue = Checkbox(name, message, options)
answer = cue.send()
print(answer)
```

This produces the following output:

<img src="https://raw.githubusercontent.com/GBS3/cues/main/media/checkbox.gif" width="800">

## To Do

 - [x] Bring support to macOS
 - [x] Bring support to Linux
 - [ ] JSON prompt
 - [x] Checkbox prompt

 ...*amongst other things!*
