============
Installation
============

Prerequisites
-------------

Install `Anaconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_.

(Optional) Get the .whl file of `PDFgetX <https://www.diffpy.org/products/pdfgetx.html>`_.
This package is used to transform the XRD data to PDF data.
If you are not using the functionality in pdfstream related to the PDF, this package is not necessary.

General Installation
--------------------

This is the instructions for the users. It is suggested to install it in a clean environment.

At the command line::

    conda create -n pdfstream_env -c conda-forge pdfstream

The ``pdfstream_env`` in the command is the name of the environment. It can be changed to any name.

Activate the environment::

    conda activate pdfstream_env

(Optional) Install the `diffpy.pdfgetx` using .whl file::

    pdfstream_install <path to .whl file>

Change the ``<path to .whl file>`` to the path of the .whl file on your computer.

Before using the `PDFstream`, remember to activate the environment::

    conda activate pdfstream_env

Development Installation
------------------------

This is the instructions for the developers and maintainers of the package.

**Fork** and clone the github repo and change the current directory::

    git clone https://github.com/<your account>/pdfstream

Remember to change ``<your account>`` to the name of your github account.

Change directory::

    cd PDFstream

Run the bash script::

    bash install.sh

