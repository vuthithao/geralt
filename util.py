from gensim import corpora, models, similarities
from underthesea import word_tokenize
from mapper import Mungen
import os

MODEL_NAME = 'lda.model'
DICT_NAME = 'dictionary.dict'
CORPUS_NAME = 'corpus.mm'
INDEX_NAME = 'index.index'

model = None
dictionary = None
corpus = None
version = None
index_to_id = None
index = None
mongo = Mungen()

def get_folder():
    return [path for path in os.listdir() if os.path.isdir(path) and path.startswith('ver_')]

def load_stuff(folder):
    for path in sorted(folder,reverse=True):
        try:
            model = models.LdaModel.load(os.path.join(path,MODEL_NAME))
            dictionary = corpora.Dictionary.load_from_text(os.path.join(path,DICT_NAME))
            corpus = corpora.MmCorpus(os.path.join(path,CORPUS_NAME))
            index = similarities.MatrixSimilarity.load(os.path.join(path,INDEX_NAME))
            return model,dictionary,corpus,index
        except:
            print("Error loading {}, using older verion...".format(path))
            
def get_model():
    global model
    global version
    global dictionary
    global corpus
    global index
    folder = get_folder()
    new_version = sorted(folder,reverse=True)[0]
    if model is None or version != new_version:
        version = new_version
        model,dictionary,corpus,index = load_stuff(folder)
    return model,dictionary,corpus,index
        
def convert_to_token(sentence):
    return word_tokenize(sentence)

def get_index_to_id():
    global mongo
    global index_to_id
    if index_to_id is None or len(index_to_id) != mongo.post_count():
        query_res = mongo.get_all_post_token(field={"index" : 1})
        index_to_id = {item["index"] : item['_id'] for item in query_res}
    return index_to_id

model,dictionary,corpus,index = get_model()
index_to_id = get_index_to_id()