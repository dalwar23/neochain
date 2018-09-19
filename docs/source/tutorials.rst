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

Finding communities
-------------------
