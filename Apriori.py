import argparse
import numpy as np
import pandas as pd

#Author: Nora Myer
#Date: 3/26/19

args = ""
columns = {}
num_transactions = 0
num_items = 0

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
    global num_transactions
    global num_items
    global columns

    with open(str(args.database_file)) as f:
        content = f.readlines()

    num_transactions = int(content[0].split()[0])
    num_items = int(content[0].split()[1])
    matrix = np.zeros((num_transactions, num_items))

    for i in range(1, num_transactions):
        row = map(int, content[i].split())
        for j in range(len(row)):
            if not row[j] in columns:
                columns[row[j]] = set()

            columns[row[j]].add(i-1)
            matrix[i-1][row[j]] = 1

    return matrix

def apriori(database, minsupp, output_file):
    fk = []
    fk_itemsets = []
    k = 1
    fk = generate_F1(minsupp)

    while len(fk) > 0:
        lk1 = generate_candidate(fk)
        lk1 = prune_candidate(database, lk1, minsupp)
        count_vector = count_support(lk1)
        eliminate_candidate(count_vector, lk1)
        k+=1

    output_freq_itemsets()

    return None

def generate_F1(minsupp):
    f1 = set()
    for key in columns:
        if float(len(columns[key]))/num_transactions > minsupp:
            fr = frozenset([key])
            f1.add(fr)

    return f1

#fk-1 x fk-1 generation method
def generate_candidate(fk):
    Lk1 = set()
    for item_set in fk:
        for item_set2 in fk:
            if len(item_set & item_set2) == len(item_set) - 1:
                if not (item_set | item_set2) in Lk1:
                    Lk1.add(frozenset(item_set | item_set2))
    return Lk1

def prune_candidate(database, Lk1, minsupp):
    eliminated = set()
    for item_set in Lk1:
        first = set(item_set).pop()
        transactions = columns[first]
        freq = 0

        for t in transactions:
            found = True
            for i in item_set:
                if database[t][i] == 0:
                    found = False;
                    break;
            if found:
                freq +=1

        if float(freq)/num_transactions > minsupp:
            eliminated.add(item_set)

    return eliminated

def eliminate_candidate(database, Lk1, minsupp):
    return None

def count_support():
    eliminated = set()
    for item_set in Lk1:
        first = set(item_set).pop()
        transactions = columns[first]
        freq = 0

        for t in transactions:
            found = True
            for i in item_set:
                if database[t][i] == 0:
                    found = False;
                    break;
            if found:
                freq +=1

        if float(freq)/num_transactions > minsupp:
            eliminated.add(item_set)

    return eliminated

def output_freq_itemsets():
    return None

def main():
    parse_data_file_args()
    matrix = read_database()
    #apriori(database, float(args.minsupp), str(args.output_file))
    f1 = generate_F1(float(args.minsupp))
    f2 = generate_candidate(f1)
    print(f2)
    pruned = prune_candidate(matrix, f2, float(args.minsupp))
    print(pruned)

if __name__ == "__main__":
    main()
