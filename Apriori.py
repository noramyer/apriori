import argparse
import numpy as np
from collections import namedtuple
from node_class import Node

#Author: Nora Myer
#Date: 3/26/19

args = ""

#Sets up and reads in args based in from the command line
def parse_data_file_args():
    global args

    #set arg labels
    args_labels = ["-database_file", "-minsupp", "-output_file"]
    parser = argparse.ArgumentParser()

    #build the parser with labels
    for arg in args_labels:
        parser.add_argument(arg)

    #set global args
    args = parser.parse_args()

#Read in database from args input file
def read_database():
    return None

def apriori(database, minsupp, output_file):
    return None

def generate_F1():
    return None

def generate_candidate():
    return None

def prune_candidate():
    return None

def count_support():
    return None

def output_freq_itemsets():
    return None

def main():
    parse_data_file_args()


if __name__ == "__main__":
    main()
