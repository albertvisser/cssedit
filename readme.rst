CSSEdit
=======

A simple tree-based CSS editor.

Inspired by two things: the wish to have a tool that I can view "compressed" CSS files in without performing some magic in a text editor first; and the opportunity to have this pop up from within my HTML editor.
And, last but not least, a fresh case of Not Invented Here syndrom.


Usage
=====

The standalone version can be started with the `start_editor.py` script in this directory. Optionally you can provide a filename as parameter.

The embedded version is to be started from within an HTML editor, obviously; for that, import and call the `main` function from `cssedit_qt.py` in the `editor` subdirectory with either of the following arguments:

- filename = <filename>
- tag = <css selector>, data = <value of the tag's `style` attribute>
- text = <contents of the html's `<style>` element>

For the embedded version, the output will be returned the way it was provided; an extra parameter is available to specify the type of formatting to be applied for the filename or text variant. Possible formats are (at the moment):

- compressed (everyting on one line with superfluous spaces and comments removed)
- short (a line for each CSS selector)
- medium (CSS selectors and their properties on separate lines)
- long (all CSS selectors, all properties and trailing braces on separate lines)

In the standalone version, the same options will be available when saving to a file.


Dependencies
============

- Python
- PyQt4
- cssutils
