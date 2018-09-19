Tutorials
=========
This tutorial is designed to help getting started with the ``neochain`` package

NEOChain Framework Architecture
-------------------------------
NEOChain is designed to detect communities in large-scale transaction-based network specially from distributed ledger or
``Blockchain``. This ``python`` package is designed as an implementation of the following framework architecture called
``NEOChain`` (Network Evolution Observation for Blockchain):

- Find top ``n`` communities at time-stamp ``t``
- Generate sub-graphs form top ``n`` communities at time-stamp ``t``
- Merge sub-graph from time-stamp ``t`` with the graph from time-stamp ``t+1``
- Find top ``n`` communities from merged graph
- Find maximum overlapping communities from time-stamp ``t`` and ``t+1``

.. warning::
   This is a prototypical framework for detecting and observing community structures in blockchain networks. Built as a
   part of an academic project. Source code of the framework might contain bugs!

Test ``neochain``
-----------------
Test if ``neochain`` is properly installed or not

.. code-block:: python

   import neochain as nc
   nc.__version__

This should give an output with the version of the currently installed ``neochain`` package

.. code-block:: python

   1.1

If ``neochain`` is not installed properly, system should give an ``ERROR`` message.

Finding communities
-------------------
Detect all community structures in a graph at time stamp ``t``

.. code-block:: python

   import neochain as nc
   all_communities_t = nc.find_communities(dataset_t, weighted='yes')

This will all the detected communities in the entire graph.

Find top ``n`` communities
--------------------------
Once all communities are detected ant any time-stamp, selection of top ``n`` communities according to their size
(community with more member nodes is bigger in size), can be done as following:

For time-stamp ``t``

.. code-block:: python

   top_n_communities_t = nc.find_top_n_communities(all_communities=all_communities_t, n=25)

For time-stamp ``t+1``

.. code-block:: python

   top_n_communities_t1 = nc.find_top_n_communities(all_communities=all_communities_t1, n=25)

.. note::
   The number (integer) of top ``n`` communities MUST be the same in both the time-stamps, that are in the context.

Creating sub-graph
------------------
