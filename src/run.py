import string
import setup
import model

# List of words that we will remove from our string
words_not_to_use = ["of", "the", "a", "when", "it", "if", "are", "so", "why", "how", "do", "to", "should", "in", "i", "you", "u", "what", "who", "is", "cant", "cannot", "way", "get", "best", "worst"]

# Function to parse a string and remove punctuation and words not to use.
def findKeywords(starting_string):
  global words_not_to_use
  i = starting_string.lower().translate(str.maketrans('', '', string.punctuation))
  for word in words_not_to_use:
    i = i.replace(word + " ", "").replace_first("celeste", "celestegame", 1).replace("hypixel", "hypixel-skyblock", 1).replace("hypixel-skyblock skyblock", "hypixel-skyblock", 1)
  return i

def promptUser():
  userInput = input("What would you like to know? Please frame your response in the form of a question, with the name of the fandom in the question.\nFor example, \"What is the best way to collect strawberries in Celeste?\" (You can quit with \"q\".)\n\n")
  print("")
  # In case they want to quit
  if(userInput.lower() == "q"): return None
  keywords = findKeywords(userInput)
  print("DEBUG_KEYWORDS", keywords)
  return False

prompting = True
while prompting:
  print(">> NEW QUESTION\n")
  x = promptUser()
  while(x is False):
    print(">> QUESTION ERROR\n")
    print("Please try again! We could not parse your input...\n")
    x = promptUser()
  else:
    if(x is None):
      prompting = False
      break
    else:
      print(">> RESULT\n")
      print(x)
      x = None
      if(answer.lower() == "y"):
        prompting = True
      else:
        prompting = False
        break
print("\n\nTHANKS FOR ASKING OUR PROGRAM!\nCreated by Nick, Annabella, Orchid, and Tyler.\n\n")
