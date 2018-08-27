#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import sys
import itertools
from pyrainbowterm import *
import pandas as pd

# Import custom libraries
import _operations


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Read data as pandas data frame
def __read_data(input_file=None, weighted=None, delimiter=None):
    """
    This function uses pandas read_csv to read data and return pandas data frame

    :param input_file: (string) A path to input file that is being read
    :param weighted: (boolean) yes/no, if the input file has weight column or not
    :param delimiter: (string) Columns separator in the input file
    :return: (pandas data frame) a data frame read from input file
    """
    # Although checking weighted values is required
    weighted = _operations.is_weighted(weighted)
    if weighted:
        headers = ['source', 'target', 'weight']
    else:
        headers = ['source', 'target']

    # Also the delimiter is required to be checked
    if delimiter is None:
        print('No delimiter provided! Using default [whitespace].....', log_type='info')
        delimiter = ' '
    else:
        delimiter = delimiter

    # Read data
    print('Reading input data.....', log_type='info')
    try:
        graph_df = pd.read_csv(input_file, delimiter=delimiter, names=headers, comment='#', skipinitialspace=True)
    except Exception as e:
        print('Can not read input data! ERROR: {}'.format(e), log_type='error', color='red')
        sys.exit(1)

    # Return
    return graph_df


# Create a function for sub-graph
def find_sub_graph(input_file=None, weighted=None, delimiter=None, top_n_communities_t=None):
    """
    This function creates a subset of links/edges from the input file depending on the nodes from top 'n' communities

    :param input_file: (string) A file path to input data at time 't'
    :param delimiter: (string) Column separator in both input files, default [whitespace]
    :param weighted: (boolean) yes/no, if files have weight column or not
    :param top_n_communities_t: (list) List of communities containing the member nodes
    :return: (pandas data frame) a data frame of edges that contains all the nodes from top 'n' communities
    """

    # Read data set from time 't'
    graph_df_t = __read_data(input_file=input_file, weighted=weighted, delimiter=delimiter)
    print('Time (t) graph size: {}'.format(len(graph_df_t.index)), log_type='info')

    # Assign short name
    df_t = graph_df_t

    # Select unique nodes from top 'n' communities
    comm_nodes = list(itertools.chain.from_iterable(top_n_communities_t))
    comm_unique_nodes = pd.unique(pd.Series(comm_nodes))

    # Generate sub data frame from data frame at time 't' with nodes from top 'n' communities
    print('Creating sub graph.....', log_type='info')
    sub_graph_t = df_t[(df_t.source.isin(comm_unique_nodes)) | (df_t.target.isin(comm_unique_nodes))]
    print('Sub graph creation complete!', log_type='info')

    # Return
    return sub_graph_t


# Generate a concatenated graph from sub_graph from time 't' and a graph snapshot from time 't1'
def generate_merged_graph(input_dataset_t=None, input_dataset_t1=None, delimiter=None, weighted=None,
                          top_n_communities=None):
    """
    This function creates a merged graph data from sub-graph at time 't' and a graph snapshot from time 't+1"

    :param input_dataset_t: (string) A file path to input data at time 't'
    :param input_dataset_t1: (string) A file path to input data at time 't+1'
    :param delimiter: (string) Column separator in both input files, default [whitespace]
    :param weighted: (boolean) yes/no, if files have weight column or not
    :param top_n_communities: (list) List of communities containing the member nodes
    :return: (pandas data frame) A data frame with links form sub graph at time 't' and links from graph at time 't+1'
    """
    # Step 2(a)
    # Get the sub graph from data set at time 't'
    sub_graph_t = find_sub_graph(input_file=input_dataset_t, weighted=weighted, delimiter=delimiter,
                                 top_n_communities_t=top_n_communities)
    print('Time (t) sub-graph size: {}'.format(len(sub_graph_t.index)), log_type='info')

    # Step 2(b)
    # Read data set from time 't+1
    graph_df_t1 = __read_data(input_file=input_dataset_t1, weighted=weighted, delimiter=delimiter)
    print('Time (t1) graph size: {}'.format(len(graph_df_t1.index)), log_type='info')

    # Creating a merged graph [G(t,t1)]
    print('Creating merged graph.....', log_type='info')
    frames = [sub_graph_t, graph_df_t1]
    merged_graph_tt1 = pd.concat(frames)
    print('Merged graph creation complete!', log_type='info')

    # Return
    return merged_graph_tt1
