.. _placeholders-label:

############
Placeholders
############

Each placeholder serves as place where new, random value will be replaced in the output.

Generally each placeholder is enclosed between **{{** and **}}**. So for example:

.. code-block::

    {{placeholder}}

Some placeholders accept arguments and some arguments can be required or optional. See below details of each placeholder.

Optional placeholder within table is denoted by *[* arg *]*.

+-----------------------------------+-----------------------------------------------------------+
|         Placeholder               |                        Description                        |
+===================================+===========================================================+
| :ref:`name([m,f])`                | Generic full name                                         |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`first_name([m,f])`          | Generic first name                                        |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`last_name([m,f])`           | Generic last name                                         |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`number(l,h)`                | Number between l (inclusive) to h (exclusive)             |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`age`                        | Number between 1 and 99. Equal to number(1,100)           |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`city`                       | Generic city name                                         |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`street_address`             | Generic street address                                    |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`lorem(n)`                   | Generic lorem ipsum text contaning n words                |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`empty`                      | Empty string field                                        |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`range(prop,n,[m])`          | Generates property with "prop" name and array as its value|
+-----------------------------------+-----------------------------------------------------------+
| :ref:`bool`                       | Boolean value - true / false                              |
+-----------------------------------+-----------------------------------------------------------+
| :ref:`option(arg1,arg2,...,argN)` |  Choose randomly one of the argument.                     |
+-----------------------------------+-----------------------------------------------------------+

Defined placeholders
********************

Follows description of each defined placeholder available to use.

.. note::
    Internally JDOG using amazing `Faker package <https://faker.readthedocs.io>`_ to generate random values.

name([m,f])
===========
Generic person full name - that is first and last name.

Arguments
---------
*Optional* m - Generates male names.

*Optional* f - Generates female names.

If none of these arguments is provided then generates a male or female name.

Example
-------

.. code-block::

    {
        "full_name": "{{name}}"
    }

    # Example output

    {
        "full_name": "Joe Hill"
    }

first_name([m,f])
=================
Generic person first name.

Arguments
---------
*Optional* m - Generates male names.

*Optional* f - Generates female names.

If none of these arguments is provided then generates a male or female name.

Example
-------
.. code-block::

    {
        "first": "{{first_name(m)}}"
    }

    # Example output

    {
        "first": "Joe"
    }

last_name([m,f])
=================
Generic person last name.

Arguments
---------
*Optional* m - Generates male names.

*Optional* f - Generates female names.

If none of these arguments is provided then generates a male or female name.

Example
-------
.. code-block::

    {
        "last": "{{last_name(f)}}"
    }

    # Example output

    {
        "last": "Hills"
    }

number(l,h)
===========
Generates number between *l* and *h*. Note that *h* is **exclusive**.

Arguments
---------
* *l* - left boundary, inclusive

* *h* - right boundary, exclusive

Example
-------
.. code-block::

    {
        "age": "{{number(1,100)}}"
    }

    # Example output

    {
        "age": "42"
    }

age
===
Random number between 1 to 99. Effectively the same as using `{{number(1,100)}}`.

Arguments
---------
None.

Example
-------
.. code-block::

    {
        "age": "{{age}}"
    }

    # Example output

    {
        "age": "42"
    }

city
====
City name.

Arguments
---------
None

Example
-------
.. code-block::

    {
        "born_city": "{{city}}"
    }

    # Example output

    {
        "born_city": "Coruscant"
    }

street_address
==============
Generic street address.

Arguments
---------
None.

Example
-------
.. code-block::

    {
        "company_address": "{{street_address}}"
    }

    # Example output

    {
        "company_address": "5th avenue"
    }

lorem(n)
========
Random text containing *n* words.

Arguments
---------
*n* - How many words should text contain.

Example
-------
.. code-block::

    {
        "description": "{{lorem(6)}}"
    }

    # Example output

    {
        "description": "Find control party plan water prove safe."
    }

empty
=====
Empty value. Useful with combination in :ref:`option <option(arg1,arg2,...,argN)>` placeholder.

Arguments
---------
None.

Example
-------
.. code-block::

    {
        "title": "{{empty}}"
    }

    # Example output

    {
        "title": ""
    }

range(prop,n,[m])
=================
Generates property named *prop* with array of values. Number of values depends on arguments *n* and *m*.

Note that range placeholder *should be used at the left side* of property. See examples below.

Arguments
---------
* *prop* - Name of property.
* *n* - If only *n* specified array contains exactly *n* values.
* **optional** *m* - If *m* is specified array contains items exactly between *n* up to *m* times.

Example
-------
Generate exactly 4 people objects.

.. code-block::

    {
      "{{range(people,4)}}": {
        "name": "{{name}}",
        "age": "{{age}}",
        "address": {
          "city": "{{city}}"
        },
        "car": "{{option(mustang,{{empty}})}}"
      }
    }

    # Example output

    {
        "people": [
            {
                "name": "Brandi Young",
                "age": 39,
                "address": {
                    "city": "Jamietown"
                },
                "car": "mustang"
            },
            {
                "name": "Michelle Best",
                "age": 70,
                "address": {
                    "city": "Port Dustin"
                },
                "car": ""
            },
            {
                "name": "Donald Hernandez",
                "age": 79,
                "address": {
                    "city": "East Julieshire"
                },
                "car": "mustang"
            },
            {
                "name": "Kaitlyn Cook",
                "age": 3,
                "address": {
                    "city": "Rachelton"
                },
                "car": "mustang"
            }
        ]
    }

bool
====
Boolean value - *true* or *false*.

Arguments
---------
None.

Example
-------
.. code-block::

    {
        "awesome": "{{bool}}"
    }

    # Example output

    {
        "awesome": "true"
    }

option(arg1,arg2,...,argN)
==========================
Randomly choose one of the arguments (arg1,arg2,...,argN).
This is very useful to generate more randomised data.

Arguments
---------
 Each argument can be an arbitrary value or even another placeholder.

Example
-------
.. code-block::

    {
        "car": "{{option(mustang,{{empty}},C4)}}"
    }

    # Example output

    {
        "car": "mustang"
    }

    # ... or for example

    {
        "car": ""
    }

.. note::
    Missing some placeholder? JDOG can be easily :ref:`extended <extending-label>`.
