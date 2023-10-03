.. image:: https://img.shields.io/pypi/v/kser-crypto.svg
   :target: https://pypi.python.org/pypi/kser-crypto/
   :alt: Latest Version

.. image:: https://travis-ci.org/cdumay/kser-crypto.svg?branch=master
   :target: https://travis-ci.org/cdumay/kser-crypto
   :alt: Latest version


.. image:: https://readthedocs.org/projects/kser-crypto/badge/?version=latest
   :target: http://kser-crypto.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/cdumay/kser-crypto/blob/master/LICENSE

.. image:: https://github.com/cdumay/kser-crypto/blob/reports/junit/tests-badge.svg?raw=true
   :target: https://htmlpreview.github.io/?https://github.com/cdumay/kser-crypto/blob/reports/junit/report.html
   :alt: Tests

.. image:: https://github.com/cdumay/kser-crypto/blob/reports/flake8/flake8-badge.svg?raw=true
   :target: https://htmlpreview.github.io/?https://github.com/cdumay/kser-crypto/blob/reports/flake8/index.html
   :alt: Lint

.. image:: https://github.com/cdumay/kser-crypto/blob/reports/coverage/coverage-badge.svg?raw=true
   :target: https://htmlpreview.github.io/?https://github.com/cdumay/kser-crypto/blob/reports/coverage/html/index.html
   :alt: Coverage badge

***********
kser-crypto
***********

`Kser <https://github.com/cdumay/kser>`_ module allow you to encrypt and decrypt messages in kafka using `libsodium <https://libsodium.org>`_.

----------
Quickstart
----------

First, install kser-crypto using
`pip <https://pip.pypa.io/en/stable/>`_:

    $ pip install kser-crypto[pykafka]

.. note::

    Only kafka-python is implemented at the moment.

--------
Examples
--------

Make sure to have the environment variable **KSER_SECRETBOX_KEY** definded.

Consumer
********

.. code-block:: python

    from kser_crypto.python_kafka.consumer import CryptoConsumer

    consumer = CryptoConsumer(config=dict(...), topics=[...])
    consumer.run()

Producer
********

.. code-block:: python

    import time
    from uuid import uuid4
    from kser.schemas import Message
    from kser_crypto.python_kafka.producer import CryptoProducer

    producer = CryptoProducer(config=dict(...))
    producer.send("test", Message(uuid=str(uuid4()), entrypoint="myTest"))
    time.sleep(1)

------------
Requirements
------------

- Python 3.x
- Libsodium

--------------
Documentations
--------------

- Project: http://kser.readthedocs.io/
- Libsodium: https://download.libsodium.org/doc/
- confluent-kafka-python: http://docs.confluent.io/current/clients/confluent-kafka-python
- kafka-python: http://kafka-python.readthedocs.io/en/master/

-----------
Other links
-----------

- PyPI: https://pypi.python.org/pypi/kser-crypto
- Project issues: https://github.com/cdumay/kser-crypto/issues

-------
License
-------

Licensed under MIT license (`LICENSE <./LICENSE>`_ or http://opensource.org/licenses/MIT)
