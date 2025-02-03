import json
import nltk
from nltk.stem import PorterStemmer
bp = 'TEST/'
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from writeBack2File import writeBack2File



def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)

def tokenize(content):
    Tokenizer = RegexpTokenizer('[a-zA-Z0-9]{1,}\'{,1}[a-zA-Z0-9]') 
    tokens = Tokenizer.tokenize(content)
    return tokens


def make_json_dict(file):
    with open(file,'r') as f:
        return json.load(f)


# def writeURLDict(unique_links_dict):
#     with open('book_keeping.txt', 'a') as file:
#         for key, val in unique_links_dict.items():
#             file.write(str(key)+',' + val)
#             file.write("\n")

def writeURLDict(unique_links_dict):
    with open('book_keeping.txt', 'w') as file:
        file.write(json.dumps(unique_links_dict))
        file.close()



if __name__ == "__main__":
    inverted_index = writeBack2File()
    unique_links_dict = dict()
    unique_links_set = set()
    counter = 0
    checksum_set = set()
    for entry in os.listdir(bp):
        x = os.path.join(bp, entry)
        for entry2 in os.listdir(x):
            final = os.path.join(x, entry2)  # file
            json_dict = make_json_dict(final)
            url = json_dict['url']
            if url not in unique_links_set:
                unique_links_set.add(url)
                unique_links_dict[counter] = url
                counter += 1

            content = json_dict['content']
            encoding = json_dict['encoding']
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            checksum = 0
            for char in text:
                checksum += int(ord(char))
            if checksum not in checksum_set:
                checksum_set.add(checksum)
                tokens = tokenize(text)
                for i in range(len(tokens)):
                    tokens[i] = stem(tokens[i])
                
                tokens_freq = dict()
                for i in range(len(tokens)):
                    if tokens[i] in tokens_freq:
                        tokens_freq[tokens[i]].append(i)
                    else:
                        tokens_freq[tokens[i]] = []
                        tokens_freq[tokens[i]].append(i)
                        
                    if i > 0:
                        if tokens[i-1]+tokens[i] in tokens_freq:
                            tokens_freq[tokens[i-1]+tokens[i]].append(i-1)
                        else:
                            tokens_freq[tokens[i-1]+tokens[i]] = []
                            tokens_freq[tokens[i-1]+tokens[i]].append(i-1)

                for k,positions in tokens_freq.items():
                    inverted_index.addUrlToToken(k,counter-1,len(positions), positions)
            else:
                pass

    writeURLDict(unique_links_dict)
    print("NUMBER OF INDEXED DOCUMENTS: "+ str(len(unique_links_set)))
    print("NUMBER OF UNIQUE WORDS: "+str(len(inverted_index.data.keys())))

    inverted_index.write()


        

        












