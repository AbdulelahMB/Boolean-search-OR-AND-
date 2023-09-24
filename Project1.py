import json # I need to import the json library to use the loads function.
import time
from nltk.tokenize import word_tokenize

# pip insall nltk
#nltk.dawnload('punkt)
# create_index takes a list of documents as input and returns an inverted index.
def create_index(corpus):
    inverted_index = {}
    for doc_id, doc in enumerate(corpus):
        print(f'\r{round(((doc_id+1)/len(corpus))*100, 1) } % ',end='')
        for word in word_tokenize(doc):
            word=word.upper()
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(doc_id)
    return inverted_index

#The function will accept a query (a string) and index (the inverted index from create_index(corpus) ) as parameters and return
# a list containing the results of searching the index for the query.
def boolean_search(query, index):
    query=word_tokenize(query)       
    Q=(GetQueryIndexs(query,index))
    return(getMyResult(query,Q))

#The function accepts a query (a string) and an index (the inverted index from create_index(corpus)) as parameters and returns 
#the inverted index for every word in the query. If a word is not in the index or if the word is &, then it returns an empty list.
def GetQueryIndexs (query,index):
    length=len(query)
    indexs=[]
    for i in range(length):
        word=query[i].upper()
        if word in index and word != '&' :
            indexs.append(index[word])
        else:
            indexs.append([""])
    return indexs

# The getMyResult function takes a query and a list of inverted indices as input and returns
#  a list of search results by combining the indices using the OR and AND operators.
def getMyResult(query,Q):
    result = []
    orlist, Andlist =(GetLists(query))
    if orlist:
        result=Q[orlist[0]]
    for l in orlist[1:]:
        result=union(result,Q[l])
    for l in Andlist:
        value = intersectionLists(l,Q)
        result=union(result,value)
    return(result)

#The GetLists function takes a query as input and returns 
# two lists of indices representing the words in the query that should be combined using the OR and AND operators.
def GetLists(query):

    indices = [i for i, x in enumerate(query) if x == "&"]

    Andlist=getAndlist(indices,query)
    orlist = [i for i, x in enumerate(query) if i not in [item for sublist in Andlist for item in sublist] and i not in indices]
    return orlist, Andlist 

#getAndlist takes a list of indices and a query as input and returns 
# a list of lists containing the indices of words that should be combined using the AND operator.
def getAndlist(indices,query) :
    Andlist=[]   
    j=0
    i=0
    while i <(len(indices)):
        temllist=[]
        while i+1<len(indices) and indices[i]+2==indices[i+1]:
            temllist.append(indices[i]-1)
            temllist.append(indices[i]+1)      

            i=i+1
        else:
            if(len(query)-1 !=indices[i]):    
                temllist.append(indices[i]-1) 
                temllist.append(indices[i]+1)      
            temllist=list(set(temllist))
            Andlist.append(temllist)
        i=i+1
    return Andlist

#intersectionLists takes a list of indices and a list of inverted indices as input and returns 
#the intersection of the specified inverted indices.
def intersectionLists (list,Q):
    i=0
    if list!=None:
        temp=Q[list[i]]
        i=i+1
        while i< len(list):
            temp=(intersection(temp, Q[list[i]]))
            i=i+1
    return temp

#intersection takes two lists as input and returns their intersection.
def intersection(lst1, lst2):
    lst3 = list(set(lst1).intersection(lst2))
    return lst3

#intersection takes two lists as input and returns their union.
def union(lst1, lst2):
    lst3 = list(set(lst1).union(lst2))
    return lst3


#===================================================================================================================================

with open('news.json', 'r') as f:# Read news in JSON format
    data = [json.loads(line) for line in f]# loads its content into a list of dictionaries called data
#contain 6 keys link:url , headline:title , category:  ,short_description:  ,authors:  , date:  ,


document=[]#list contains the title, authors, and short description of a news article.
for text in data:
    title=text['headline']
    authors=text['authors']
    description=text["short_description"]
    t= f"{title} {authors} {description}"
    document.append(t)


print("Welcome",end="")
print('\nLoading ... ')
start = time.time() 
#We call the create_index(corpus) function and it returns
#an inverted index where the keys are words and the values are lists of document indices where the word appears.
inverted_index=create_index(document)
end = time.time()
t=(end - start)
print("The time it takes to calculate the inverted_index ==>",round(t))
print("--------------------------------------------------------------------------")
while True:
    query=input("write your query here: ")
    start = time.time() 
    result=boolean_search(query,inverted_index)
    end = time.time()
    t=(end - start)*10**6
    length=(len(result))
    print(f"I find {length} results ({t})")
    print("--------------------------------------------------------------------------",end= '\n \n' )


