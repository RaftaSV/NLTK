import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import sent_tokenize, word_tokenize

url = "https://en.wikipedia.org/wiki/Machine_learning"
html = urllib.request.urlopen(url).read().decode('utf-8')
text = get_text(html)
article_text = text
article_text = article_text.replace("[ edit ]", "")
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('English')

word_frequencies = {}

for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1


# calcula las frecuencias de las palabras
sentence_scores = {}
# for es un bucle que itera sobre una lista
for sent in sentence_list:
    # for es un bucle que itera sobre una lista
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

maximum = max(word_frequencies.values())
# for es un bucle que itera sobre una lista
for sent in sentence_scores.keys():
    # sentence_scores se actualiza con la frase y su frecuencia
    sentence_scores[sent] = (sentence_scores[sent]/maximum)
       
# retorna el resumen
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)
print(summary)