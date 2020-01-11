.. _extending-label:

**************
Extending JDOG
**************

It's easy to add new placeholder.

JDOG instance has two methods which support you to extend behavior.

* :meth:`~jdog.jdog.Jdog.add_matcher` - adds new matcher and placeholder behavior
* :meth:`~jdog.jdog.Jdog.placeholder_keys` - returns already defined placeholders

Each **placeholder** is represented by some subclass of :class:`~jdog.placeholder.placeholder.Placeholder` class.

Especially comes handy :class:`~jdog.placeholder.placeholder.FuncPlaceholder` which can be easily used to introduce new placeholders.

So, how to add a new placeholder?
=================================
For example we want to introduce *fizzbuzz* placeholder which with 50% chance print 'fizz' or 'buzz'.

Its only a few steps and you are good to go.

#. Think of a new name (or use an existing one).
#. Create regex pattern.
#. Add placeholder - use :class:`~jdog.placeholder.placeholder.FuncPlaceholder` or subclass :class:`~jdog.placeholder.placeholder.Placeholder`.
#. Put it together and call :meth:`~jdog.jdog.Jdog.add_matcher`.

Come up with new name
---------------------
It should be clear, only by name, what placeholder does. Beside the name think also about arguments.

.. warning::

    If you use existing name new behavior will replace odl one.

Create regex pattern
--------------------
During parsing phase each placeholder is *tokenized*. Tokenization process use regex to match each placeholder.

Starting regex could look like **`^{{token}}$`**, that is:

* It has to start with double {{
* It has to end with double }}

If you want any arguments for the placeholder, regex **has to capture** arguments as a group, that is `^{{token\((.*)\)$`.

A few examples of existing placeholders:

.. code-block:: python

    # age
    r'^{{age}}$'

    # number
    r'^{{number\((.*)\)}}$'

    # name (most complex one, arguments are optional)
    r'^{{name\(?([f,m]?)\)?}}$'

    # and new one
    r'^{{fizzbuzz}}$'

Simple, isn't it? (If in doubt, take a look `here <https://www.debuggex.com/cheatsheet/regex/python>`_.)

Add placeholder
---------------
Placeholder is special class that holds logic of generating specific values.

The easiest way is to use :class:`~jdog.placeholder.placeholder.FuncPlaceholder`.

* Takes argument - function.
* This function takes one argument - placeholder *arguments* as list.

So to our fizzbazz example:

.. code-block::

    def fizzbuzz(args):
        if random.random() > 0.5:
            return 'fizz'
        return 'buzz'

If you want more fine grained functionality, just subclass :class:`~jdog.placeholder.placeholder.Placeholder` and use it.

.. note::
    If you want to automatically enclose returned value by placeholder within double quotes use :class:`~jdog.placeholder.placeholder.FuncStrPlaceholder`.

Putting it together
-------------------
We have *name*, *regex* pattern and function which has logic of our *fizzbuzz placeholder*

On the instance of :class:`~jdog.jdog.Jdog` call :meth:`~jdog.jdog.Jdog.add_matcher` function.
Function takes three arguments

* **key** - the unique identification of placeholder - name.
* **pattern** - our regex pattern.
* **f_placeholder** - function which takes two arguments - token, it's arguments and should return :class:`~jdog.placeholder.placeholder.Placeholder` subclass.

Putting it together

.. code-block::

    # our pattern
    pattern = r'^{{fizzbuzz}}$'

    # placeholder logic
    def fizzbuzz(args):
        if random.random() > 0.5:
            return 'fizz'
        return 'buzz'

    # helper function to create placeholder
    def create_fizzbuzz(token, args):
        return FuncStrPlaceholder(token, args, fizzbuzz)

    jdog = Jdog()
    jdog.add_matcher('fizzbuzz', pattern, create_fizzbuzz)

.. warning::
    We are using :class:`~jdog.placeholder.placeholder.FuncStrPlaceholder` to automatically enclose value within double quotes.
    If you generate string values and do not enclose them result is not valid JSON.

Example can be simplified using lambda expressions.

.. code-block::

    jdog.add_matcher('fizzbuzz',match_fizzbuzz, lambda token, args: FuncStrPlaceholder(token, args, fizzbuzz))

We can go further

.. code-block::

    # in fizzbuzz logic, we dont really care about arguments
    jdog.add_matcher('fizzbuzz',match_fizzbuzz, lambda token, args: FuncStrPlaceholder(token, args,lambda _: 'fizz' if random.random() > 0.5 else 'buzz'))

But remember less lines does not mean more readable code. In this example rather opposite.