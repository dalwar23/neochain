#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

# Import python libraries
import os
import sys
import datetime
from itertools import islice
from math import *
from decimal import Decimal

# Import custom python libraries
try:
    from pyrainbowterm import *
except ImportError:
    print('Can not import pyrainbowterm!', log_type='error')
    print('Try: pip install pyrainbowterm', log_type='hint')
    sys.exit(1)


# Source code meta data
__author__ = 'Dalwar Hossain'
__email__ = 'dalwar.hossain@protonmail.com'


# Check input file permissions
def check_input_file_permissions(input_file):
    """
    This function check permissions for the input file
    :param input_file: Input file path
    :return: input file, status of the file (OK/NOT OK) for reading
    """
    # Check input file's status (is a file?, has right permissions?)
    print('Checking input file status.....', log_type='info')
    if os.access(input_file, os.F_OK):
        print('Input file found!', log_type='info')
        if os.access(input_file, os.R_OK):
            print('Input file has read permission!', log_type='info')
            permission_status = 1
        else:
            print('Input file does not has read permission!', log_type='error')
            permission_status = 0
    else:
        print('Input file not found!', log_type='error')
        permission_status = 0

    # Return
    return permission_status


# Check if the file has header or not
def file_sniffer(input_file=None):
    """
    This function checks if the first line of the file is a header or not
    :param input_file: Input file path
    :return: detected delimiter, headers (if available), number of columns, skip rows
    """
    try:
        import csv
    except ImportError:
        print('Can not import python csv library!', log_type='error')
        sys.exit(1)

    # Open the file and take a sniff
    with open(input_file) as f:
        first_five_lines = list(islice(f, 5))
        file_head = ''.join(map(str, first_five_lines))
        try:
            dialect = csv.Sniffer().sniff(file_head)
            _headers = csv.Sniffer().has_header(file_head)
            delimiter = dialect.delimiter
        except Exception as e:
            print('Can not detect delimiter or headers! ERROR: {}'.format(e), log_type='error')
            print('Please check input file!!', log_type='error')
        # Sniff into the file and see if there is a header or not
        if _headers:
            headers = file_head.split('\n')[0].split(delimiter)
            n_cols = len(headers)
            skip_rows = 1
        else:
            headers = None
            n_cols = len(file_head.split('\n')[0].split(delimiter))
            skip_rows = 0

    # Return
    return delimiter, headers, n_cols, skip_rows


# Check File Header
def check_file_header(headers=None):
    """
    This file checks if the file header is active or commented
    Limitation: Checks only First line of the file
    --------------------------------------
    =================
    == Attention!! ==
    =================
    File with header => 0
    File without/commented header=> 1
    --------------------------------------
    :param headers: File headers with column names
    :return: <>
    """
    if headers:
        print('Headers detected in input file!', log_type='warn')
        if headers[0].startswith('#'):
            print('Found commented header in input file!', log_type='info')
            header_status = 1
        else:
            header_status = 0
            print('Please comment [#] or delete header from input file!', log_type='warn')
    else:
        print('No headers detected in input file!', log_type='info')
        header_status = 1

    # Return header status
    return header_status


# Check Delimiter
def check_delimiter(detected_delimiter=None, provided_delimiter=None):
    """
    This function checks match between provided and detected delimiter
    ----------------------------------------------------------
    =================
    == Attention!! ==
    =================
    detected delimiter and provided delimiter - match => 1
    detected delimiter and provided delimiter - mismatch => 2
    -----------------------------------------------------------
    :param detected_delimiter: Delimiter that is detected from the input file
    :param provided_delimiter: Delimiter that was provided
    :return: <>
    """
    print('Provided delimiter: "{}"'.format(provided_delimiter), log_type='info')
    print('Detected delimiter: "{}"'.format(detected_delimiter), log_type='info')

    if detected_delimiter is ' ' and provided_delimiter is None:
        print('Delimiter converted to whitespace!', log_type='hint')
        delimiter_status = 1
    elif detected_delimiter != provided_delimiter:
        delimiter_status = 2
        print('Delimiter mismatch!', log_type='warn', color='orange')
    elif detected_delimiter == provided_delimiter:
        delimiter_status = 1

    # Return
    return delimiter_status


