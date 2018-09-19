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
- Find maximum overlapping communities (similar community structures) from time-stamp ``t`` and ``t+1``

To read more about the architecture, please visit this [`Website <http://www.user.tu-berlin.de/hossainarif/>`_]

.. warning::
   This is a prototypical framework for detecting and observing community structures in blockchain networks. Built as a
   part of an academic project. Source code of the framework might contain bugs!

Test neochain installation
--------------------------
Test if ``neochain`` is properly installed or not

.. code-block:: python

   import neochain as nc
   nc.__version__

This should give an output with the version of the currently installed ``neochain`` package. Something similar like:

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

Creating merged graph
---------------------
A merged graph at time-stamp ``t+1`` from a sub-graph from time-stamp ``t`` and a graph from time-stamp ``t+1`` can be
obtained with the help of ``generate_merged_graph`` function.

.. code-block:: python

   merged_graph = nc.generate_merged_graph(input_dataset_t=dataset_t, input_dataset_t1=dataset_t1, weighted='yes', top_n_communities=top_n_communities_t.values())

.. note::
   Here ``input_data_set_t`` represents the entire data-set at time-stamp ``t`` and likewise ``input_data_set_t1``
   represents the entire data-set from timestamp ``t+1``. Creating sub-graph from top ``n`` communities is handled
   internally by this function.

Creating sub-graph
------------------
Although creating a sub-graph and merging with another graph can be done with ``generate_merged_graph`` function, creating
a sub-graph from top ``n`` communities at any given time-stamp is also possible.

.. code-block:: python

   sub_graph_df = nc.find_sub_graph(input_file=dataset_t, weighted='yes', top_n_communities_t=top_n_communities_t.values())

Find maximum overlap
--------------------
Overlapping communities tends to be similar to each other. Maximum overlap can be measured between two community structures
by measuring the similarity.

.. code-block:: python

   similarity = nc.find_relative_overlap(top_n_communities_t, top_n_communities_t1)

``find_relative_overlap`` will return a list of most similar pairs of communities with the value of similarity measure.
Execution result of the above source code segment might look like following:

.. code-block:: python

   [(1, 2, 0.7267641315247797), (2, 3, 0.35002051702913417)]

First tuple of this output list represents that community ``1`` from time-stamp ``t`` is similar to community ``2`` from
time-stamp ``t+1``.

.. note::
   This framework uses ``jaccard similarity`` measure by default. Other similarity measures like ``cosine similarity``,
   ``euclidean distance similarity``, ``manhattan distance similarity`` and ``minkowski distance similarity`` can also
   be used simply by invoking appropriate similarity measure.

Preferred similarity measures can be invoked by defining ``similarity_measure`` keyword in the argument list. Available
keywords are: ``jaccard``, ``cosine``, ``euclidean``, ``manhattan`` and ``minkowski``.

.. code-block:: python
      similarity = nc.find_relative_overlap(top_n_communities_t, top_n_communities_t1, similarity_measure='cosine')

