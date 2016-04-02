************
Contributing
************

This project is open to any kind of contribution. You can help with improving the documentation, adding fixes to the
code, providing test cases in code or as a description or just spreading the word. Please feel free to create an
issue or pull request.
In order to reduce the amount of work for everyone please try to adhere to good practice.

The pull requests and issues will be prefilled with templates. Please fill in your information where applicable.

This project uses `semantic versioning <http://semver.org/>`_ and tries to adhere to the proposed rules as
good as possible.

Style-Guide
-----------

When writing code please try to stick to these rules.

Python 2 and 3
^^^^^^^^^^^^^^
We have rewritten the code in order to maintain compatibility with both Python 2 and Python 3.
In order to ensure that we do not miss any accidental degradation, please add these imports to the top
of every file of code:

.. code-block:: Python

  from __future__ import absolute_import
  from __future__ import division
  from __future__ import print_function
  from __future__ import unicode_literals
 
Furthermore please be aware of the differences between Python 2 and 3. For
example `this guide <https://docs.python.org/3/howto/pyporting.html>`_ is helpful.
Special care has to be taken when dealing with strings and byte-strings. Please note
that the :py:meth:`~escpos.escpos.Escpos._raw`-method only accepts byte-strings.
Often you can achieve compatibility quite easily with a tool from the `six`-package.

PEP8
^^^^
This is not yet consequently done in every piece of code, but please try to ensure
that your code honors PEP8.
The checks by Landscape and QuantifiedCode that run on every PR will provide you with hints.

GIT
^^^
The master-branch contains code that always builds. Releases are tags on the master branch.
Currently, development happens in a separate branch, because we refactored basically the whole code.
Please branch of the HEAD of the current development-branch and create a pull request to development with your changes.

Try to group your commits into logical units. Before creating your pull request consider rebasing your branch to the
HEAD of the branch that you developed against. You can also regroup your commits during this rebase with the
feature `squash` of interactive rebasing. You may also do so after creating your PR, but please put up a notice
that you have force-pushed your changes into your feature-branch.
A force-push should never occur directly on the master- or development-branch.

When you create a branch please name your branch after what you are trying to achieve, e.g. when you add a new
feature that enables color printing, you could name the branch `feature/enable-color-printing`. This makes the log more
readable.
Imagine you improve text handling, then you could name your branch `improve/text-handling`.

Docstrings
^^^^^^^^^^
This project tries to have a good documentation.
Please add a docstring to every method and class. Have a look at existing methods and classes for the style.
We use basically standard rst-docstrings for Sphinx.

Test
^^^^
Try to write tests whenever possible. Our goal for the future is 100% coverage.
We are currently using `nose` but might change in the future.
You can copy the structure from other testcases. Please remember to adapt the docstrings.

Further reading
^^^^^^^^^^^^^^^
For further best practices and hints on contributing please see the
`contribution-guide <http://www.contribution-guide.org/>`_. Should there be any contradictions between this guide
and the linked one, please stick to this text.
Aside from that feel free to create an issue or write an email if anything is unclear.

Thank you for your contribution!
