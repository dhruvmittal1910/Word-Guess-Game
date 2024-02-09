import nltk
import sys
import nltk
import random
import re


from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import *
nltk.download("averaged_perceptron_tagger")


# this function when called starts the game

def guessGame(wordGuessList):
  # 5 points to every user to start
  newWord=random.choice(wordGuessList)
  print(newWord)
  guessBlank=["_"]*len(newWord)
  totalScore=5
  print(len(newWord)*"_ ")
  
  while True:
    
    letter=input("Guess a letter: ")
    if letter in guessBlank:
      print("Already guessed this letter, guess another letter")
    
    elif totalScore<=0 or letter=="!":
      print("Game Ends")
      exit(1)
    
    elif(letter in newWord):
      totalScore=totalScore+1
      print("Right! Score is ",totalScore)
      for m in re.finditer(letter,newWord):
        guessBlank[m.start()]=letter
      print(customPrint(guessBlank))
      
         
    elif(letter not in newWord):
      totalScore=totalScore-1
      if(totalScore==0):
        print("Sorry, your score is 0")
        response=input("Want to play another game (yes/no):- ")
        if response=="yes":
          guessGame(wordGuessList)
        else:
          print("Thank you for Playing 😊")
          exit()
      else:
        print("Sorry, guess again. Score is ",totalScore)  
        print(customPrint(guessBlank))
      
    
    count=0
    for i in guessBlank:
      if i != "_":
          count=count+1
    if count==len(newWord):
        print("Greattt..You Solved it!😁")
        response=input("Want to play another game (yes/no):- ")
        if response=="yes":
          guessGame(wordGuessList)
        else:
          print("Thank you for Playing 😊")
          exit()

  
  


# function is called to start preprocessing of the data
def preProcessing(newText):
  #### preprocess the text function
  # print(len(newText))
  newTokens=word_tokenize(newText)
  # lowercase the tokens
  lowerCaseTokens=[]
  for i in newTokens:
    lowerCaseTokens.append(i.lower())
  
  # newUniqueTokens=set(lowerCaseTokens)
  # print(len(newUniqueTokens))

  # converting tuple of unique tokens to a list of unique tokens
  tokens=[]
  for i in lowerCaseTokens:
    tokens.append(i)

  # reduce to those tokens that are alpha
  alphaTokens=[word for word in lowerCaseTokens if word.isalpha()]
  # print(len(alphaTokens))

  # reduce to those tokens that are not in stopword list
  stop_words=set(stopwords.words("english"))
  tokensWithNoStopwords=[word for word in alphaTokens if word not in stop_words]
  # print(len(tokensWithNoStopwords))

  # reduce to words that have length>5
  finalTokens=[word for word in tokensWithNoStopwords if len(word)>5]
  # print(len(finalTokens))

  # lemmatize tokens and make a list of unique lemmas
  wnl=WordNetLemmatizer()
  lemmatizeTokens=[wnl.lemmatize(i) for i in finalTokens]

  lemmatizeTokens=set(lemmatizeTokens)
  
  lemmatizeTokens=list(lemmatizeTokens)
  # print(len(lemmatizeTokens))
  # add pos tagging and get first 20 unique words and there tags
  lemmatizeTokens=sorted(lemmatizeTokens)
  posTagTokens=nltk.pos_tag(lemmatizeTokens)
  print("first 20 words and there tags:- ",posTagTokens[:20])

  # only noun lemmas
  nounTokens=[]
  for word in posTagTokens:
    if word[1] == "NN" or word[1] == "NNS" or word[1] == "NNP" or word[1] == "NNPS" :
      nounTokens.append(word)
  # print(len(nounTokens))

# step e -> final token list after step a
  print("Number of Tokens after step a:-", len(finalTokens))
# step e -> total number of nouns
  print("Total number of nouns in step d:-",len(nounTokens))  
  

  return finalTokens,nounTokens



def customPrint(newList):
  word=""
  for i in newList:
    word=word+i+" "
  return word



def main():
  # check if command line arg is provided
  if len(sys.argv)!=2:
    print("Error:python new.py <filename>")
    sys.exit(1)
  
  filename=sys.argv[1]
  print("Filename:",filename)
  my_file=open(filename,"r")
  #  read the file
  text=my_file.read()
  # print(text)
  my_file2=open(filename,"r")
  newText=my_file2.read()
  # finalTokens,nounTokens=preProcessing(text)



  # replace end of line with blank space and split wherever we see a "."
  text=text.replace('\n',' ').split(".")
  # print(text)

  # storing each line in a list of lists
  sentenceTokens=[]
  for line in text:
    sentenceTokens.append(word_tokenize(line))
  # print(sentenceTokens)

  # fetching tokens in whole text file
  tokens=[]
  for i in sentenceTokens:
    for j in i:
      tokens.append(j.lower())

  # total tokens
  totalTokenNumber=len(tokens)
  print("Total number of tokens:-",totalTokenNumber)
  # unique tokens
  uniTokens=set(tokens)
  totalUniqueTokenNumber=len(uniTokens)
  print("Unique Tokens:- ",totalUniqueTokenNumber)

  # lexical diversity
  lexticalDiversity=totalUniqueTokenNumber/totalTokenNumber
  print("Lexical Diversity: ",round(lexticalDiversity,2)," It means there are",round(lexticalDiversity,2)*100,"% of unique words in the text")

  print("Step 3:-")
  finalTokens,nounTokens=preProcessing(newText)
  print("Step 4:- ")
  # make a dictionary
  dict={}

  # make a dict from {noun:number of noun in finalTokens list}
  for key in nounTokens:
      dict[key[0]]=finalTokens.count(key[0])
  
  dict=sorted(dict.items(),key=lambda x:x[1],reverse=True)
  # 50 most common words
  commonWords=dict[:50]

  print(commonWords)

  #saved the words in a list for use in word guess game 
  wordGuessList=[word[0] for word in commonWords]

  # starting the game
  print("Step 5:-")
  guessGame(wordGuessList)


if __name__=="__main__":
  main()
