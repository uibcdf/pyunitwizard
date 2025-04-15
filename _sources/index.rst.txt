.. pyunitwizard documentation master file

PyUnitWizard
============

There are several Python libraries to work with physical quantities in the market. Pint, unyt or openmm.unit, are just some of them. Imagine that your project, or workflow, requires the interaction with more than one of these tools. Or that you are not sure if you will work with a different quantities library in the future. Are you looking for a unique API to work with different quantities libraries? Wouldn't it be a relief? PyUnitWizard just do that. It is the wizard you need in your code to change the form of your quantities with few effort. With PyUnitWizard you can:

- Convert physical quantities and units between the different native objects from a set of :ref:`supported libraries<libraries-supported>`.
- Work with physical quantities with a simple syntaxis no matter the library you chose to do the hard work in the background.
- Integrate a quantities wizard in your library defining the default library and the standard units in you project.

Have a look to the `quick guide <https://uibcdf.org/PyUnitWizard/Quick_Guide.html>`_ to see some examples of PyUnitWizard in action.


.. _libraries-supported:

Libraries supported
-------------------

- `pint <https://github.com/hgrecco/pint>`_
- `unyt <https://github.com/yt-project/unyt>`_
- `openmm.unit <https://github.com/openmm/openmm/tree/master/wrappers/python/openmm/unit>`_ (openmm.unit in a near future)

.. toctree::
   :name: about
   :caption: About
   :maxdepth: 2

   contents/about/introduction.md
   contents/about/installation.md
   contents/about/showcase/index.rst

.. toctree::
   :name: user_guide
   :caption: User guide
   :maxdepth: 2

   contents/user/Importing.ipynb
   contents/user/Quantities_and_Units.ipynb
   contents/user/Dimensionality.ipynb
   contents/user/Convert.ipynb
   contents/user/Strings.ipynb
   contents/user/Lists_and_arrays.ipynb
   contents/user/Standardize.ipynb
   contents/user/Check.ipynb
   contents/user/In_Your_Library.ipynb

.. toctree::
   :name: developer_guide
   :caption: Developer Guide
   :maxdepth: 2

   contents/developer/intro/index.rst
   contents/developer/names_convention.ipynb
   contents/developer/exceptions.ipynb
   contents/developer/documentation/index.rst

.. toctree::
   :name: api_doc
   :caption: API Documentation
   :maxdepth: 2

   api_user.rst
   api_developer.rst


Glossary, indices and tables
============================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

