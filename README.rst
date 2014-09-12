Taarifa API
===========

Background
------------

Taarifa_ is an open source platform for the crowd sourced reporting and
triaging of infrastructure related issues. Think of it as a bug tracker for
the real world which helps to engage citizens with their local government.

Taarifa was founded at the 2011 London WaterHackathon, Winner of the 2013
Sanitation Hackathon, finalist at the 2014 Barcelona World Mobile Congress,
and has been deployed in Uganda, Ghana, and Tanzania.


The API
-------

The API forms the core of the Taarifa platform. It provides a RESTful
API (built on Flask_ and Eve_) that clients can interact with to create
and triage "bug reports" relating to public infrastructure (e.g., the
public toilet is broken).

To understand the API it is important to clarify some terminology:

- **service**: a service provided by some authority (e.g. electricity,
  water, road cleaning, ...)
- **facility**: category of physical infrastructure (e.g. power lines,
  water pipes, road network, ...)
- **resource**: particular addressable piece of infrastructure (e.g.
  Church Street, the waterpoint at (23.44,-5.87))
- **request**: a ticket/issue/report made by a citizen about a
  particular resource, service, or both

*Aside*: Those familiar with Open311_ will recognize the terminology and
semantics. While the Taarifa API is not fully Open311 compliant yet,
this is on the roadmap.

Taarifa API provides a way for clients to create services, facilities,
resources, and requests dynamically (at runtime). In particular the
features it provides include:

- defining new service/facility/resource/request schemas
- automatic validation that submitted service/facility/... instances
  conform to the schema
- versioning / history to track changes to resources and requests

Distributions
-------------

The goal is to have different distributions or flavours of Taarifa, built on
top of the core API. The main one is currently the `Taarifa Waterpoints`_
distribution.

Installation
------------

Ensure you have installed Python, pip and MongoDB and that MongoDB is running.

Install virtualenv_ and virtualenvwrapper (you might need admin rights for
this): ::

  pip install virtualenv virtualenvwrapper

`Set up virtualenvwrapper`_ according to your shell and create a virtualenv: ::

  mkvirtualenv TaarifaAPI

If you already created the virtualenv, activate it: ::

  workon TaarifaAPI

Clone the repository: ::

  git clone https://github.com/taarifa/TaarifaAPI

Change into the directory and install the requirements: ::

  cd TaarifaAPI
  pip install -r requirements.txt

Install the package itself: ::

  python setup.py develop


Usage
-----

Start the API server from the ``TaarifaAPI`` directory by running: ::

  python taarifa_api/taarifa_api.py

This should start the API server. To check things are working, open a
browser and navigate to: ::

  http://localhost:5000/api

This should show you the various endpoints available. To see the API
documentation go to: ::

  http://localhost:5000/docs


Contribute
----------

There is still much left do do and Taarifa is currently undergoing rapid
development. To get started send a message to the taarifa-dev_ mailinglist and
check out the github issues. We use the github pull request model for all
contributions. Refer to the `contributing guidelines`_ for further details.

.. _Taarifa: http://taarifa.org
.. _Taarifa Waterpoints: https://github.com/taarifa/TaarifaWaterpoints
.. _Open311: http://open311.org
.. _taarifa-dev: https://groups.google.com/forum/#!forum/taarifa-dev
.. _Eve: http://python-eve.org
.. _Flask: http://flask.pocoo.org
.. _contributing guidelines: CONTRIBUTING.rst
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
.. _Set up virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file
