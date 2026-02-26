#Get the average words per sentence, excluding punctuation def getWords PerSentence(sentences):
totalwords=0
for sentence in sentences:
    totalWords += len(sentence.split(" "))
return totalWords / len(sentences)

# Convert part of speech from pos_tag() function
# into wordset compatible pos tag 
posToWordnetTag = {
}
"J": wordnet.ADJ, "V": wordnet.VERB,
"N": wordnet.NOUN,
"R": wordnet.ADV
def treebankPosToWordnetPos(partOfSpeech):
posFirstCharpartofSpeech (0)
if posFirstChar in posToWordnetTag:
return posToWordnetTag(posFirstChar)
return wordnet.NOUN
Convert raw list of (word, POS) tuple to a list of strings
