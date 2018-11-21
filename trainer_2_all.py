# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 10:28:58 2018

@author: MinhNguyen
"""

from util import get_model, get_index_to_id
from mapper import Mungen,POST_COLLECTION
import json
mongo = Mungen()
model,dictionary,corpus,index = get_model()
index_to_id = get_index_to_id()
stored = mongo.get_all_post_token(field={"token" : 1})
for i,item in enumerate(stored):
    if i % 500 == 0:
        print(i)
    token = item['token']
    vec_bow = dictionary.doc2bow(token)
    vec_lda = model[vec_bow]
    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    update_data = [(index_to_id[data[0]],str(round(data[1],2))) for data in sims[:20]]
    mongo.update_one(POST_COLLECTION,item['_id'],{"recommend" : update_data})

with open("update_data",'w') as file:
    json.dump(update_data,file)