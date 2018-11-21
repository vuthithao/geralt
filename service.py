# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:27:48 2018

@author: MinhNguyen
"""
from nlp import markdown_to_text,remove_punctuation
from util import get_model,convert_to_token, get_index_to_id
from mapper import Mungen,MuhExKillEl
mongo = Mungen()
mysql = MuhExKillEl()
GRAY_LOG_URL = '42.113.207.172'
NOT_TRAINED_CODE = '1415'
class NotTrainedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        
def query(aid):
    
    #try query
    recommend = mongo.get_recommend(int(aid))
    if recommend is not None and 'recommend' in recommend:
        result = recommend['recommend']
        if str(result[0][0]) == str(aid):
            result = result[1:]
        return result
        #TODO update this
#    query_res = mysql.get_post_conent(aid)
#    if not query_res:
#        raise ValueError("Không tìm thấy ID: {}".format(aid))
        

    raise NotTrainedError("ID này chưa được train: {}, code: {}".format(aid,NOT_TRAINED_CODE))

    model,dictionary,corpus,index = get_model()
    index_to_id = get_index_to_id()
    content = query_res[0]['post_content']
    text = markdown_to_text(content)
    text = remove_punctuation(text)
    
    tokens = convert_to_token(text)
    vec_bow = dictionary.doc2bow(tokens)
    vec_lda = model[vec_bow]
    sims = index[vec_lda]
    
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    res = []
    for sim in sims[:12]:
        if str(sim[0]) == str(aid):
            continue
        res.append({
                    "id" : index_to_id[sim[0]],
                    "score" : str(round(sim[1],2))
                })
    return res

"""
([(0, 1.0),
  (7906, 0.98011696),
  (7842, 0.97625023),
  (1623, 0.96912104),
  (5819, 0.9668543)],
 0)
"""