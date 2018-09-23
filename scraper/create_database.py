import subprocess
from os import listdir
from os.path import join
from get_data import GetArticles, Database
import sys
sys.path.append('..')
from languages import LANGUAGES

WORDS=40000
DATABASE_LOCATION='data'

class DataBaseWriter(object):
    def __init__(self,db_root_location):
        self.getdata=GetArticles()
        self.db_root_location=db_root_location

    def _count_words_in_language(self,language):
        words=0
        language_data_folder=join(self.db_root_location, language)
        contents=listdir(language_data_folder)
        articles=[article for article in contents if article[-3:]=='txt']
        for article in articles:
            with open(join(language_data_folder,article),'r') as text:
                for line in text:
                    for _ in line.split(' '):
                        words+=1


        return words

    def _get_words_in_language(self,language):
        words=[]
        language_data_folder=join(self.db_root_location,language)
        contents=listdir(language_data_folder)
        articles=[article for article in contents if article[-3:]=='txt']
        for article in articles:
            with open(join(language_data_folder,article),'r') as text:
                for line in text:
                    for word in line.split(' '):
                        words.append(word)

        return words

    def dbwrite(self,language, sql_database, words):
        print ('checking '+language+' articles')
        language_data_folder=join(self.db_root_location,language)
        train_ratio=.9

        if language not in listdir(self.db_root_location):
            subprocess.run(["mkdir",language_data_folder])

        while self._count_words_in_language(language)<words:
            print ('....downloading more words..not enough: ',self._count_words_in_language(language))
            self.getdata.write_articles(language,25,language_data_folder)

        all_words=self._get_words_in_language(language)[:words]
        split=int(train_ratio*words)
        training_set=all_words[split:]
        test_set=all_words[:split]

        sql_database.write_categories(language,' '.join(training_set), ' '.join(test_set))


if __name__=="__main__":
    SQLDB_NAME='language_data'
    SQLDB=Database(SQLDB_NAME)

    TEXTFILES=DataBaseWriter(DATABASE_LOCATION)

    for lang in LANGUAGES:
        TEXTFILES.dbwrite(lang,SQLDB, WORDS)