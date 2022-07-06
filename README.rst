E3SM Data Documentation
=======================

TODO: Add an overview here

Getting Started
--------------------------

This documentation is created using
`Sphinx <http://www.sphinx-doc.org/en/stable>`_. Sphinx is an open-source tool
that makes it easy to create intelligent and beautiful documentation, written
by Georg Brandl and licensed under the BSD license.

The documentation is maintained in the ``main`` branch of the GitHub repository.
You can include code and its corresponding documentation updates in a single pull request (PR).

After merging a PR, GitHub Actions automates the documentation building process.
It pushes the HTML build to the ``gh-pages`` branch, which is hosted on GitHub Pages.

.. _conda-env:

Setup the Conda Environment
-------------------------------

1. Install Miniconda/Anaconda

2. Clone the repository ::

        git clone https://github.com/E3SM-Project/e3sm_data_docs.git

3. Enter the repo directory ::

        cd e3sm_data_docs

4. Create the ``e3sm_data_docs`` conda environment ::

        conda env create -f conda-env/docs.yml
        conda activate e3sm_data_docs

Edit Documentation
-------------------------------

Sphinx uses `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ as its markup language. For more information on how to write documentation using Sphinx, you can refer to:

* `First Steps with Sphinx <http://www.sphinx-doc.org/en/stable/tutorial.html>`_
* `reStructuredText Primer <http://www.sphinx-doc.org/en/stable/rest.html#external-links>`_

1. Create a branch from ``main``  ::

    git checkout main
    git checkout -b <BRANCH_NAME>

2. Edit the ``rst`` files under ``/docs/source``.

3. Build the HTML pages : ::

    cd docs
    make html

4. View them locally in a web browser at ``file:///<myDir>/e3sm_data_docs/docs/_build/html/index.html``

5. Commit and push changes ::

    cd <myDir>/e3sm_data_docs
    # `docs/_build` is ignored by git since it does not need to be pushed.
    git add .
    git commit "..."
    git push <fork-origin> <branch-name>

6. Create a pull request

Once this pull request is merged and GitHub Actions finishes building the docs, changes will be available on the
`e3sm_data_docs documentation page <https://e3sm-project.github.io/e3sm_data_docs/>`_.
