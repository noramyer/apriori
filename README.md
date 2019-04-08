# Apriori
#### Nora Myer
#### April 2019

## Running
Dependencies include:
- Python 2.7
- numpy compatible with python 2.7
- Run on Linux or Mac environment

```
python Apriori.py -database_file database.txt -minsupp .25 -output_file output.txt
```

## About

### Data representations
To hold the database, I used a sparse matrix, "database", of size n x m where n is the number of transactions and m is the number of unique elements within the database file.

For example, suppose the database file look like this:
```
5 6
0 2
0 3 4 5
1 2 3 4
0 2 3 4
0 1 2 4
```
The resulting sparse matrix of size 5 x 6 would look like the following, where database[n][m] is a 1 if item m appears in the nth transaction:
```
1 0 1 0 0 0
1 0 0 1 1 1
0 1 1 1 1 0
1 0 1 1 1 0
1 1 1 0 1 0
```

An addition dictionary was used to map each unique item to a set of all transactions containing that item. For example:
```
0 --> (0, 1, 3, 4)
```
This was useful when getting the frequent 1-itemsets as well as when getting the support count for an item_set. The first item in the item_set was removed, and only those transactions were iterated through to check if the transaction contains the entire item_set. Since the dictionary functions with hashing, this saved complexity during these calculations.

Lastly, to store the candidate item_sets, such as with lk1 and fk, I used a set which contained frozenset versions of item_sets. My choice for this was based on the fact that python sets can only contain objects like a set if they are immutable since they get hashed. I wanted the O(1) look-up time of sets within a set.

### def generate_F1(minsupp):
Parameters:
```
minsupp = the minimum support
uses global variable columns: dictionary that maps each unique item to a set of all transactions containing that item.
```
This method generates all frequent itemsets of length 1. Utilizing one of the data structures which maps a unique item to it's frequency in transactions, all the items who meet the minimum support are returned.

Return: A set of item_sets which represents frequent 1-itemsets.

### def generate_candidates(fk):
Parameters:
```
fk = a set of item_sets, { {1, 2}, {2, 3}, {1, 3}, {1, 4} }
```
This method took in a set, fk, which contained item_sets. To generate the Lk+1 candidates, the Fk-1 X Fk-1 candidate generation method was used. If the intersection of two item_sets was of length k-1, meaning the overlap was one less than the length of the item_set, then the union of those two item_sets is a candidate in Lk+1.

Return: A set of item_sets which represents Lk+1 candidates.

### def prune_candidates(database, fk, Lk1, minsupp):
Parameters:
```
database =  sparse matrix representation of the database file
fk = a set of item_sets, { {1, 2}, {2, 3}, {1, 3}, {1, 4} }
Lk1 = set of candidate item_sets, { {1, 2, 3}, {1, 2, 4}, {1, 3, 4} }
minsupp = the minimum support
```
This method finds all infrequent subsets of length k contained within the item_sets in Lk+1 and prunes the Lk+1 itemsets if they contain those infrequent k-itemsets. It utilizes the sparse matrix to efficiently check if an item_set is contained within a transaction, breaking if not to save run-time.

Return: A set of item_sets which represents Lk+1 candidates after pruning.

### def count_support(database, Lk1):
Parameters:
```
database =  sparse matrix representation of the database file
Lk1 = set of candidate item_sets, { {1, 2, 3}, {1, 2, 4}, {1, 3, 4} }
```
Counts the frequency of each itemset in Lk+1 in the database.

Return: A dictionary mapping Lk+1 itemsets to a count of their frequency in the database.

### def eliminate_candidates(count_vector, Lk1, minsupp):
Parameters:
```
count_vector = dictionary mapping of an item_set to the frequency of appearance in database, { ({1, 2, 3}): 1.0, ({1, 2, 4}): 2.0, ({1, 3, 4}): 1.0 }
Lk1 = set of candidate item_sets, { {1, 2, 3}, {1, 2, 4}, {1, 3, 4} }
minsupp = the minimum support
```
Based on the frequency counts of each Lk+1 itemset found in count_vector, removes item_sets if the support does not meet the minsupp.

Return: A set of item_sets which represents Lk+1 candidates after elimination.
## Results

Results are found in output.txt. For each Fk, the results are printed of the format:
```
num_transactions num_unique_items
transaction 1
.
.
.
transaction n
```
The final non-zero Fk item_set can be found at the bottom of the file. Each transaction has a number of items, for example,
the first transaction in the above example has item 0, 2 and 3 (C-style indexing). The format should match the database input file, except that the format is repeated for each fk from 1 to k.
