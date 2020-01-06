Documentation WIP [https://jdog.readthedocs.io/en/latest/]


.. image:: https://github.com/petrnymsa/jdog/workflows/jdog/badge.svg

Just another Data Offline Generator (JDOG) 🐶
*********************************************

- JDOG is Python library which helps generate sample data for your projects.
- JDOG can be run also as CLI tool.
- For generating sample data, the data scheme is provided
- The scheme is in JSON format

Scheme
======
- Scheme of data is provided as a JSON file with special placeholders.
- Placeholder is, special place within JSON, and its purpose is like variable, where generated data will be replaced.
- Output file is nearly the same as scheme besides replaced placeholders.

In the simplest form, given JSON file::

    {
        "name": "Bob",
        "age" : "18"
    }

is **valid scheme** although no additional generation will proceed.

The simplest example could be::

    {
        "name": "Bob",
        "age": "{{number(18,100)}"
    }


which produce Bob with any age between <18, 99> where. So for example::

    {
        "name": "Bob",
        "age": 26
    }


Let's go wild::

    {
        "{{range(people, 4)}}": {
            "name": "{{first_name}}",
            "age" : "{{number(18, 100)}}"

        }
    }


generates array of size 4 with objects containing name and age. Example result::

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
============

+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
|         Placeholder        |                          Arguments                          |                        Description                        |                Usage                |      Example     |
+============================+=============================================================+===========================================================+=====================================+==================+
| name                       |                                                             | Generic full name                                         | {{name}}                            | Joe Hill         |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| first_name                 |                                                             | Generic first name                                        | {{first_name}}                      | Joe              |
+----------------------------+-------------------------------------------------------------+-----------------------------------------------------------+-------------------------------------+------------------+
| last_name                  |                                                             | Generic last name                                         | {{last_name}}                       | Hill             |
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


Usage in code
=============

Basic usage ::

    jdog = Jdog('cs_CZ')
    scheme = '....' # your scheme
    jdog.parse_scheme(scheme)

    result = jdog.generate()

Just instantiate Jdog class and provide language code (en-US is default). Parse the scheme and call generate as many times you want.
The result is json string.


Extending functionality
-----------------------
Jdog can be easily extended::

        # just call add_matcher to provide new placeholder
        jdog.add_matcher('quote', lambda token: re.match('^{{quote}}$'), lambda token, args: return 'quote based on args'):

Function *add_matcher* takes three arguments:

- key: unique identification of placeholder
- f_matcher: function which takes one argument - token and should return boolean if token matches
- f_placeholder: function which takes token and parsed arguments. Should return *Placeholder* object. See below.

Note: with providing existing key, default behavior of any placeholder can be altered. To get all available placeholders, call *defined_keys* method.

Placeholder class and its derivatives
-------------------------------------
Each parsed placeholder is represented with *Placeholder* class. There are many derivatives of this base class.
New placeholder should either use *FuncPlaceholder* or sub-class *Placeholder* or *FakerPlaceholder* if faker usage is needed.

TODO: describe classes --- redirect to full documentation


CLI Usage
=========

- [PATH] (Positional argument) Path to scheme
- *-f*, *--format* [FORMAT] Output is in given format {json, xml}.
- *-s*, *--save* [PATH] Saves output at given path. **Optional**

By default, CLI tool does not save output to file, just print results to standard output.

TODO: .........
