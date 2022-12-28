#!/usr/bin/env python
# coding: utf-8

# # Installing Important Libraries

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


# # Web Scraping using BeautifulSoup

# In[2]:


url_data = pd.read_excel("Input.xlsx")


# In[3]:


url_data.head()


# In[4]:


url_data.shape


# In[5]:


url_data["URL"][0]


# In[6]:


df = pd.DataFrame({"URL":[''],"Title":[''],"Content":['']})

for i in range(114):
    page = requests.get(url_data["URL"][i],headers={"User-Agent": "XY"})

    soup = BeautifulSoup(page.text,"lxml")
    try:
        title = soup.find("h1",class_="entry-title").text
    except:
        None
    try:
        content = soup.find("div",class_="td-post-content").text.replace("\n",'')
    except:
        None
    df = df.append({"URL":url_data["URL"][i],"Title":title,"Content":content},ignore_index=True)


# In[7]:


df.head()


# In[8]:


df = df.iloc[1:]
df.shape


# # Text Data Preprocessing

# In[9]:


df['Content'] = df['Content'].apply(lambda x:x.lower())


# In[10]:


stop_words_list = pd.read_csv('StopWords_GenericLong.txt')


# In[11]:


my_stopwords = stop_words_list.values.tolist()


# In[12]:


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
library_stopwords = nltk.corpus.stopwords.words('english')
library_stopwords.extend(my_stopwords)


# In[13]:


df['Content'] = df['Content'].apply(lambda x: " ".join([i for i in x.split() if i not in library_stopwords]))


# In[14]:


df['Content']


# # Counting the number of Positive Words

# In[15]:


import itertools
positive_words = pd.read_csv('positive-words.txt')
my_postive_words = positive_words.values.tolist()
my_positive_words_modified = list(itertools.chain.from_iterable(my_postive_words))


# In[16]:


df['Positive_Score'] = df['Content'].apply(lambda x: len([x for x in x.split() if x in my_positive_words_modified]))


# In[17]:


df.head()


# # Counting the Number of Negative Words

# In[18]:


import itertools
negative_words = pd.read_csv('negative-words.txt',encoding='latin-1')
my_negative_words = negative_words.values.tolist()
my_negative_words_modified = list(itertools.chain.from_iterable(my_negative_words))


# In[19]:


df['Negative_Score'] = df['Content'].apply(lambda x: len([x for x in x.split() if x in my_negative_words_modified]))


# In[20]:


df.head()


# # Calculating the Polarity Score of the Content

# In[21]:


for i in range(len(df)):
    df['Polarity_Score'] = (df['Positive_Score'] - df['Negative_Score'])/((df['Positive_Score'] + df['Negative_Score']) 
                                                                          + 0.000001)


# In[22]:


df.head()


# # Calculating the Subjectivity Score of the Content

# In[23]:


for i in range(len(df)):
    df['Subjectivity_Score'] = (df['Positive_Score'] + df['Negative_Score']) / (len(df['Content']) + 0.000001)
df.head()


# # Calculating the Average Sentence Length of the Content

# In[24]:


def avg_sentence_len(text):
    sentences = text.split(".") 
    words = text.split(" ") 
    if(sentences[len(sentences)-1]==""): 
        average_sentence_length = len(words) / len(sentences)-1
    else:
        average_sentence_length = len(words) / len(sentences)
    return average_sentence_length 


# In[25]:


df['Average_Sentence_Length'] = df['Content'].apply(lambda x: avg_sentence_len(x))


# # Calculating the Percentage of Complex Words in the Content

# In[26]:


import syllapy
count = 0
complex_words = []
for i in range(len(df)):
    text = df['Content'][i+1].split()
    for j in range(len(text)):
        if syllapy.count(text[j]) > 2:
            count = count + 1
    complex_words.append(count)


# In[27]:


complex_length = []
for words in range(len(df)):
    length = (complex_words[words])/(len(df['Content'][words + 1]))
    complex_length.append(length)


# In[28]:


df['Percentage_of_Complex_Words'] = complex_length


# In[29]:


df.head()


# # Calculating Fog Index

# In[30]:


index_score = []
for score in range(len(df)):
    value = 0.4*((df['Average_Sentence_Length'][score+1]) + (df['Percentage_of_Complex_Words'][score+1]))
    index_score.append(value)
df['Fog_Index'] = index_score


# In[31]:


df.head()


# # Calculating Average Number of Words per Sentence

# In[32]:


import re
average_words = []
for i in range(len(df)):
    parts = [len(l.split()) for l in re.split(r'[?!.]', df['Content'][i+1]) if l.strip()]
    words = sum(parts)/len(parts)
    average_words.append(words)


# In[33]:


df['Average_Number_Of_Words_per_Sentence'] = average_words


# In[34]:


df.head()


# # Calculating the Number of Complex Words

# In[35]:


df['Complex_Words'] = complex_words


# # Removing Punctuation Marks

# In[36]:


import string
def punctuation_remove(text_data):
    clean_data = ''.join([i for i in text_data if i not in string.punctuation])
    return clean_data
df['Content'] = df['Content'].apply(lambda x: punctuation_remove(x))


# # Calculating the Word Count of the Content

# In[45]:


words = []
for word in range(len(df)):
    content_length = len(df['Content'][word+1])
    words.append(content_length)
df['Word_Count'] = words


# # Calculating the Syllables

# In[46]:


vowels = ['a','e','i','o','u']
syllable = 0
syllable_count = []
for websites in range(len(df)):
    for post in df['Content'][websites+1]:
        for letter in post:
            if letter in vowels:
                syllable = syllable + 1
        
    syllable_count.append(syllable)
df['Syllable_Count_'] = syllable_count      


# # Calculating the number of Pronouns present in the Content

# In[47]:


pronoun_count = []
for websites in range(len(df)):
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    pronoun = pronounRegex.findall(df['Content'][websites+1])
    pronoun_length = len(pronoun)
    pronoun_count.append(pronoun_length)  
df['Personal_Pronouns'] = pronoun_count


# # Calculating the Average Word Length of the Content

# In[48]:


average_word_length = []
for websites in range(len(df)):
    for post in df['Content'][websites+1]:
        total_characters = len(post)
        total_words = len(post.split(" "))
        average = total_characters/total_words
    average_word_length.append(average)
df['Average_Word_Length'] = average_word_length


# # Saving the DataFrame into a CSV file

# In[50]:


df.to_csv("D:/BlackCoffer/Assignment_Output_File.csv")


# In[ ]:




