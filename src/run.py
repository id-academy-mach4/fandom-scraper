import string
import setup

# List of words that we will remove from our string
wordsNotToUse = ["of", "the", "a", "when", "it", "if", "are", "so", "why", "how", "do", "to", "should", "in", "i", "you", "u", "what", "who", "is", "cant", "cannot", "way", "get", "best", "worst"]

# Function to parse a string and remove punctuation and words not to use.
def findKeywords(startingString):
  i = startingString.lower().translate(str.maketrans('', '', string.punctuation))
  for word in wordsNotToUse:
    i = i.replace(word + " ", "")

  return i

def promptUser():
  userInput = input("What would you like to know about " + setup.fandom + "?\nPlease frame your response in the form of a question, with the name of the fandom in the question.\nFor example, \"What is the best way to collect strawberries in celestegame?\"\n")
  keywords = findKeywords(userInput)
  print(keywords)