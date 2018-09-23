from sklearn.externals import joblib
from languages import LANGUAGES

CLASSIFIER=joblib.load('model/classifier.pkl')
TDIDF_TRANSFORMER=joblib.load('model/tdidf_transformer.pkl')
COUNT_VECT=joblib.load('model/count_vect.pkl')

LANGUAGE_MAPPING={14:"undetermined"}

for index, language in enumerate(LANGUAGES):
    LANGUAGE_MAPPING[index]=language

def identify(phrase):
    counts=COUNT_VECT.transform([phrase])
    tfidf=TDIDF_TRANSFORMER.transform(counts)
    predicted=CLASSIFIER.predict(tfidf)

    return LANGUAGE_MAPPING[predicted[0]]
