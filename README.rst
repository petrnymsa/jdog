Documentation WIP [https://jdog.readthedocs.io/en/latest/]


.. image:: https://github.com/petrnymsa/jdog/workflows/build-test/badge.svg

.. image:: https://readthedocs.org/projects/jdog/badge/?version=latest

*********************************************
Just another Data Offline Generator (JDOG) 🐶
*********************************************

- JDOG is Python library which helps generate sample data for your projects.
- JDOG can be run also as CLI tool.
- For generating sample data, the data scheme is provided
- The scheme is in JSON format

Scheme
======

- Scheme is provided in JSON format with special placeholders.
- Placeholder is something like variable, where generated data will be replaced.
- Output is nearly the same as scheme besides replaced placeholders.

In the simplest form, given JSON scheme

.. code-block::

    {
        "name": "Bob",
        "age" : "18"
    }

is **valid scheme** although no additional generation will proceed.

The simplest example can be

.. code-block::

    {
        "name": "Bob",
        "age": "{{number(18,100)}"
    }

which produce Bob with any age between <18, 99> e.g:

.. code-block::

    {
        "name": "Bob",
        "age": 26
    }

More useful example

.. code-block::

    {
        "{{range(people, 4)}}": {
            "name": "{{first_name}}",
            "age" : "{{number(18, 100)}}"

        }
    }
generates array of size 4 with objects containing name and age. The result

.. code-block::

    {
        "people": [{
                "name": "Bob",
                "age": "18"
            },
            {
                "name": "Alice",
                "age": 25
            },
            {
                "name": "George",
                "age": 85
            },
            {
                "name": "Janice",
                "age": 34
            }
        ]
    }

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

TODO - link to page about placeholders with example

*********
Use it
*********

.. code-block::

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
