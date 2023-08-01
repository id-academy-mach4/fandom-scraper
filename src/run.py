import string

# List of words that we will remove from our string
wordsNotToUse = ["of", "the", "a", "when", "it", "if", "are", "so", "why", "how", "do", "to", "should", "i"]

# Function to parse a string and remove punctuation and words not to use.
def findKeywords(startingString):
  i = startingString.lower().translate(str.maketrans('', '', string.punctuation))
  for word in wordsNotToUse:
    i = i.replace(word + " ", "")

  return i
