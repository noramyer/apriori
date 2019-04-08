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
    fk_itemsets = []
    k = 1
    fk = generate_F1(minsupp)

    while len(fk) > 0:
        fk_itemsets.append(fk)
        #print(len(fk))
        #print("k = "+str(k) + " and " + str(fk))
        lk1 = generate_candidates(fk)
        lk1 = prune_candidates(database, fk, lk1, minsupp)
        count_vector = count_support(database, lk1)
        lk1 = eliminate_candidates(count_vector, lk1,minsupp)
        k+=1
        fk = lk1

    output_freq_itemsets(fk_itemsets[-1], output_file)

    return None

def generate_F1(minsupp):
    f1 = set()
    for key in columns:
        if float(len(columns[key]))/num_transactions > minsupp:
            fr = frozenset([key])
            f1.add(fr)

    return f1

#fk-1 x fk-1 generation method
def generate_candidates(fk):
    Lk1 = set()
    for item_set in fk:
        for item_set2 in fk:
            if len(item_set & item_set2) == len(item_set) - 1:
                if not (item_set | item_set2) in Lk1:
                    Lk1.add(frozenset(item_set | item_set2))
    return Lk1

def get_count_support(database, s):
    first = s.pop()
    transactions = columns[first]
    freq = 0

    for t in transactions:
        found = True
        for i in s:
            if database[t][i] == 0:
                found = False;
                break;
        if found:
            freq +=1

    return float(freq)

def findsubsets(s):
    combinations = set()
    for item in s:
        new_s = set()
        new_s.add(item)
        combinations.add(frozenset(s - new_s))

    return combinations

def prune_candidates(database, fk, Lk1, minsupp):
    remove_set = set()
    for item_set in Lk1:
        sets = set()
        sets = findsubsets(set(item_set))

        for s in sets:
            if not s in fk:
                if (get_count_support(database, set(s))/num_transactions < minsupp):
                    remove_set.add(item_set)

    return Lk1 - remove_set

def eliminate_candidates(count_vector, Lk1, minsupp):
    remove_set = set()
    for item_set in Lk1:
        if count_vector[item_set]/num_transactions < minsupp:
            remove_set.add(item_set)

    return Lk1 - remove_set

def count_support(database, Lk1):
    lk1_map = {}
    for item_set in Lk1:
        lk1_map[item_set] = get_count_support(database, set(item_set))

    return lk1_map

def output_freq_itemsets(fk, output_file):
    f = open(output_file, 'w+')
    num = len(fk)
    print("Fk = "+str(fk))
    print("num = "+str(num))
    print("union is "+str(fk.union()))
    f.write(str(num) + "\n")
    for s in fk:
        f.write(str(' '.join(str(e) for e in s)) + "\n")

    return None

def main():
    parse_data_file_args()
    database = read_database()
    apriori(database, float(args.minsupp), str(args.output_file))

if __name__ == "__main__":
    main()