# Check Columns
def check_columns(n_cols=None, weighted=None):
    """
    This function checks the number of columns detected from the input file
    also checks that it matches with the weighted argument. For example:
    A normal unweighted graph will have two column and weighted graph will have
    three columns.
    ------------------------------------
    =================
    == Attention!! ==
    =================
    If weighted and column == 3 =>1
    else => 0
    If unweighted and column == 2 => 1
    else => 0
    -------------------------------------
    :param n_cols: Number of columns detected from the input file
    :param weighted: Is the weighted argument provided yes or no
    :return: <>
    """
    # Check the number of columns in the file
    print('Detected columns: {}'.format(n_cols), log_type='info')
    weight_col = is_weighted(weighted)
    if weight_col:
        if n_cols == 3:
            column_status = 1
        else:
            print('Number of expected columns does not match', log_type='warn', color='orange')
            column_status = 0
    else:
        if n_cols == 2:
            column_status = 1
        else:
            print('Number of expected columns does not match', log_type='warn', color='orange')
            column_status = 0

    # Return
    return column_status


# Get data value for networkx graph (data = True) in read_edgelist()
def is_weighted(weighted=None):
    """
    Gets the data value for networkx graph
    :param weighted: yes/no boolean
    :return: data value for networkx graph
    """
    # Assign data based on weighted or not
    if weighted == "yes" or weighted == "Yes" or weighted == "Y" or weighted == "y":
        data_ = True
    elif weighted == "no" or weighted == "No" or weighted == "N" or weighted == "n":
        data_ = False
    else:
        print('Please provide weighted argument with yes/no, y/n, Yes/No', log_type='error')
        sys.exit(1)

    # Return
    return data_


# Generate appropriate sanity check status code
def generate_sanity_status(input_file_status=None, header_status=None, delimiter_status=None, column_status=None):
    """
    This function creates sanity check status codes
    :param input_file_status:
    :param header_status:
    :param delimiter_status:
    :param column_status:
    :return: (int) status_code
    """
    status_code = 1
    print('Sanity check.....', log_type='info', end='')
    print('COMPLETE', color='green')
    print('--------------- Summary -------------------')

    # Input file
    if input_file_status:
        print('Input file.....', log_type='info', end='')
        if input_file_status == 1:
            print('OK', color='green')
            status_code = status_code and 1
        elif input_file_status == 0:
            print('NOT OK', color='red')
            status_code = status_code and 0

    # Header
    print('Headers.....', log_type='info', end='')
    if header_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif header_status == 0:
        print('NOT OK', color='red')
        status_code = status_code and 0

    # Delimiter
    print('Delimiter.....', log_type='info', end='')
    if delimiter_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif delimiter_status == 2:
        print('[!] OK', color='orange')
        print('Program might not detect nodes if input file does not have default (whitespace) delimiter',
              log_type='warn', color='orange')
        status_code = status_code and 1

    # Columns
    print('Columns.....', log_type='info', end='')
    if column_status == 1:
        print('OK', color='green')
        status_code = status_code and 1
    elif column_status == 0:
        print('NOT OK', color='red')
        status_code = status_code and 0

    print('-------------------------------------------')

    # Return
    return status_code


# Sanity Check for file operations
def sanity_check(input_file=None, delimiter=None, weighted=None):
    """
    This function checks the sanity of the input and returns a status with file is weighted or not
    :param input_file: Input file full path
    :param delimiter: Column separator in the input file
    :param weighted: Does the file contain edge weights or not
    :return: sanity status
    """
    # Get file information (Header, delimiter, number of columns etc.)
    detected_delimiter, headers, n_cols, skip_n_rows = file_sniffer(input_file)

    # Input file?
    input_file_status = check_input_file_permissions(input_file)

    # Header?
    header_status = check_file_header(headers)

    # Delimiter?
    delimiter_status = check_delimiter(detected_delimiter, delimiter)

    # Number of columns?
    column_status = check_columns(n_cols, weighted)

    # Generate sanity status
    sanity_status = generate_sanity_status(input_file_status, header_status, delimiter_status, column_status)

    # Return
    return sanity_status


