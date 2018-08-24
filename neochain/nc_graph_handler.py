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
        df_t = pd.read_csv(input_file, delimiter=delimiter, names=headers, comment='#', skipinitialspace=True)
    except Exception as e:
        print('Can not read input data! ERROR: {}'.format(e), log_type='error', color='red')
        sys.exit(1)

    # Return
    return df_t


# Create a function for sub-graph
def __find_sub_graph(data_frame_t=None, top_n_communities_t=None):
    """
    This function creates a subset of links/edges from the main input file depending on the nodes from
    top 'n' communities
    :param data_frame_t: (pandas data frame) A pandas data frame with data from time 't'
    :param top_n_communities_t: (list) List of communities containing the member nodes
    :return: (pandas data frame) a data frame of edges that contains all the nodes from top 'n' communities that
    are present in input file
    """

    # Assign short name
    df_t = data_frame_t

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

    :param input_dataset_t: (string) A file path to input data at time 't'
    :param input_dataset_t1: (string) A file path to input data at time 't+1'
    :param delimiter: (string) Column separator in both input files, default [whitespace] [MUST BE SAME FOR BOTH FILE]
    :param weighted: (boolean) yes/no, if files have weight column or not [NUMBER OF COLUMN MUST BE SAME IN BOTH FILES]
    :param top_n_communities: (list) List of communities containing the member nodes
    :return: (pandas data frame) A data frame with links form sub graph at time 't' and links from graph at time 't+1'
    """
    # Step 2(a)
    # Read data set from time 't'
    graph_df_t = __read_data(input_file=input_dataset_t, weighted=weighted, delimiter=delimiter)

    # Get the sub graph from data set at time 't'
    sub_graph_t = __find_sub_graph(data_frame_t=graph_df_t, top_n_communities_t=top_n_communities)

    # Step 2(b)
    # Read data set from time 't+1
    graph_df_t1 = __read_data(input_file=input_dataset_t1, weighted=weighted, delimiter=delimiter)

    # Creating a merged graph [G(t,t1)]
    frames = [sub_graph_t, graph_df_t1]
    merged_graph_tt1 = pd.concat(frames)

    # Return
    return merged_graph_tt1
