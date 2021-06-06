# v0.3.0

## Features

* Added a new cue: the `Password` cue
* Added tests for the `Password` cue
* Added documentation for the `Password` cue

## Fixes

* Fixed documentation mistakes for instantiating from `dict`s for several cues

# v0.2.2

## Fixes

* Fixed bug in `Form` cue that would use the fields' messages instead of their names when creating the response dict
* Improved test coverage

# v0.2.1

## Fixes

* Improved coverage for `Confirm` cue
* Added `canvas.py` module
  * Added test for `canvas.py` module
* Rewrote `Form` cue
  * Should behave much better now (no more flashing!)
  * Can now use left and right arrow keys
  * Can now use Backspace/Delete key
* Begun gradual switch to NumPy-styled docstrings

# v0.2.0

## Features

* Added a new cue: the `Checkbox` cue
* Added test for `Checkbox` module
* Created documentation for the *Cues* library
* Added ANSI code for the spacebar

## Fixes

* Reorganized cues so that they each reside in their own individual module

# v0.1.1

## Fixes

* Fixed issue where user could not access examples from command line due to an AttributeError


# v0.1.0

Initial release