.. image:: AxisVM_logo.bmp

PyAxisVM - The official Python package for **AxisVM**
=====================================================

----

.. image:: gt40.png

.. note::
    The documentation is under heavy development. Expect changes more often than usual,
    and enjoy what is alraeady out. This only affects the documentation, not the code base. 
    Until we het to the end of it, browse the examples and the notebooks to get a glimpse 
    of what the library can provide!

The **PyAxisVM** project offers a high-level interface to **AxisVM**, 
making its operations available directly from Python. It builds on top of 
Microsoft's COM technology and supports all the features of the original 
**AxisVM** COM type library, making you able to

* build, manipulate and analyse **AxisVM** models

* find better solutions with iterative methods

* combine the power of **AxisVM** with third-party Python libraries

* build extension modules

On top of that, **PyAxisVM** enhances the type library with Python's slicing 
mechanism, context management and more, that enables writing clean, concise, 
and readable code.

.. _getting started:

.. include:: getting_started.md
    :parser: myst_parser.sphinx_

.. include:: tips_and_tricks.md
    :parser: myst_parser.sphinx_

.. toctree::
    :caption: Contents
    :maxdepth: 3

    notebooks
    downloads
    auto_examples/index.rst

.. toctree::
    :caption: API
    :maxdepth: 6
    :hidden:

    api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



