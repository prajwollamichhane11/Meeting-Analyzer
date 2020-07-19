import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from textblob import TextBlob

import csv

from pydub import AudioSegment 
import speech_recognition as sr

#####################################################################################
#To convert given audio input to texts
def audio_to_txt():

	# Input audio file to be sliced 
	audio = AudioSegment.from_wav("./Audio_Input/audioWAV.wav") 

	''' 
	Step #1 - Slicing the audio file into smaller chunks. 
	'''
	# Length of the audiofile in milliseconds 
	n = len(audio)
	print(n)

	# Variable to count the number of sliced chunks of audio
	counter = 1

	# Text file to write the recognized audio 
	fh = open("./Text_Output/recognized.txt", "w+") 

	# Interval length at which to slice the audio file. 
	# If length is 22 seconds, and interval is 5 seconds, 
	# The chunks created will be: 
	# chunk1 : 0 - 5 seconds 
	# chunk2 : 5 - 10 seconds 
	# chunk3 : 10 - 15 seconds 
	# chunk4 : 15 - 20 seconds 
	# chunk5 : 20 - 22 seconds 
	interval = 5 * 1000

	# Length of audio to overlap. 
	# If length is 22 seconds, and interval is 5 seconds, 
	# With overlap as 1.5 seconds, 
	# The chunks created will be: 
	# chunk1 : 0 - 5 seconds 
	# chunk2 : 3.5 - 8.5 seconds 
	# chunk3 : 7 - 12 seconds 
	# chunk4 : 10.5 - 15.5 seconds 
	# chunk5 : 14 - 19.5 seconds 
	# chunk6 : 18 - 22 seconds 
	overlap = 500

	# Initialize start and end seconds to 0 
	start = 0
	end = 0

	# Flag to keep track of end of file. 
	# When audio reaches its end, flag is set to 1 and we break 
	flag = 0

	# Iterate from 0 to end of the file, 
	# with increment = interval 
	for i in range(0, 2 * n, interval): 
		
		# During first iteration, 
		# start is 0, end is the interval 
		if i == 0: 
			start = 0
			end = interval 

		# All other iterations, 
		# start is the previous end - overlap 
		# end becomes end + interval 
		else: 
			start = end - overlap 
			end = start + interval 

		# When end becomes greater than the file length, 
		# end is set to the file length 
		# flag is set to 1 to indicate break. 
		if end >= n: 
			end = n 
			flag = 1

		# Storing audio file from the defined start to end 
		chunk = audio[start:end] 

		# Filename / Path to store the sliced audio 
		filename = 'chunk'+str(counter)+'.wav'

		# Store the sliced audio file to the defined path 
		chunk.export(filename, format ="wav") 
		# Print information about the current chunk 
		print("Processing chunk "+str(counter)+". Start = "
							+str(start)+" end = "+str(end)) 

		# Increment counter for the next chunk 
		counter = counter + 1
		
		# Slicing of the audio file is done. 
		# Skip the below steps if there is some other usage 
		# for the sliced audio files. 


		# ''' 
		# Step #2 - Recognizing the chunk and writing to a file. 
		# '''

		# Here, Google Speech Recognition is used 
		# to take each chunk and recognize the text in it. 

		# Specify the audio file to recognize 

		AUDIO_FILE = filename 

		# Initialize the recognizer 
		r = sr.Recognizer() 

		# Traverse the audio file and listen to the audio 
		with sr.AudioFile(AUDIO_FILE) as source: 
			audio_listened = r.listen(source) 

		# Try to recognize the listened audio 
		# And catch expections. 
		try:	 
			rec = r.recognize_google(audio_listened) 
			
			# If recognized, write into the file. 
			fh.write(rec+". ") 
		
		# If google could not understand the audio 
		except sr.UnknownValueError: 
			print("Could not understand audio") 

		# If the results cannot be requested from Google. 
		# Probably an internet connection error. 
		except sr.RequestError as e: 
			print("Could not request results.") 

		# Check for flag. 
		# If flag is 1, end of the whole audio reached. 
		# Close the file and break. 
		if flag == 1: 
			fh.close() 
			break
###############################################################################
# To Generate the Summary out of the meeting
def tsvFile():
	audio_to_txt()
	df = pd.read_csv("Text_Output/recognized.txt")
	df.to_csv('Text_Output/out.tsv')


def summerization(meeting_text):
    extra_words=list(STOP_WORDS)+list(punctuation)+['\n']
    nlp = spacy.load("en_core_web_sm")
    cleaned_text = nlp(meeting_text)
    all_words=[word.text for word in cleaned_text]

    Freq_word={}
    for w in all_words:
        w1=w.lower()
        if w1 not in extra_words and w1.isalpha():
            if w1 in Freq_word.keys():
                Freq_word[w1]+=1
            else:
                Freq_word[w1]=1

    val=sorted(Freq_word.values())
    max_freq=val[-3:]
    print("Topic of document given :-")
    for word,freq in Freq_word.items():  
        
        if freq in max_freq:
            print(word ,end=" ")
            
        else:
            continue
    
    print("\n\n")

    for word in Freq_word.keys():  
        Freq_word[word] = (Freq_word[word]/max_freq[-1])
    sent_strength={}
    for sent in cleaned_text.sents:
        for word in sent :

            if word.text.lower() in Freq_word.keys():

                if sent in sent_strength.keys():
                    sent_strength[sent]+=Freq_word[word.text.lower()]
                else:

                    sent_strength[sent]=Freq_word[word.text.lower()]

            else:
                continue
    top_sentences=(sorted(sent_strength.values())[::-1])

    top30percent_sentence=int(0.3*len(top_sentences))

    top_sent=top_sentences[:top30percent_sentence]

    summary=[]
    for sent,strength in sent_strength.items():
        if strength in top_sent:
            summary.append(sent)

        else:
            continue
    for i in summary:
        print(i,end="")

meeting = []
tsvFile()
with open('Text_Output/out.tsv') as tsvfile:
	reader = csv.reader(tsvfile, delimiter='\t')
	n = 0
	for row in reader:
		n += 1
		meeting.append(" ".join(row))
		if n == 100:
			break
summerization(" ".join(meeting))
##########################################################################
# Polarity to check if the meeting was a positive, negative or neutral discussion.
def Polarity():
    with open('Text_Output/out.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            pass


    polaSum = 0

    zen = TextBlob(row[0])
    # print(zen.words)
    totalSentences = len(zen.sentences)
    for i in range(totalSentences):
        print(type(zen.sentences[i]))
        testimonial = TextBlob(str(zen.sentences[i]))
        polarity = testimonial.sentiment.polarity
        print(polarity)
        polaSum += polarity
    print(f"The Polarity of the meeting is: {polaSum/totalSentences}")

Polarity()
##########################################################################################
# For Displaying the Word Highlights
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