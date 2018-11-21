from gensim import corpora, models, similarities
from nlp import markdown_to_text
from underthesea import word_tokenize
import time
import os
from mapper import MuhExKillEl,Mungen,POST_COLLECTION
from util import MODEL_NAME,DICT_NAME,CORPUS_NAME ,INDEX_NAME
#get all posts
mongo = Mungen()
mysql = MuhExKillEl()
texts = mysql.get_all_post_content()
stored = mongo.get_all_post_token()

id_to_token = {}
for item in stored:
    id_to_token[item['_id']] = item
    
#train token if not found
index = 0
data_insert = []
print("Inserting new document...")
for i,item in enumerate(texts):
    index += 1
    if index % 100 == 0:
        print(index)
        
    #skip if already converted
    if item['ID'] in id_to_token and 'token' in id_to_token[item['ID']]:
        continue
    
    content = item["post_content"]
    paras = content.split("\r\n")
    token_paragraph = []
    token_sentence = []
    for para in paras:
        para = markdown_to_text(para)
        if not para:
            continue
        sentences = para.split('.')
        current_paragraph = []
        for sentence in sentences:
            token = word_tokenize(sentence)
            token = [word.lower() for word in token]
            if not token or not sentence:
                continue
            token_sentence.append(token)
            current_paragraph.extend(token)
        if current_paragraph:
            token_paragraph.append(current_paragraph)
    item['token_paragraph'] = token_paragraph
    item['token_sentence'] = token_sentence   
    item['token'] = []
    for token in token_paragraph:
        item['token'].extend(token)
    item['_id'] = item['ID']
    item['index'] = i
    del item['ID']
    mongo.update_one(POST_COLLECTION,item['_id'],item,True)
    stored.append(item)

print("Done")

texts = []
query_texts = []
for i in range(len(stored)):
    texts.append(stored[i]['token'])
    texts.extend(stored[i]['token_paragraph'])
    query_texts.append(stored[i]['token'])
    
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below=5, no_above=0.8)
corpus = [dictionary.doc2bow(text) for text in texts]
query_corpus = [dictionary.doc2bow(text) for text in query_texts]

folder = "ver_{:0>3d}"
for i in range(1,10000):
    if os.path.isdir(folder.format(i)):
        continue
    folder = folder.format(i)
    break

dump_folder = 'temp_' + folder
if not os.path.isdir(dump_folder):
    os.mkdir(dump_folder)
if not os.path.isdir(folder):
    os.mkdir(folder)
    
dictionary.save_as_text(os.path.join(dump_folder,DICT_NAME))
print("dictionary saved in {}/dictionary.dict".format(dump_folder))
corpora.MmCorpus.serialize(os.path.join(dump_folder,CORPUS_NAME), query_corpus)
print("corpus saved in {}/corpus.mm".format(dump_folder))

before = time.time()
lda = models.LdaModel(corpus, num_topics=12, \
                                id2word=dictionary, \
                                update_every=5, \
                                chunksize=5000, \
                                passes=100,\
                                random_state=42)

lda.save(os.path.join(dump_folder,MODEL_NAME))
after = time.time()

print("model saved in {}/lda.model".format(dump_folder))
print("Took {}h".format(round((after - before) / 3600,2)))

index = similarities.MatrixSimilarity(lda[query_corpus])
index.save(os.path.join(dump_folder,INDEX_NAME))

os.rename(dump_folder,folder)