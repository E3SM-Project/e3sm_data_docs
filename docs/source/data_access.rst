.. _data-access:

Accessing E3SM Data
===================

This page describes how E3SM archives released simulation output and how to
retrieve it. Each dataset page links to a table of simulations; this page
explains how to use the paths and links in those tables.

How E3SM data is archived
*************************

E3SM simulation output is archived and released in the following ways. Each
links to a section below describing how to retrieve it.

* :ref:`NERSC HPSS <nersc-hpss-access>` -- Native model output
  is archived on the `NERSC HPSS <https://docs.nersc.gov/filesystems/archive/>`_
  tape system in directories with world-read permissions (under
  ``/home/projects/e3sm/www/`` or a user's ``www`` directory). Because the
  files are world-readable, they can be retrieved either by NERSC users with
  the standard HPSS tools, or by anyone through the NERSC HPSS web portal at
  `https://portal.nersc.gov/archive/home/projects/e3sm/www/ <https://portal.nersc.gov/archive/home/projects/e3sm/www/>`_
  (or ``https://portal.nersc.gov/archive/home/<u>/<user>/www/`` for a user's
  ``www`` directory). Each simulation table lists the **HPSS Path** of each
  simulation and, where available, an **HPSS URL** to the corresponding web
  portal page.

  Most campaign output is archived with `zstash <https://e3sm-project.github.io/zstash>`_,
  which stores files in a series of tar files together with an ``index.db``
  database listing their contents. Some datasets (e.g., the AI training
  datasets) instead provide an ``archive_contents`` text file listing the files
  in each tar archive.

* :ref:`ESGF <esgf-access>` -- Data reformatted to CMIP
  conventions (and, for some campaigns, native model output) is published to
  the `Earth System Grid Federation (ESGF) <https://aims2.llnl.gov/search>`_.
  When an ESGF link is listed in a simulation table, ESGF is the preferred
  retrieval method.

* :ref:`Globus sharing <globus-sharing>` -- High-usage datasets, i.e., those
  being actively analyzed by E3SM, may also have a copy on the NERSC Community
  File System (CFS), shared through Globus. Simulation tables list these
  copies' **Data on Disk** path and **Globus URL**. Currently, this applies to
  the :doc:`AI training datasets <AITraining/simulation_data/simulation_table>`.
  Because the data is already on disk, this is usually much faster than
  retrieving it from tape. These disk copies are **not guaranteed
  to persist** -- the HPSS archive is the authoritative long-term copy.

**Run scripts.** Where available, the scripts originally used to run each
simulation campaign are archived in the
`run_scripts <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts>`_
directory of this repository, and are linked from each dataset page. Original
run scripts **will not run out-of-the-box**; they are provided as guidance for
setting up a similar run. For some campaigns (e.g., E3SMv2), separate
reproduction scripts are also provided.

.. _nersc-hpss-access:

NERSC HPSS
**********

All simulations with an **HPSS Path** in the simulation table can be retrieved
from NERSC HPSS, either with a NERSC account or, more slowly, through the web
portal without one.

With a NERSC account
--------------------

This is the most efficient way to retrieve data from HPSS, and is recommended
for DOE-affiliated users and anyone who needs a large volume of data. See
`NERSC's account documentation <https://docs.nersc.gov/accounts/>`_ for how to
obtain an account.

**zstash archives.** Use ``zstash``, available in the
`E3SM-Unified <https://github.com/E3SM-Project/e3sm-unified>`_ conda
environment. To extract files locally on a NERSC machine: ::

   source /global/common/software/e3sm/anaconda_envs/load_latest_e3sm_unified_pm-cpu.sh
   zstash extract --hpss=<HPSS path in table>

To list the files in an archive without extracting: ::

   zstash ls --hpss=<HPSS path in table>

Patterns can be used to retrieve only a subset of files. For example, to
retrieve the monthly land output for years 0030--0049 of v2.LR.piControl: ::

   zstash extract --hpss=/home/projects/e3sm/www/WaterCycle/E3SMv2/LR/v2.LR.piControl "*.elm.h0.00[3-4]?-??.nc"

To transfer data to a machine other than NERSC, use the zstash Globus
interface from that machine: ::

   zstash extract --hpss=globus://nersc/<HPSS path in table>

or, equivalently, using the NERSC HPSS Globus endpoint UUID: ::

   zstash extract --hpss=globus://9cd89cfd-6d04-11e5-ba46-22000b92c6ec/<HPSS path in table>

For more information, refer to the
`zstash usage documentation <https://e3sm-project.github.io/zstash/_build/html/master/usage.html#extract>`_.

**Other archives.** Use the standard HPSS tools ``hsi`` and ``htar`` on a NERSC
machine, or transfer the files with Globus using the NERSC HPSS endpoint. For
example: ::

   hsi ls <HPSS path in table>
   hsi get <HPSS path in table>/<file>

See NERSC's
`HPSS documentation <https://docs.nersc.gov/filesystems/archive/#hsi-commands>`_
for details.

Without a NERSC account
-----------------------

Anyone can download world-readable HPSS data through the
`NERSC HPSS web portal <https://portal.nersc.gov/archive/home/projects/e3sm/www/>`_.
An HPSS path such as ``/home/projects/e3sm/www/<...>`` is available at
``https://portal.nersc.gov/archive/home/projects/e3sm/www/<...>``; the
**HPSS URL** column of the simulation tables provides these links directly.

Files are downloaded through the web browser (or a tool such as ``wget`` or
``curl``) one file at a time. Because the data must be staged from tape and
many archives are multiple terabytes, this can be **slow**. Downloading only
what you need is strongly recommended:

* For **zstash** archives, first download the ``index.db`` file and query it to
  find which tar files contain the data you need: ::

     sqlite3 index.db "SELECT tar,name,size from files;" > archive_contents.txt

* For archives that provide an ``archive_contents`` text file, check it first
  to identify the tar files you need.

.. _esgf-access:

ESGF
****

Simulations with an **ESGF Links** entry in the simulation table can be
downloaded from the `Earth System Grid Federation (ESGF) <https://aims2.llnl.gov/search>`_.
Neither a NERSC account nor an ESGF login is required to download data with a
wget script. ESGF has two kinds of E3SM data:

* **CMIP** -- a subset of the output, reformatted to CMIP conventions (CMOR'd)
  and published as part of CMIP6. The **CMIP** links in the tables open these
  datasets.
* **Native** -- native model output, as written by E3SM. Where available, the
  **Native** links in the tables open these datasets.

To download the data:

1. Click the **CMIP** or **Native** link in the simulation table. This opens
   the ESGF search page, filtered to that simulation's datasets.
2. Use the search facets (e.g., variable, frequency, realm) to narrow down to
   the datasets you need, and add them to the **Data Cart**.
3. From the Data Cart, download a **wget script** and run it on the machine
   where you want the data: ::

     bash wget-<...>.sh

   Alternatively, for data hosted at nodes that support it, you can start a
   **Globus** transfer from the Data Cart (this requires signing in to Globus).

For more information, see the `ESGF user documentation <https://esgf.github.io/esgf-user-support/user_guide.html>`_.

.. _globus-sharing:

Globus sharing
**************

.. note::
   Globus sharing is provided for high-usage datasets that are being actively
   analyzed. Currently, it is available for the
   :doc:`AI training datasets <AITraining/simulation_data/simulation_table>`.
   For other datasets, use :ref:`NERSC HPSS <nersc-hpss-access>` or
   :ref:`ESGF <esgf-access>`.

**Requirement: a Globus account.** Globus sharing requires a free
`Globus <https://www.globus.org/>`_ account. You can sign up at
`app.globus.org <https://app.globus.org/>`_ using your institution's login,
ORCID, or a Google account. A NERSC account is **not** required.

Shared datasets have a copy on the NERSC Community File System under a
``gsharing`` directory (for example,
``/global/cfs/cdirs/e3sm/gsharing/SamudrACE-E3SMv3``). These directories are
shared as read-only Globus guest collections on the **NERSC SHARE** collection
(see NERSC's `Sharing Data <https://docs.nersc.gov/filesystems/sharing/>`_
documentation).

Where a **Globus URL** is listed in a simulation table, that directory is
shared with all Globus users. If no Globus URL is listed, Globus access is not
available for that dataset; use :ref:`NERSC HPSS <nersc-hpss-access>` instead.

To transfer the data:

1. Click the **Globus URL** link in the simulation table and sign in with your
   Globus account. This opens the shared directory in the
   `Globus web app <https://app.globus.org/>`_ File Manager; the path ``/``
   is the top of the shared dataset directory.
2. In the other panel of the File Manager, choose the destination collection,
   e.g., your institution's data transfer node or your own computer running
   `Globus Connect Personal <https://www.globus.org/globus-connect-personal>`_.
3. Select the files or directories you want and click **Start** to begin the
   transfer. Globus runs the transfer in the background and emails you when it
   finishes.

NERSC users can also read these directories directly on Perlmutter at the
**Data on Disk** path. For more information, see NERSC's
`Globus documentation <https://docs.nersc.gov/services/globus/>`_.
