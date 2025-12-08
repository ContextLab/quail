.. _installation:

Installation
============

To install quail in the recommended way, run:

.. code-block:: bash

    pip install quail

This will install quail with basic functionality.  To install with speech decoding dependencies (Note: you will still need to install ffmpeg manually on your computer since it is not pip installable):

.. code-block:: bash

    pip install quail[speech-decoding]

For CDL users, you can install speech decoding and efficient learning capabilities like this:

.. code-block:: bash

    pip install quail[speech-decoding, efficient-learning]

To install directly from this repo (not recommended, but you'll get the "bleeding edge" version of the code):

.. code-block:: bash

    git clone https://github.com/ContextLab/quail.git

Then, navigate to the folder and type:

.. code-block:: bash

    pip install -e .

Requirements
------------

+ python>=3.6
+ pandas>=2.0.0
+ seaborn>=0.12.0
+ matplotlib>=3.5.0
+ scipy>=1.10.0
+ numpy>=2.0.0
+ joblib>=1.3.0
+ pytest (for development)

If installing from github (instead of pip), you must also install the requirements:

.. code-block:: bash

    pip install -r requirements.txt
