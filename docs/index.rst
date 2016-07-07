Python Library Template Documentation
=====================================

|build_badge| |doc_badge| |pypi_badge| |requires_badge| |coverage_badge| |issues_badge| |license_badge|


Python library template project.


Installation
------------

.. code:: bash

    pip install python-template


Or to manually install, execute the following commands:


.. code:: bash

    git clone https://github.com/derek-miller/python-template.git
    cd python-template/
    python setup.py install


Usage
-----

.. code:: python

    # Insert demo code here


Scripts
-------

<script_name>
~~~~~~~~~~~~~

.. code:: bash

    # Insert usage text here


For full API usage documentation, refer to the `API <api.html>`__

v0.0.3 - 07/07/2016
~~~~~~~~~~~~~~~~~~~

-  Unpinned pip now that pip-compile works with 8.1.2

v0.0.2 - 06/12/2016
~~~~~~~~~~~~~~~~~~~

-  Fixed Makefile install target so it rebuilds the compiled requirements everytime it is run.
-  Removed temporary requirement in requirements/install-py2.txt

v0.0.1 - 05/30/2016
~~~~~~~~~~~~~~~~~~~

-  Initial release

|
|

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Site Map
--------
.. toctree::

    api


.. |build_badge| image:: https://img.shields.io/travis/derek-miller/python-template.svg
    :alt: Build Status
    :target: https://travis-ci.org/derek-miller/python-template

.. |doc_badge| image:: https://readthedocs.org/projects/python-template2/badge/?version=latest
   :alt: Documentation Status
   :target: http://python-template2.readthedocs.io/en/latest/?badge=latest

.. |pypi_badge| image:: https://img.shields.io/pypi/v/python-template.svg
    :alt: PyPi Status
    :target: https://pypi.python.org/pypi/python-template/

.. |requires_badge| image:: https://img.shields.io/requires/github/derek-miller/python-template.svg
    :alt: Requires.io
    :target: https://requires.io/github/derek-miller/python-template/requirements/?branch=master

.. |coverage_badge| image:: https://img.shields.io/codecov/c/github/derek-miller/python-template.svg
    :alt: Test Coverage
    :target: https://codecov.io/gh/derek-miller/python-template

.. |issues_badge| image:: https://img.shields.io/github/issues/derek-miller/python-template.svg
    :alt: GitHub Issues
    :target: https://github.com/derek-miller/python-template/issues

.. |license_badge| image:: https://img.shields.io/github/license/derek-miller/python-template.svg
    :alt: License
    :target: https://github.com/derek-miller/python-template/blob/master/LICENSE
