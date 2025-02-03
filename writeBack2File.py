import json
import math
from Posting import Posting
import os
import jsonpickle
from collections import defaultdict
from itertools import chain
from operator import methodcaller
directory_0 = "indices"
directory_1 = "partial_indices"

class writeBack2File:
    def __init__(self):
        self.data = dict()
        self.token_docid = dict()
        self.bigData = dict()
        self.count = 0
        self.initial_set = set()
    def addUrlToToken(self, token, docid, fre, positions):
        self.count += 1
        P = jsonpickle.encode(Posting(docid, fre, positions))
        initial = token[0]
        if initial.isdigit():
            initial = "numeric"
        self.initial_set.add(initial)
        if initial in self.bigData:
            if token in self.bigData[initial]:
                self.bigData[initial][token].append(P)
            else:
                self.bigData[initial][token] = list()
                self.bigData[initial][token].append(P)

        else:
            self.bigData[initial] = dict()
            self.bigData[initial][token] = list()
            self.bigData[initial][token].append(P)
        if token in self.token_docid:
            self.token_docid[token].add(docid)
        else:
            self.token_docid[token] = set()
            self.token_docid[token].add(docid)


        if self.count > 5000:
            self.partialIndices()
            count = 0

    def partialIndices(self):
            for initial in self.bigData:
                path = directory_1 + "/" + initial + ".txt"
                merged_dict = self.bigData[initial]
                if os.path.exists(path):
                    file = open(path, 'r')
                    tmp_dict = json.load(file)
                    file.close()
                    merged_dict = self.merge(merged_dict, tmp_dict)
                file = open(path, 'w+')
                file.write(json.dumps(merged_dict))
                file.close()
            self.bigData.clear()

    def merge(self, dict1, dict2):
        merged = defaultdict(list)
        dict_items = map(methodcaller('items'), (dict1, dict2))
        for k, v in chain.from_iterable(dict_items):
            merged[k].extend(v)
        return merged


    def write(self):
        with open('book_keeping.txt','r') as file:
            url_docid_dict = json.load(file)
            total_files = max(url_docid_dict.keys())
            file.close()
        for initial in list(self.initial_set):
            path0 = directory_0 + "/" + initial + ".txt"
            path1 = directory_1 + "/" + initial + ".txt"
            if initial in self.bigData:
                merged_dict = self.bigData[initial]
            else:
                merged_dict = {}
            if os.path.exists(path1):
                file = open(path1, 'r')
                tmp_dict = json.load(file)
                merged_dict = self.merge(merged_dict, tmp_dict)
                file.close()
            for token, lists in merged_dict.items():
                with open(path0, 'a') as file:
                    token_file = open("token_index.txt", "a")
                    token_file.write(token + "," + repr(file.tell()) + "\n")
                    token_file.close()

                    N = int(total_files) + 1
                    df = len(self.token_docid[token])
                    idf = math.log(N/df, 10)

                    file.write(token + "\n") 
                    file.write(str(self.token_docid[token]))
                    file.write("\n")
                    for p in lists:
                        posting = jsonpickle.decode(p)
                        tf = 1 + math.log(posting.tfidf, 10)
                        tfidf = tf*idf
                        file.write(str(posting.docid))
                        file.write("||")
                        file.write(str(tfidf))
                        file.write("||")
                        file.write(str(posting.fields))
                        file.write("||#@\n")
                    file.close()