# Create initial message
def initial_message(script=None, algorithm=None):
    """
    This function creates initial message
    :param script: name of the script that will show the message
    :param algorithm: name of the algorithm of that particular script
    :return: <>
    """
    # Print a general help message
    date_time = datetime.datetime.now()
    print_string = "Network analysis and community detection with " + algorithm
    print_string += " [ " + date_time.strftime("%d-%B-%Y %H:%M:%S") + " ]"
    print('=' * len(print_string), print_string, "Need help?: python {} -h/--help".format(script),
          '=' * len(print_string), sep='\n')


# Create initial message
def initial_message(script=None, custom_message=None):
    """
    This function creates initial message and prints it
    """
    marker = '-'  # Must be single character
    # Print a general help message
    date_time = datetime.datetime.now()
    _print_string = "Column based text filtering and processing"
    _print_string += " [ " + date_time.strftime("%d-%B-%Y %H:%M:%S") + " ]"
    # Help message display
    _help_string = "Need help?: python {} -h/--help".format(script)
    # Create prefix and suffix
    prefix = marker * 2 + ' '
    suffix = ' ' + marker * 2
    print_string = prefix + _print_string
    custom_message = prefix + custom_message
    help_string = prefix + _help_string
    # Take max
    str_length = max([len(print_string), len(custom_message), len(help_string)]) + 3
    # Create padding
    print_string = print_string + " " * (str_length - len(print_string) - len(suffix)) + suffix
    custom_message = custom_message + " " * (str_length - len(custom_message) - len(suffix)) + suffix
    help_string = help_string + " " * (str_length - len(help_string) - len(suffix)) + suffix
    # Print
    line_block = marker * str_length
    print(line_block, print_string, custom_message, help_string, line_block, sep='\n')


# Get directory path for input/output data
def get_dir_path(input_file=None):
    """
    This function extracts the directory path of input file and creates a new file name for the output file
    :param input_file: A complete file path for input dataset
    :return: A directory path and a file name
    """
    # Get input file's directory
    input_dir = os.path.dirname(input_file)
    if os.path.isdir(input_dir):
        output_dir = input_dir
    else:
        print('Can not determine output directory!', log_type='error')
        sys.exit(1)

    # Return output path
    return output_dir


# Generate output file name
def generate_output_filename(input_file=None, prefix=None):
    """
    This function generates appropriate output file name
    :param input_file: A file path to input file
    :param prefix: Prefix of output file
    :return: output filename full path
    """
    splitter = '_'
    # Get file name
    input_file_name = os.path.basename(input_file)
    # Create new file name
    base_file_name, base_file_extension = os.path.splitext(input_file_name)
    output_file_name = prefix + splitter + base_file_name + base_file_extension

    # Get output directory
    output_directory = get_dir_path(input_file)

    # Output file full path
    output_file = os.path.join(output_directory, output_file_name)

    # Return
    return output_file


