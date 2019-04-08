import argparse
import numpy as np

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
def read_database(database_file):
    global num_transactions
    global num_items
    global columns

    #open file and read lines into array
    with open(database_file) as f:
        content = f.readlines()

    #Get number of transactions and items from line 1
    num_transactions = int(content[0].split()[0])
    num_items = int(content[0].split()[1])

    #Initialize sparse matrix based on size
    matrix = np.zeros((num_transactions, num_items))

    #For every transaction, fill in sparse matrix
    for i in range(1, num_transactions+1):
        row = map(int, content[i].split())
        for j in range(len(row)):
            if not row[j] in columns:
                columns[row[j]] = set()

            #Add set of transactions for every item
            columns[row[j]].add(i-1)
            #Add item to transaction matrix
            matrix[i-1][row[j]] = 1

    return matrix

#Apriori function
def apriori(database, minsupp, output_file):
    fk_itemsets = []
    k = 1
    #generate frequent 1-itemsets
    fk = generate_F1(minsupp)

    #while there are still k-itemsets to generate
    while len(fk) > 0:
        #history of each k item set
        fk_itemsets.append(fk)

        lk1 = generate_candidates(fk)
        lk1 = prune_candidates(database, fk, lk1, minsupp)
        count_vector = count_support(database, lk1)
        lk1 = eliminate_candidates(count_vector, lk1, minsupp)
        k+=1
        fk = lk1

    #print itemsets to output file
    output_freq_itemsets(fk_itemsets, output_file)

#Generate all frequent 1-item sets
def generate_F1(minsupp):
    f1 = set()

    #Use column mapping dictionary to pull number transactions containing item
    for key in columns:
        if float(len(columns[key]))/num_transactions >= minsupp:
            fr = frozenset([key])
            f1.add(fr)

    return f1

#fk-1 x fk-1 generation method
def generate_candidates(fk):
    Lk1 = set()
    for item_set in fk:
        for item_set2 in fk:
            #if the intersection of the item sets = k - 2
            if len(item_set & item_set2) == len(item_set) - 1:
                #and the itemset is not repeated
                if not (item_set | item_set2) in Lk1:
                    #add itemset to k+1 candidate set
                    Lk1.add(frozenset(item_set | item_set2))
    return Lk1

#Get count of support for a given set
def get_count_support(database, s):
    #get all transactions containing first item in itemset
    first = s.pop()
    transactions = columns[first]
    freq = 0

    #for all the transactions containing the first item in the set
    for t in transactions:
        found = True
        #see if transaction contains all items in the set
        for i in s:
            #if not, break
            if database[t][i] == 0:
                found = False;
                break;
        #if so, add support count of the set
        if found:
            freq +=1

    return float(freq)

#generates subsets of length n - 1
def findsubsets(s):
    combinations = set()
    #get all subsets
    for item in s:
        new_s = set()
        new_s.add(item)
        combinations.add(frozenset(s - new_s))

    return combinations

#prune candidates containing infrequent k-1 subets
def prune_candidates(database, fk, Lk1, minsupp):
    remove_set = set()
    #for each subset
    for item_set in Lk1:
        sets = set()
        #get subsets of length k-1
        sets = findsubsets(set(item_set))

        for s in sets:
            #if the itemset is not known to be frequent
            if not s in fk:
                #if itemset doesnt meet support
                if (get_count_support(database, set(s))/num_transactions < minsupp):
                    if not item_set in remove_set:
                        remove_set.add(item_set)

    #remove item sets containing subsets
    return Lk1 - remove_set

#Eliminate candidates that are infrequent
def eliminate_candidates(count_vector, Lk1, minsupp):
    remove_set = set()
    #for each set
    for item_set in Lk1:
        #if the support is less than the minimum support, add to set to be removed
        if count_vector[item_set]/num_transactions < minsupp:
            remove_set.add(item_set)

    #remove infrequent sets
    return Lk1 - remove_set

#Get the count frequency of all item_sets in set Lk1
def count_support(database, Lk1):
    lk1_map = {}
    for item_set in Lk1:
        lk1_map[item_set] = get_count_support(database, set(item_set))

    #return dictionary mapping each set to a count
    return lk1_map

#for each set of candidates generated from k = 1 to k = n print item sets generated
def output_freq_itemsets(fk, output_file):
    f = open(output_file, 'w+')

    #for each fk
    for i in range(len(fk)):
        #get number of transactions and unique elements in set
        num = len(fk[i])
        unique = get_unique_item_size(fk[i])

        #write header information for fk itemsets
        f.write(str(num) + " " + str(unique) + "\n")
        #write each itemset to file
        for s in fk[i]:
            f.write(str(' '.join(str(e) for e in s)) + "\n")

        f.write("\n")

#get number of unique elements contained within a set of sets
def get_unique_item_size(item_sets):
    unique_items = set()
    for sets in item_sets:
        unique_items = unique_items | sets

    return len(unique_items)

#main function
def main():
    #get arg parser
    parse_data_file_args()
    #get database
    database = read_database(str(args.database_file))
    #apriori
    apriori(database, float(args.minsupp), str(args.output_file))

if __name__ == "__main__":
    main()
