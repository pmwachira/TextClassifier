import re
import json
import requests
from sqlalchemy import Table, Column, Text, String, MetaData, create_engine
import codecs
from languages import ENCODINGS

class GetArticles(object):
    def __init__(self):
        pass
    def _get_random_article_ids(self,language_id,number_of_articles):

        query=\
                'https://'+language_id\
                +'.wikipedia.org/w/api.php?format=json&action=query&list=random&rnlimit='\
                +str(number_of_articles)+'&rnnamespace=0'

        data = json.loads(requests.get(query).text)

        ids=[]
        for article in data['query']['random']:
            ids.append(article['id'])

        return ids

    def _get_article_text(self,language_id,article_id_list):

        for idx in article_id_list:
            idx=str(idx)

            query= \
                    'https://'+language_id\
                    +'.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&pageids='\
                    +idx+'redirects=true'

            data=json.loads(requests.get(query).text)

            try:
                title=data['query']['pages'][idx]['title']
                text_body=data['query']['pages'][idx]['extract']

            except KeyError as error:
                print(error)
                continue

            def clean(text):
                match_tag=re.compile(r'(<[^>]+>|\[\d+\]|[,.\'\"()])')
                return match_tag.sub('',text)

            yield title, clean(text_body)


    def write_articles(self,language_id,number_of_articles,db_location):
        articles=self._get_random_article_ids(language_id,number_of_articles)
        text_list=self._get_article_text(language_id,articles)

        for title, text in text_list:
            title=''.join(x for x in title if x.isalnum())
            for enc_type in ENCODINGS:
                with codecs.open(db_location+'/'+title+'.txt','w+',errors ='ignore',encoding=enc_type) as wikipedia_file:
                    wikipedia_file.write(text)

class Database(object):
    def __init__(self,database_name):
        self.engine = create_engine('sqlite:///'+database_name+'.db')
        self.metadata=MetaData()

        self.train = Table('train',self.metadata,
                           Column('language',String, primary_key=True),
                           Column('text',Text))

        self.test=Table('test',self.metadata,
                        Column('language',String, primary_key=True),
                        Column('text',Text))

        self.metadata.create_all(self.engine)

    def write_categories(self,language, training_text, test_text):
        conn= self.engine.connect()

        del1= self.train.delete().where(self.train.columns.language==language)
        del2= self.test.delete().where(self.test.columns.language==language)

        conn.execute(del1)
        conn.execute(del2)

        ins1=self.train.insert().values(
            language=language,
            text=test_text
        )

        ins2=self.test.insert().values(
            language=language,
            text=test_text
        )

        conn.execute(ins1)
        conn.execute(ins2)

