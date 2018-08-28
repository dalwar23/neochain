Install
=======
NEOChain requires Python 2.7, 3.4, 3.5, 3.6 or 3.7. If you do not already have a Python environment configured on your
computer, please see the python page `Python <https://www.python.org>`_ for instructions on installing Python environment.

.. note::
   if you are on Windows and want to install optional packages (e.g., scipy) then you will need to install a python
   distribution such as `Anaconda <https://www.anaconda.com>`_, `Enthought Canopy <https://www.enthought.com/product/canopy>`_
   or `Pyzo <https://www.pyzo.org>`_. If you use one of these Python distributions, please refer to their online documentation.

Assuming that the default python environment already configured on your computer and intend to install ``neochain`` inside
of it. To create and work with Python virtual environments, please follow instructions on
`venv <https://docs.python.org/3/library/venv.html>`_ and `virtual environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_

To start the installation process, please make sure the latest version of ``pip`` (Python package manager) is installed.
If ``pip`` is not installed, please refer to the `Pip documentation <https://pip.pypa.io/en/stable/installing/>`_ and
install ``pip`` first.

Install the released version
============================
Install the current release of ``neochain`` with ``pip``:

.. code-block::
   :linenos:

   pip install neochain

To upgrade to a newer version use the ``--upgrade`` flag:

.. code-block::
   :linenos:

   pip install --upgrade neochain

If system wide installation is not possible for permission reasons, use ``--user`` flag to install ``neochain`` for current
user

.. code-block::
   :linenos:

   pip install --user neochain

Alternatively, ``neochain`` can be installed manually by downloading the current version from
`GitHub <https://github.com/dharif23/neochain>`_ or `PyPI <https://pypi.org/project/neochain/>`_.
To install a downloaded versions, please unpack it in a preferred directory and run the following commands at the top
level of the directory:

.. code-block::
   :linenos:

   pip install .

or run the following:

.. code-block::
   :linenos:

   python setup install


