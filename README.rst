.. image:: https://github.com/petrnymsa/jdog/workflows/build-test/badge.svg

.. image:: https://readthedocs.org/projects/jdog/badge/?version=latest

*********************************************
Just another Data Offline Generator (JDOG) 🐶
*********************************************

🗎 `Full documentation <https://jdog.readthedocs.io/en/latest/>`_.

.. start-inclusion-marker-do-not-remove

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

.. code-block:: json

    {
        "name": "Bob",
        "age" : "18"
    }

is **valid scheme** although no additional generation will proceed.

The simplest example can be

.. code-block:: json

    {
        "name": "Bob",
        "age": "{{number(18,100)}"
    }

which produce Bob with any age between <18, 99> e.g:

.. code-block:: json

    {
        "name": "Bob",
        "age": 26
    }

More useful example

.. code-block:: json

    {
        "{{range(people, 4)}}": {
            "name": "{{first_name}}",
            "age" : "{{number(18, 100)}}"

        }
    }

generates array of size 4 with objects containing name and age. The result

.. code-block:: json

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

.. end-inclusion-marker-do-not-remove

TODO - faker info
