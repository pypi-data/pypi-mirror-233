version 0.0.5
-------------
Added requirements.txt in MANIFEST file

version 0.0.4
-------------
Replaced absolute imports by relative ones
Fixed bug when closing pygenplot which could trigger crashed when used in external applications
Fixed bug when loading units
Several small fixes

version 0.0.3
-------------
Deep refactoring of the code to allow further integration of pygenplot in external projects
Added the possibility to draw and plot ROI
Several small fixes
Reformatted all docstrings according to PEP and type hints

version 0.0.2
-------------
The contents of a dataset can now be displayed by right-clicking on it in the data tree
Right-clicking on the tables showing the data does not trigger cell selection anymore. It only pops up the contextual menu
Fixed bug when right-clicking on the data panel when no data has been loaded
The cross-viewer integration boxes are now displayed
Fixed bug when closing/reopening the cross-viewer dialog which was not properly reset
Set the slicer lines colors in agreement with the corresponding integration boxes colors
Fixed bug when deselecting integration over x or y checkboxes which was not setting the slicer lines back

version 0.0.1
-------------
Fixed bug when opening lines settings dialog on MacOS
The single value data can now be plotted

version 0.0.0
-------------
Initial version
