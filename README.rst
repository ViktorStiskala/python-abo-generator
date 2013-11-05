python-abo-generator
====================

.. image:: https://badge.fury.io/py/abo-generator.png
    :target: http://badge.fury.io/py/abo-generator

ABO banking format generator.

Currently supports only "CSOB" compatible format

Specification sources: http://www.fio.cz/docs/cz/struktura-abo.pdf and http://www.equabank.cz/files/doc/13-format-abo.pdf (available only in czech).

.. code-block:: python

    from datetime import datetime, timedelta
    from abo import ABO

    tomorrow = datetime.now() + timedelta(days=1)
    abo_export = ABO(client_account_number='123456789/0300', client_name='Super company a.s.', due_date=tomorrow)

    abo_export.add_transaction('123456789/0100', 500.34, variable_symbol='123456', message='Hello world!')
    abo_export.add_transaction('155-987523423/2010', 1234.55, variable_symbol='789654321', message='Test transaction')

    with file('example.pkc', 'w') as f:
        abo_export.save(f)

Installation
------------

To install ABO generator, simply:

.. code-block:: bash

    $ pip install abo-generator

License
-------

This software is licensed under MPL 2.0.

- http://mozilla.org/MPL/2.0/
- http://www.mozilla.org/MPL/2.0/FAQ.html#use