# Create a community file as output file
def create_community_file(dict_communities=None, output_file=None):
    """
    This function creates the output file
    :param dict_communities: A python dictionary with communities assigned to nodes
    :param output_file: name and location of the output files (.grp) and (.pkl)
    :return: <> file object <>
    """
    # Create pickled extension for saving data for further use
    pickled_file = output_file.rsplit('.', 1)[0] + '.pkl'

    # Create community extension for saving communities
    community_file = output_file.rsplit('.', 1)[0] + '.grp'

    # Put the dictionary data in a pickled jar for later use
    if sys.version_info[0] == 2:
        import cPickle as pickle
    if sys.version_info[0] == 3:
        import pickle

    try:
        print('Creating pickled jar of (.pkl) data.....', log_type='info')
        with open(pickled_file, 'w') as pickled_file:
            pickle.dump(dict_communities, pickled_file)
    except Exception as e:
        print('Can not create pickled data!!! ERROR: {}'.format(e), log_type='error')

    # import json
    #
    # communities = json.dumps(dict_communities, sort_keys=True, indent=4)
    #
    # print('Creating community file.....', log_type='info')
    # with open(output_file, 'w') as f:
    #     f.write(communities)

    # Import pandas
    try:
        import pandas as pd
    except ImportError as e:
        print('Can not import python pandas library! ERROR: {}'.format(e), log_type='error')
        sys.exit(1)

    # Create a pandas data frame from the dictionary
    communities = pd.DataFrame(dict_communities.items(), columns=['node', 'cluster'], dtype=int)

    # Generate list of nodes that belongs to same community
    groups = communities.groupby('cluster')['node'].apply(list)

    # Write to output file
    try:
        print('Creating community (.grp) file.....', log_type='info')
        groups.to_csv(community_file, header=False)
    except Exception as e:
        print('Can not create output file! ERROR: {}'.format(e), log_type='error')
        sys.exit(1)


# Get python dictionay
def __get_dict(data=None):
    """
    This function creates python dictionary from an iterator

    :param data: An iterator
    :return: (python dict) A python dictionary
    """
    # Create dictionary and use integer values as keys
    _dict = {}
    _id = 1
    for item in data:
        _dict[_id] = item
        _id += 1

    # Return
    return _dict


# Find jaccard similarity
def __jaccard_similarity(set_a=None, set_b=None):
    """
    This function calculates jaccard similarity

    :param set_a: (list) Python list of items
    :param set_b: (list) Python list of second items
    :return: (float) jaccard similarity between set_a and set_b
    """
    # Assign
    x = set_a
    y = set_b
    # Calculate
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    # Return
    return intersection_cardinality / float(union_cardinality)


# Find cosine similarity
def __cosine_similarity(set_a=None, set_b=None):
    """
    This function calculates cosine similarity

    :param set_a: (list) Python list of items
    :param set_b: (list) Python list of second items
    :return: (float) cosine similarity between set_a and set_b
    """
    # Find square root
    def square_rooted(value):
        """
        This function finds the square root of a value
        :param value: (int) An integer
        :return: (float) square root of 'value'
        """
        return round(sqrt(sum([a * a for a in value])), 6)  # Rounded upto 6 decimal point

    # Assign
    x = set_a
    y = set_b
    # Calculate
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)

    # Return
    return round(numerator / float(denominator), 6)  # Rounded upto 6 decimal point


# Find euclidean distance similarity
def __euclidean_distance_similarity(set_a=None, set_b=None):
    """
    This function calculates euclidean distance similarity

    :param set_a: (list) Python list of items
    :param set_b: (list) Python list of second items
    :return: (float) euclidean distance similarity between set_a and set_b
    """
    # Assign
    x = set_a
    y = set_b

    # Calculate &
    # Return
    return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


# Find manhattan distance similarity
def __manhattan_distance_similarity(set_a=None, set_b=None):
    """
    This function measures manhattan distance similarity

    :param set_a: (list) Python list of items
    :param set_b: (list) Python list of second items
    :return: (int / float) manhattan distance similarity between set_a and set_b
    """
    # Assign
    x = set_a
    y = set_b

    # Calculate &
    # Return
    return sum(abs(a - b) for a, b in zip(x, y))


# Find minkowski distance similarity
def __minkowski_distance_similarity(set_a=None, set_b=None):
    """
    This function calculates minkowski distance similarity

    :param set_a: (list) Python list of items
    :param set_b: (list) Python list of second items
    :return: (int / float) minkowski distance similarity between set_a and set_b
    """
    # Assign
    x = set_a
    y = set_b
    p_value = 3

    # Calculate
    def nth_root(value, n_root):
        """
        This function calculates the nth_root
        :param value: (int) the number of which nth root to be taken of
        :param n_root: (int) number of degree that root is being taken [default: 3]
        :return: (float) nth_root
        """
        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 6)  # Rounded up to 6 decimal point

    # Return
    return nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)
