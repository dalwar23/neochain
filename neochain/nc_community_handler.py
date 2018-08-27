#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import datetime
from pyrainbowterm import *
import heapq

# Import custom libraries
from infomap import infomap
import networkx as nx
import community
import pandas as pd

# Import custom libraries
import _operations


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Compose graph with networkx library
# @profile  # Uncomment to profile this function for memory usage with 'mprof'
def __compose_ntx_graph(input_file=None, delimiter=None, weighted=None):
    """
    This function creates a networkx graph from provided file

    :param input_file: Input file path
    :param delimiter: separator for the column of the input file
    :param weighted: Simple yes/no if the input file is weighted or not
    :return: networkx graph
    """
    # Get data for weighted networkx graph
    file_is_weighted = _operations.is_weighted(weighted)

    if file_is_weighted:
        print('Creating Networkx weighted graph.....', log_type='info')
        try:
            ntx_graph = nx.read_weighted_edgelist(input_file, delimiter=delimiter, nodetype=int)
        except Exception as e:
            print('Can not create weighted networkx graph. ERROR: {}'.format(e), color='red', log_type='error')
            sys.exit(1)
    else:
        print('Creating Networkx unweighted graph.....', log_type='info')
        try:
            ntx_graph = nx.read_edgelist(input_file, delimiter=delimiter, nodetype=int)
        except Exception as e:
            print('Can not create unweighted networkx graph. ERROR: {}'.format(e), color='red', log_type='error')
            sys.exit(1)

    # Return graph
    return ntx_graph


# Run louvain method algorithm for community detection
def __run_louvain(ntx_graph=None):
    """
    This function runs louvain method algorithm

    :param ntx_graph: (Graph) A networkx graph
    :return: (dict) Python dictionary of nodes and communities
    """
    print('Finding communities with louvain method.....', log_type='info')
    try:
        start_time = datetime.datetime.now()
        print('Louvain method started at: {}'.format(start_time.strftime("%H:%M:%S")), log_type='info')
        louvain_communities = community.best_partition(ntx_graph)
        elapsed_time = datetime.datetime.now() - start_time
        print('Elapsed time: ', log_type='info', end='')
        print('{}'.format(elapsed_time), color='cyan', text_format='bold')
    except Exception as e:
        print('Can not detect communities with louvain method! ERROR: {}'.format(e))
        sys.exit(1)

    # Return
    return louvain_communities


# Run infomap algorithm for community detection
def __run_infomap(input_file=None, options=None):
    """
    This function runs infomap algorithm

    :param input_file: (string) input file path, default [.txt]
    :return: (dict) python dictionary of nodes and communities
    """
    # Options for Infomap class
    options += ' --two-level -z'
    print('Using options: {}'.format(options), log_type='info')
    infomap_wrapper = infomap.Infomap(options)

    # Build infomap network from input file
    print('Building Infomap network from the input file.....', log_type='info')
    infomap_wrapper.readInputData(input_file)

    # Run infomap
    print("Finding communities with Infomap.....", log_type='info')
    infomap_wrapper.run()
    # Create tree from infomap_wrapper
    tree = infomap_wrapper.tree
    print("Found {} modules with code length: {}".format(tree.numTopModules(), tree.codelength()), log_type='info')

    # Find communities
    infomap_communities = {}
    for node in tree.leafIter():
        infomap_communities[node.originalLeafIndex] = node.moduleIndex()

    # Return
    return infomap_communities


# Find communities
def find_communities(input_file=None, delimiter=None, weighted=None, algorithm=None, **kwargs):
    """
    This function finds community structure using defined algorithm

    :param input_file: (string) Input dataset for community detection, default [.txt]
    :param delimiter: (string) Column separator for input file, default [whitespace]
    :param weighted: (boolean) yes/no. Is the input file has a weight column?, default [no]
    :param algorithm: (string) Community detection algorithm, default [infomap]
    :return: (dict) Python dictionary of nodes and communities
    """
    if input_file:
        # Check for algorithm
        if algorithm is None:
            print('No algorithm specified! Using default [infomap].....', log_type='info')
            algorithm = 'infomap'
        else:
            algorithm = algorithm

        # Check for delimiter
        if delimiter is None:
            print('No delimiter provided! Using default [whitespace].....', log_type='info')
            delimiter = None
        else:
            delimiter = delimiter

        # Check weighted
        if weighted is None:
            print('No weighted parameter provided! Using default [no].....', log_type='info')
            weighted = 'No'
        else:
            weighted = weighted

        # Run sanity check once again
        sanity_status = _operations.sanity_check(input_file=input_file, delimiter=delimiter, weighted=weighted)

        # Run algorithm
        if sanity_status == 1:
            print('Initializing [{}] algorithm.....'.format(algorithm), log_type='info')
            if algorithm == 'infomap':
                # get options from kwargs
                if 'options' in kwargs:
                    infomap_options = kwargs['options']
                else:
                    infomap_options = ''
                # Run infomap algorithm
                all_communities = __run_infomap(input_file=input_file, options=infomap_options)

            elif algorithm == 'louvain':
                # Create networkx graph from input data
                input_graph = __compose_ntx_graph(input_file=input_file, delimiter=delimiter, weighted=weighted)
                all_communities = __run_louvain(ntx_graph=input_graph)

            else:
                print('Unknown algorithm name provided! Currently supports: infomap, louvain',
                      log_type='error', color='red')
                sys.exit(1)

            # Return all_communities that are detected
            return all_communities

        else:
            print('Sanity check failed!', log_type='error', color='red')
            sys.exit(1)

    else:
        print('Invalid parameters! Check input!!', log_type='error', color='red')
        sys.exit(1)


# Find top 'n' communities
def find_top_n_communities(all_communities=None, n=None):
    """
    This function finds the top 'n' communities from a python dictionary of nodes and communities

    :param all_communities: (dict) A python dictionary of nodes and communities
    :param n: (int) number of top community to be selected
    :return: (list) of top 'n' communities ([[list of member nodes]])
    """
    # Create a Pandas data frame from dict to run group by
    communities_df = pd.DataFrame(all_communities.items(), columns=['node', 'cluster'], dtype=int)

    # Group nodes by community
    node_groups = communities_df.groupby('cluster')['node'].apply(list)

    # Find top (e.g. n=10) communities based on number of nodes in the community
    # heapq.nlargest(n, iterable, [key]) is equivalent to
    # sorted(flat_comm_list, key=len, reverse=True)[:10]
    top_n_communities = heapq.nlargest(n, node_groups, key=len)

    # Return
    return top_n_communities


# Find similarity between communities
def find_relative_overlap(communities_t=None, communities_t1=None):
    """
    This function calculates relative overlap of communities

    :param communities_t: (python list) Top 'n' communities at time 't'
    :param communities_t1: (python list) Top 'n' communities at time 't+1'
    :return: (python list) list of pairs of communities
    """
    pass
