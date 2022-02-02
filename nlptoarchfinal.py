# -*- coding: utf-8 -*-
"""NLPtoArchFinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Az7ps0L9EoLeAJF3sbGEQdi3UK0ULmvd
"""

import nltk
import re
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
stopwords_remove=['from','to','and','it','with']
for i in stopwords_remove:
  stop_words.remove(i)
stopwords_add=['The']
for i in stopwords_add:
  stop_words.add(i)
# stop_words.remove('of')

from nltk.stem.snowball import SnowballStemmer
ps = SnowballStemmer("english")
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

input_paragraph = "The coffeemaker consists of a brewer and a pot. The pot consists of a glassware, a lid, and a handle. The brewer is composed of a tank, a heating unit, a brewing unit, and a dispensing unit. The heating unit consists of a heating coil, a hot water pipe, and a water valve. The heating coil imports electricity and converts it into heat. The heating coil transfers heat to the water pipe. The water pipe imports water and heat and energizes water with heat. The vertical pipe transfers hot water from the water pipe to the shower head. The brewing unit consists of a shower head, a filter, and a filter holder. The shower head imports hot water from the vertical pipe and distributes it. The filter imports ground coffee and hot water from the shower head, couples these two flows,and exports liquid coffee. The filter separates liquid coffee from the ground coffee and exports it to the glassware."
energy_list=['heat','electricity','water','steam','kinetic','chemical','electrical','mechanical','thermal','nuclear','gravitational', 'hot']



def remove_stopwords_from_raw_text(text):
    try:
        words = nltk.word_tokenize(text)
        return remove_stopwords_from_tokenized_text(words)

    except Exception as e:
        print(str(e))



def remove_stopwords_from_tokenized_text(words):
    try:
        output_list = []
        
        for w in words:
            if w not in stop_words:
                output_list.append(w)

        return output_list

    except Exception as e:
        print(str(e))



def tag_pos_of_raw_text(text):
    try:
        words = nltk.word_tokenize(text)
        return nltk.pos_tag(words)
    except Exception as e:
            print(str(e))



#Removing stopwords
final_list= remove_stopwords_from_raw_text(input_paragraph)

print("\n\n\n\nAfter removing stopwords = " , final_list)

# Converting words not in nltk  synonym list to the ones that are accepted
index=0
for i in final_list:
  if ((i.lower()=="supply".lower())):
    final_list[index]="transfer"
  if i.lower()=="incorporate".lower() or i.lower()=="composed".lower() :
    final_list[index]="consists"
  if i.lower()=="accomodates".lower() :
    final_list[index]="contains"
  if i.lower()=="tranform".lower() :
    final_list[index]="converts"
  index=index+1


new_final_list=[]
new_para=""
for ele in final_list: 
        new_para= new_para +" " +ele


new_para_latest=""
carry_on=""
new_list=new_para.split(".")
for i in new_list:
  if "consists" in i:
    carry_on=""
    within_words=i.split()
    for words in within_words:
      if (words=="and" or words=="consists" or words==","):
        new_para_latest=new_para_latest[:-1]+" "+words+" "
      else:
        new_para_latest=new_para_latest+words.upper()+"_"
      carry_on=words
    new_para_latest=new_para_latest[:-1]+" . " 
  else:
    if (("imports" in i) or ("couples" in i) or ("transfers" in i)):
      within_words=i.split()
      index_func=0
      index_from=0
      index_to=0
      for m in range(len(within_words)):
        if (within_words[m]=="imports" or within_words[m]=="transfers" or within_words[m]=="couples"):
          index_func=m
        elif (within_words[m]=="from"):
          index_from=m
        elif (within_words[m]=="to"):
          index_to=m
        else:
          continue
    m=0
    while(m<len(within_words)):
      if (index_func>0 and m==0):
        for x in range(index_func):
          new_para_latest=new_para_latest+within_words[m].upper()+"_"
          m=m+1
        new_para_latest=new_para_latest[:-1]
      elif(index_from>0 and index_to>0 and m==index_from):
        new_para_latest=new_para_latest+" from"+" "
        m=m+1
        for x in range(index_from+1,index_to):
          new_para_latest=new_para_latest+within_words[m].upper()+"_"
          m=m+1
        new_para_latest=new_para_latest[:-1]+" to "
        m=m+1
        for x in range(index_to+1,len(within_words)):
          new_para_latest=new_para_latest+within_words[m].upper()+"_"  
          m=m+1    
        new_para_latest=new_para_latest[:-1]    
      elif (index_from>0 and i==index_from and m==index_from):
        new_para_latest=new_para_latest+" from "
        m=m+1
        for x in range(index_from+1,len(within_words)):
          new_para_latest=new_para_latest+within_words[m].upper()+"_"
          m=m+1
        new_para_latest=new_para_latest[:-1]
      elif(index_from==0 and index_to>0 and m==index_to):
        new_para_latest=new_para_latest+" to "
        m=m+1
        for x in range(index_to+1,len(within_words)):
          new_para_latest=new_para_latest+within_words[m].upper()+"_"
          m=m+1
        new_para_latest=new_para_latest[:-1]     
      else:
        new_para_latest=new_para_latest+" "+within_words[m]
        m=m+1
    new_para_latest=new_para_latest+" . "


        
        
   

print("\n\n Latest para = ", new_para_latest)


var= False
exchange_word='';
def convert_synonyms(word) :
  try :
    stemmed_word=ps.stem(word)
    if ((word=='.') or (word==',')):
      return word
    new_word='"' + stemmed_word + '"'
    # print(new_word)
    for syn in wordnet.synsets(new_word):
      for lm in syn.lemmas():
        for x in word_accept :
          if (lm.name()).lower()==x.lower():
            var=True;
            exchange_word=x
    if var==True :
      return exchange_word
      var=False
    else :
      return word
  except Exception as e:
      word.upper()

#Converting the words into synonym if there in nltk library
for item in word_tokenize(new_para_latest):
  var=False
  for i in energy_list:
    if i.lower()==item.lower():
      new_final_list.append(i)
      var=True
      break
  if var==True:
    continue
  else:
    new_item= convert_synonyms(item)
    if(new_item==None):
      new_final_list.append(item)
    else:
      new_final_list.append(new_item)


# #Printing list
print("\n\n\n List after processing synonyms = " , new_final_list)



str=''
for element in new_final_list:
  str=str+" "+element



print(str)

# textfile = open("NLP_Output.txt", "w")
# for element in final_list:
#     textfile.write(element + "\n")
# textfile.close()

# from google.colab import files
# files.download('NLP_Output.txt')