.. _extending-label:

**************
Extending JDOG
**************

If you want change behavior of some defined placeholder or, more likely, introduce new one you can.

JDOG instance has two methods which support you to extend behavior.

* :meth:`~jdog.jdog.Jdog.add_matcher` - adds new matcher and placeholder behavior
* :meth:`~jdog.jdog.Jdog.placeholder_keys` - returns already defined placeholders

Each **placeholder** is represented by some sub-class of :class:`~jdog.placeholder.placeholder.Placeholder` class.

Especially will come handy `~jdog.placeholder.placeholder.FuncPlaceholder` which can be easily used to introduce new placeholders.
Of course it is possible to sub-class :class:`~jdog.placeholder.placeholder.Placeholder`.

So, how to add a new placeholder?
=================================
For example we want to introduce *fizzbuzz* placeholder which with 50% chance print 'fizz' or 'buzz'.

Its only a few steps and you are good to go.

#. Think of a new name (or use an existing one)
#. Create regex pattern
#. Add matcher
#. Add placeholder - use :class:`~jdog.placeholder.placeholder.FuncPlaceholder` or sub-class :class:`~jdog.placeholder.placeholder.Placeholder`
#. Put it together and call :meth:`~jdog.jdog.Jdog.add_matcher`

Come up with new name
---------------------
It should be clear, only by name, what placeholder does. Beside the name think also about arguments.

.. warning::

    If you use existing name new behavior will replace odl one.

Create regex pattern
--------------------
During parsing phase each placeholder is *tokenized*. Tokenization process use regex to match each placeholder.

Starting regex should look like **`^{{token}}$`**, that is:

* It must have start with double {{
* It must have end with double }}

If you want arguments **it must have** arguments capture as group, that is `^{{token\((.*)\)$`.

* It must have start with double {{
* It must have end with double }}
* It must have *(* and *)*
* Capture anything between () to the group.

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

Simple, isn't it? (If in doubt, take a look for example `here <https://www.debuggex.com/cheatsheet/regex/python>`_.)

Add matcher
-----------
The matcher is a function which takes token and should decide whatever it is a placeholder which we want or not.
That is, just use regex match function and return the result or None if no match found.

.. code-block::

    # name matcher looks like this (kind of)
    def match_name(token):
        return re.match(r'^{{name\(?([f,m]?)\)?}}$', token)

    # and our fizzbuzz
    def match_fizzbuzz(token):
        return re.match(r'^{{fizzbuzz}}$', token)

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

If you want more fine grained functionality, just sub-class :class:`~jdog.placeholder.placeholder.Placeholder` and use it.

.. note::
    If you want to automatically enclose returned value by placeholder within double quotes use :class:`~jdog.placeholder.placeholder.FuncStrPlaceholder`.

Putting it together
-------------------
We have *name*, *matching function* and function which has logic of our *fizzbuzz placeholder*

On the instance of :class:`~jdog.jdog.Jdog` call :meth:`~jdog.jdog.Jdog.add_matcher` function.
Function takes three arguments

* **key** - the unique identification of placeholder - name.
* **f_matcher** - our matching function.
* **f_placeholder** - function which takes two arguments - token and arguments and should return placeholder.

Putting it together

.. code-block::

    # our matching function
    def match_fizzbuzz(token):
        return re.match(r'^{{fizzbuzz}}$', token)

    # placeholder logic
    def fizzbuzz(args):
        if random.random() > 0.5:
            return 'fizz'
        return 'buzz'

    # helper function to create placeholder
    def create_fizzbuzz(token, args):
        return FuncStrPlaceholder(token, args, fizzbuzz)

    jdog = Jdog()
    jdog.add_matcher('fizzbuzz',match_fizzbuzz, create_fizzbuzz)

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