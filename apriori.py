# -*- coding: utf-8 -*-
"""Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15XAlhcqXJEl8sd1X1HoyaQmiAPHjeqfY
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import pylab as pl
import csv
from itertools import combinations
# %matplotlib inline

from google.colab import files


uploaded = files.upload()

dff = pd.read_csv("retail_dataset.csv")

# take a look at the dataset
print(dff)

#Putting a number for each item
dictionaries = {'Bread': 1, 'Cheese': 2, 'Meat': 3, 'Diaper': 4, 'Wine': 5 , 'Eggs': 6, 'Milk': 7,'Pencil': 8, 'Bagel': 9, }
#Dropping first column
#convertin the df into an array contains each row in an array
dff['items'] = dff[dff.columns[1:]].apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1
)
df_items = dff['items']
df_tid = dff['Transaction Number']
comma_splitted_df = df_items.apply(lambda x: x.split(','))
numbered_col = []
for i in range(len(comma_splitted_df)):
    list_numbered = list(map(lambda x: dictionaries[x], comma_splitted_df[i]))
    sort_numbered = sorted(list_numbered)
    numbered_col.append(sort_numbered)

#making an array that contains each item in the whole dataset
dict_data = {'items': numbered_col}
df = pd.DataFrame.from_dict(dict_data)

items = []
for i in range(len(df)):
    for j in range(len(df['items'][i])):
        items.append(df['items'][i][j])
print(items)

#Get unique element from list/array
unique_item = set(items)

#Convert it to list
list_unique_item = list(unique_item)
#counting the occurance of each item
count_unique = []
for value in (list_unique_item):
    count_unique.append((value, items.count(value)))

candidate1_df = pd.DataFrame(count_unique, columns=["itemset", "sup"])
candidate1_df

import numpy
#Apriori
#filtering the candidate list with the minimum support
def getL(candidate,minimum_sup):
    filtering = candidate['sup'] > minimum_sup
    freq = candidate[filtering]
    return freq
#making the next candidate table 
def nextCandidate(prev_freq_itemset):
    self_join_candidate = []
    for i in range(len(prev_freq_itemset['itemset'])):
        for j in range((i+1), len(prev_freq_itemset['itemset'])):
            itemset_i = prev_freq_itemset['itemset'][i]
            itemset_j = prev_freq_itemset['itemset'][j]
            if(type(itemset_i) == numpy.int64 and type(itemset_j) == numpy.int64):
                itemset_i = {itemset_i}
                itemset_j = {itemset_j}
            union_candidate = itemset_i.union(itemset_j)

            if union_candidate not in self_join_candidate:
                self_join_candidate.append(union_candidate)
    return self_join_candidate

#Let's add it with 1 whenever we found every candidate is a subset from Database D


def count_support(database_dataframe, prev_candidate_list):
    initial_df_candidate['sup'] = 0 #set All value into 0 only for initial value for consistency value when running this cell everytime.
    count_prev_candidate = []

    #Set the Initial value of Previous Candidate
    for i in range(len(prev_candidate_list)):
        count_prev_candidate.append((prev_candidate_list[i], 0))
    
    df_candidate = pd.DataFrame(count_prev_candidate, columns=['itemset', 'sup'])
    
    for i in range(len(database_dataframe)):
        for j in range(len(count_prev_candidate)):
            #using issubset() function to check whether every itemset is a subset of Database or not
            if (df_candidate['itemset'][j]).issubset(set(database_dataframe['items'][i])): 
                df_candidate.loc[j, 'sup'] += 1
            
    return df_candidate

# filter_sup = candidate1_df['sup'] > minimum_sup
freq_itemset1 = getL(candidate1_df,50)
freq_itemset1

candidate2_list = nextCandidate(freq_itemset1)

count_candidate2 = []
#initialize the support =0
#Set the Initial value of Second Count Candidate (C2)
for i in range(len(candidate2_list)):
    count_candidate2.append((candidate2_list[i], 0))

initial_df_candidate = pd.DataFrame(count_candidate2, columns=['itemset', 'sup'])

count_candidate2_df = count_support(df, candidate2_list)

count_candidate2_df

#Filter the itemset based on minimum support (occurences of items)
freq_itemset2 = getL(count_candidate2_df,50)
freq_itemset2

freq_itemset2_reset = freq_itemset2.reset_index(drop=True)
#We need to reset the index, because need to access the index later.
freq_itemset2_reset

self_join_result = nextCandidate(freq_itemset2_reset)

def get_subset(candidate):
    temp = []
    final = []
    for i in range(len(candidate)):
        for j in range(len(candidate)):
            if i != j:
                temp.append(candidate[j])
        temp_set = set(temp)
        final.append(temp_set)
        temp.clear()
    print('Subset from {} : {}'.format(candidate, final))
    return final

def pruning(candidate_set, prev_freq_itemset):
    print('Candidate set', candidate_set)
    temp = []
    
    for idx, value in enumerate(candidate_set):
        list_candidate = list(value)
        temp_candidate = (get_subset(list_candidate))
        
        for temp_item in temp_candidate:
            print('Temp item', temp_item)
            check = temp_item == prev_freq_itemset['itemset']
            print('\nCheck candidate from Previous Frequent Itemset\n', check)
            
            if any(check) == False:
                print(any(check))
                print('Val', value)
            else:
                print('\nAll of {} subset contained in \n{}'.format(candidate_set, prev_freq_itemset))
                if value not in temp:
                    temp.append(value)
                
    return temp

freq_itemset2_reset

subset = [{2, 3}, {1, 3}, {1, 2}]
self_join_result

"""# New Section"""