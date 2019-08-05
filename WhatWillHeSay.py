import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re
import pyodbc
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ADARSH;'
                      'Database=TrumpSpeeches;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute("SELECT STitle, SContent FROM Speeches")

speechList = list()
lemmatization = nltk.WordNetLemmatizer()
for row in cursor:
    speech = row[1]
    speech = re.sub("[^a-zA-Z]", " ", speech)
    speech = speech.lower()
    speech = nltk.word_tokenize(speech)
    speech = [i for i in speech if i not in set(stopwords.words("english"))]
    omitList = ['mr president', 'president', 'applause', 'mr', 'q', 'u']
    speech = [i for i in speech if i not in omitList]
    speech = [lemmatization.lemmatize(i)for i in speech]
    speech = " ".join(speech)
    speechList.append(speech)
    speechWordCloud = WordCloud(width=1600, height=1200, max_font_size=120, max_words=100).generate(text=speech)
    plt.imshow(speechWordCloud, interpolation='bilinear')
    plt.axis("off")
    # plt.show()
    # plt.savefig("img/" + row[0] + ".png", figsize=(20, 10), format="png")

allSpeeches = ' '.join(speechList)
allSpeechesWordCloud = WordCloud(width=1600, height=1200, max_font_size=120, max_words=100).generate(allSpeeches)
plt.imshow(allSpeechesWordCloud, interpolation='bilinear')
plt.axis("off")
# plt.show()
plt.gcf().clear()
# plt.savefig("img/allSpeeches.png", figsize=(20, 10), format="png")

wordCounter = dict()
words = allSpeeches.split()
for word in words:
    if word in wordCounter:
        wordCounter[word] += 1
    else:
        wordCounter[word] = 1

# wordCounter = sorted(wordCounter.items(), key=operator.itemgetter(1), reverse=True)
# print(wordCounter)
wordCounter = Counter(wordCounter)
wordCounter.most_common()
topWords = dict()
for k, v in wordCounter.most_common(100):
    topWords[k] = v
print(topWords)
sns.barplot(list(topWords.values()), list(topWords.keys()))
# plt.xticks(rotation=90)
figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
# plt.show()

# bow_transformer = CountVectorizer().fit([allSpeeches])
# print(bow_transformer.vocabulary_)
# speeches_bow = bow_transformer.transform(speechList)
# print("Shape of Sparse Matrix: ", speeches_bow.shape)
# # print(len(bow_transformer.vocabulary_))
# speech2 = [speechList[2]]
# bow2 = bow_transformer.transform(speech2)
# print(bow2.shape)

