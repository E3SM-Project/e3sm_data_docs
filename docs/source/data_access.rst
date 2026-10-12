.. _data-access:

Accessing E3SM Data
===================

This page describes how E3SM archives released simulation output and how to
retrieve it. Each dataset page links to a table of simulations; this page
explains how to use the paths and links in those tables.

How E3SM data is archived
*************************

E3SM simulation output is released through one or both of the following:

* **ESGF** -- Data reformatted to CMIP conventions (and, for some campaigns,
  native model output) is published to the
  `Earth System Grid Federation (ESGF) <https://aims2.llnl.gov/search>`_.
  When an ESGF link is listed in a simulation table, ESGF is the preferred
  retrieval method.

* **NERSC HPSS** -- Native model output is archived on the
  `NERSC HPSS <https://docs.nersc.gov/filesystems/archive/>`_ tape system in
  directories with world-read permissions (under ``/home/projects/e3sm/www/``
  or a user's ``www`` directory). Because the files are world-readable, they
  can be retrieved either by NERSC users with the standard HPSS tools, or by
  anyone through the NERSC HPSS web portal.

  Most campaign output is archived with `zstash <https://e3sm-project.github.io/zstash>`_,
  which stores files in a series of tar files together with an ``index.db``
  database listing their contents. Some datasets (e.g., the AI training
  datasets) instead provide an ``archive_contents`` text file listing the files
  in each tar archive.

Each simulation table lists the **HPSS path** of each simulation and, where
available, an **HPSS URL** to the corresponding web portal page.

.. note::
   Some tables also list a **Data on Disk** path on the NERSC Community File
   System (CFS), with a **Globus URL** for transferring it (see
   :ref:`globus-sharing`). Because the data is already on disk, this is usually
   much faster than retrieving it from tape. These disk copies are **not
   guaranteed to persist** -- the HPSS archive is the authoritative long-term
   copy.

Option 1: Users with a NERSC account
************************************

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

Option 2: Users without a NERSC account
***************************************

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

.. _globus-sharing:

Option 3: Globus sharing of on-disk copies
******************************************

Some datasets (e.g., the AI training datasets) also have a copy on the NERSC
Community File System under a ``gsharing`` directory (for example,
``/global/cfs/cdirs/m4492/gsharing/e3sm-v2-climsst-180x360-gaussian``). These
directories are shared through `Globus <https://www.globus.org/>`_ guest
collections, so **a NERSC account is not required** -- only a free Globus
account. You can sign in to Globus with your institution's login, ORCID, or a
Google account.

To transfer the data:

1. Click the **Globus URL** link in the simulation table. This opens the shared
   directory in the `Globus web app <https://app.globus.org/>`_ (sign in if
   prompted).
2. In the other panel of the File Manager, choose the destination collection,
   e.g., your institution's data transfer node or your own computer running
   `Globus Connect Personal <https://www.globus.org/globus-connect-personal>`_.
3. Select the files or directories you want and click **Start** to begin the
   transfer. Globus runs the transfer in the background and emails you when it
   finishes.

NERSC users can also read these directories directly on Perlmutter at the
**Data on Disk** path. For more information, see NERSC's
`Globus documentation <https://docs.nersc.gov/services/globus/>`_.

Run scripts
***********

Where available, the scripts originally used to run each simulation campaign
are archived in the
`run_scripts <https://github.com/E3SM-Project/e3sm_data_docs/tree/main/run_scripts>`_
directory of this repository, and are linked from each dataset page. Original
run scripts **will not run out-of-the-box**; they are provided as guidance for
setting up a similar run. For some campaigns (e.g., E3SMv2), separate
reproduction scripts are also provided.
