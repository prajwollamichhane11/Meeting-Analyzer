import spacy
import csv


def wordProcessing(words):
    cleanWords = []

    smallWords = []


    for i in range(len(words)):
        smallWords.append(words[i].lower())

    noRepetition = list(set(smallWords))

    for i in range(len(noRepetition)):
        try:
            if type(int(noRepetition[i])) == "<class 'int'>":
                continue
        except:
            cleanWords.append(noRepetition[i])

    return cleanWords


def talkedWords():

    words = []

    with open('Text_Output/out.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            pass

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(row[0])

    for ent in doc.ents:
        words.append(ent.text)
    
    words = wordProcessing(words)

    return words


words = talkedWords()
print(words)