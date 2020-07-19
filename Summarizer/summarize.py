import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

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

if __name__=="__main__":
    import csv
    meeting = []
    with open('out.tsv') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        n = 0
        for row in reader:
            n += 1
            meeting.append(" ".join(row))
            if n == 100:
                break
    summerization(" ".join(meeting))
