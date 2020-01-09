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

*********
CLI Usage
*********

- [PATH] (Positional argument) Path to scheme
- *-f*, *--format* [FORMAT] Output is in given format {json, xml}.
- *-s*, *--save* [PATH] Saves output at given path. **Optional**

By default, CLI tool does not save output to file, just print results to standard output.

TODO: .........
