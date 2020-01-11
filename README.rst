.. image:: https://github.com/petrnymsa/jdog/workflows/build-test/badge.svg

.. image:: https://readthedocs.org/projects/jdog/badge/?version=latest

*********************************************
Just another Data Offline Generator (JDOG) 🐶
*********************************************


🗎 `Full documentation <https://jdog.readthedocs.io/en/latest/>`_.
==================================================================


.. start-inclusion-marker-do-not-remove

- JDOG is a Python library which helps generate a sample data for your projects.
- JDOG can also be run as CLI tool.
- For generating a sample data, the data scheme is provided.

Scheme
======

- The *scheme* is provided in JSON format with special placeholders.
- In the output, the placeholders are replaced with some generated data.

Any valid JSON is **valid** scheme.

How to use it?
==============

Install it

.. code-block::

    python -m pip install jdog

Prepare a scheme

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

Use it

.. code-block::

    from jdog import Jdog

    def main():
        jdog = Jdog()
        scheme = ... # your loaded scheme

        # parse scheme
        jdog.parse_scheme(scheme)

        # generate instance
        result = jdog.generate()

        print(result) # result is JSON

And the example result:

.. code-block::

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

CLI
****
Package can be used as cli tool.

.. code-block::

    Usage: jdog [OPTIONS] SCHEME

    Accepts SCHEME and generates new data to stdin or to specified OUTPUT

    Options:
      -p, --pretty           Output as pretty JSON.
      -s, --strict           Raise error when no matching placeholder is found.
      -l, --lang TEXT        Language to use.
      --lang-help            Displays available language codes and exit.
      -o, --output FILENAME  Output file where result is written.
      --help                 Show this message and exit.


By default, CLI tool does not save output to file, just print results to standard output.

.. end-inclusion-marker-do-not-remove

👍 JDOG is using awesome package `Faker <https://faker.readthedocs.io>`_ which is used to generate random data.

`CONTRIBUTING <https://github.com/petrnymsa/jdog/blob/master/CONTRIBUTING.md>`_
===============================================================================

`LICENSE <https://github.com/petrnymsa/jdog/blob/master/LICENSE>`_
===============================================================================
