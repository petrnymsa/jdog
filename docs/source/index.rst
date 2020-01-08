.. JDOG documentation master file, created by
   sphinx-quickstart on Mon Jan  6 23:45:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#############################################
Just another Data Offline Generator (JDOG) 🐶
#############################################

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :hidden:

   pages/placeholders
   pages/extending

.. toctree::
   :maxdepth: 2
   :caption: API
   :hidden:

   pages/api

.. include:: ../../README.rst
   :start-after: start-inclusion-marker-do-not-remove
   :end-before: end-inclusion-marker-do-not-remove

Placeholders
------------

+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
|         Placeholder        |                          Arguments                          |                        Description                        |                Usage                |      Example     |
+============================+=============================================================+===========================================================+=====================================+==================+
| name(m|f)                  | M - only male, F - only female. No argument - both          | Generic full name                                         | {{name}}                            | Joe Hill         |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| first_name                 | M - only male, F - only female. No argument - both          | Generic first name                                        | {{first_name}}                      | Joe              |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| last_name                  | M - only male, F - only female. No argument - both          | Generic last name                                         | {{last_name}}                       | Hill             |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| number(l,h)                | l,h - int numbers                                           | Number between l (inclusive) to h (exclusive)             | {{number(1,8)}}                     | 7                |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| age                        |                                                             | Number between 1 and 99. Equal to number(1,100)           | {{age}}                             | 26               |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| city                       |                                                             | Generic city name                                         | {{city}}                            | Las Vegas        |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| street_address             |                                                             | Generic street address                                    | {{street_address}}                  | 4 Privet Drive   |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| lorem(n)                   | n - number                                                  | Generic lorem ipsum text contaning n words                | {{lorem(3)}}                        | Lorem ipsum text |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| empty                      |                                                             | Empty string field                                        | {{empty}}                           | ""               |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| range(prop, n,[m])         | prop - string                                               |                                                           | {{range(people,4)}} : {json object} |                  |
|                            |                                                             | Generate array with propert name "prop" and with N items  |                                     |                  |
|                            | n - number                                                  |                                                           |                                     |                  |
|                            | m - maximum, optional                                       | or randomly bettwen N and M (exclusive)                   |                                     |                  |
|                            |                                                             |                                                           |                                     |                  |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| bool                       |                                                             | Boolean value - true / false                              | {{bool}}                            | false            |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| option(arg1,arg2,...,argN) | Argument can be string, number or even another placeholder. | Choose randomly on of the argument.                       | {{option({{empty}},{{name}})}}      | Joe Hill         |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+

For more info visit :ref:`details <placeholders-label>`.

*********
Use it
*********

.. code-block:: python

    jdog = Jdog('cs_CZ')
    scheme = '....' # your scheme
    jdog.parse_scheme(scheme)

    result = jdog.generate()

* Just instantiate :class:`.jdog.Jdog` and optionally provide language code (en-US is default).
* Parse the scheme and call generate as many times you want.
* The result is JSON string.


Extending functionality
=======================
Jdog can be easily extended

.. code-block::

        # call add_matcher to provide new placeholder
        jdog.add_matcher('quote', lambda token: re.match('^{{quote}}$'), lambda token, args: return 'quote based on args')

For more info see :meth:`.jdog.Jdog.add_matcher`.

.. note::
    When you provide existing key, default behavior of any placeholder can be altered. To get all available placeholders use :meth:`.jdog.Jdog.placeholder_keys`.

TODO - link to page about extending functionality with example

Placeholder class and its derivatives
-------------------------------------

Each parsed placeholder is represented with *Placeholder* class. There are many derivatives of this base class.
New placeholder should either use *FuncPlaceholder* or sub-class *:class:`Placeholder*` or *:class:`FakerPlaceholder`* if faker usage is needed.

TODO: describe classes --- redirect to full documentation

*********
CLI Usage
*********

- [PATH] (Positional argument) Path to scheme
- *-f*, *--format* [FORMAT] Output is in given format {json, xml}.
- *-s*, *--save* [PATH] Saves output at given path. **Optional**

By default, CLI tool does not save output to file, just print results to standard output.

TODO: .........
