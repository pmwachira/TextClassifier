import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sqlalchemy import create_engine
import os

LANGUAGES=['en','sv','de','fr','nl','ru','it','es','pl','vi','pt','uk','fa','sco']

TRAINING_DATA=[]

db=create_engine('sqlite:///../scraper/language_data.db')
conn=db.connect()
res=conn.execute('select * from train')
for row in res:
    TRAINING_DATA.append(row['text'])

TRAINING_SET=np.array(TRAINING_DATA)

TARGETS=np.array([i for i in range(len(LANGUAGES))])

COUNT_VECT=CountVectorizer()
TRAIN_COUNTS=COUNT_VECT.fit_transform(TRAINING_SET)

TFIDF_TRANSFORMER=TfidfTransformer()
TRAIN_TFIDF=TFIDF_TRANSFORMER.fit_transform(TRAIN_COUNTS)

CLASSIFIER=MultinomialNB().fit(TRAIN_TFIDF,TARGETS)

joblib.dump(COUNT_VECT,'count_vect.pkl')
joblib.dump(TFIDF_TRANSFORMER,'tdidf_transformer.pkl')
joblib.dump(CLASSIFIER,'classifier.pkl')