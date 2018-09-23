import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix

CLASSIFIER=joblib.load('model/classifier.pkl')
TDIDF_TRANSFORMER=joblib.load('model/tdidf_transformer.pkl')
COUNT_VECT=joblib.load('model/count_vect.pkl')

LANGUAGES=['en','sv','de','fr','nl','ru','it','es','pl','vi','pt','uk','fa','sco']

TEST_DATA=[]

for language in LANGUAGES:
    TEST_DATA.append(
        np.array([open('scraper/data/'+language+'/TEST_SET.db').read()])
    )


def get_chunks(lang, size=30):
    for i in range(0,len(lang),size):
        yield ' '.join(lang[i+i +size])


ACTUAL=[]

PREDICTED=[]

index=-1

for language in TEST_DATA:
    index +=1

    chunks = get_chunks(language[0].split())
    chunks=[i for i in chunks]

    TEST_COUNTS=COUNT_VECT.transform(chunks)
    TEST_TFIDF=TDIDF_TRANSFORMER.transform(TEST_COUNTS)
    PREDICTED=CLASSIFIER.predict(TEST_TFIDF)

    for chunk in chunks:
        ACTUAL.append(index)

def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Reds):
    plt.imshow(cm,interpolation='nearest', cmap=cmap)
    plt.title(title)
    tick_marks=np.arange(len(classes))
    plt.xticks(tick_marks,classes)
    plt.yticks(tick_marks,classes)

    fmt='d'
    thresh=cm.max()/2

    for i, j in itertools.product(range(cm.shape[0]),range(cm.shape[1])):
        plt.text(j,i,format(cm[i,j],fmt),
                 horizontalalignment='center',
                 color="white" if cm[i,j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True Class')
        plt.xlabel('Predicted Class')


cnf_matrix=confusion_matrix(ACTUAL,PREDICTED)

plt.figure()

class_names=LANGUAGES

plot_confusion_matrix(cnf_matrix,classes=class_names,title='Confusion matrix')

plt.show()