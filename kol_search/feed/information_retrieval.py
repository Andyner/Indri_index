#!/usr/bin/python
# -*- coding: utf-8 -*-

from feed_util import process_keywords
# keys_for_extract=['DOCNO','author','clean_text','title','date','quality_rank','page_type']
keys_for_extract=['DOCNO','site']
keys_for_replace=['NZ_PP','NZ_CS','NZ_CX']

def find_tag_content(text,tag):
    if not text:
        return ''
    if not tag:
        return text
    if isinstance(text,unicode):
        text=text.encode('utf8',errors='ignore')
    if isinstance(tag,unicode):
        tag=tag.encode('utf8',errors='ignore')

    start_pos=text.find('<%s>'%tag)+len('<%s>'%tag)
    end_pos=text.find('</%s>'%tag)
    return text[start_pos:end_pos]

def _get_title(title):
    if not title:
        return ''
    for key in keys_for_replace:
        title=title.replace('<%s>'%key, ' ')
        title=title.replace('</%s>'%key, ' ')
        del key
    return title.replace(' ','')

def _get_snippet(text,num=200):
    if not text:
        return ''
    for key in keys_for_replace:
        text=text.replace('<%s>'%key,'')
        text=text.replace('</%s>'%key, '')
    text=text.replace(' ','')

    if isinstance(text,str):
        text=text.decode('utf8',errors='ignore')
    result=text[:min(num,len(text))]
    del text
    return result.encode('utf8',errors='ignore')

def get_one_result(doc_text):
    """
    paras: doc_text: trectext
    return: title,abstract,author,date
    """
    result=dict()
    for key in keys_for_extract:
        if isinstance(key,unicode):
            key=key.encode('utf8',errors='ignore')
        
        tmp=find_tag_content(doc_text,key)
        if key=='DOCNO':
            result['userid']=tmp
        elif key=='site':
            result['site']=tmp
    return result

def get_desc_sentence(sentences,flag):
    res = []
    for sentence in sentences:
        pos = sentence.find(flag)
        if pos==-1 :
            res.append(sentence)
            continue
        tmp = sentence[:pos+1]
        tmp1 = sentence[pos+1:]
        res.extend([tmp,tmp1])
    return res

def get_desc_sentence2(sentences,flag):
    res = []
    for sentence in sentences:
        while True:
            pos = sentence.find(flag)
            if pos==-1 :
                res.append(sentence)
                break
            tmp = sentence[:pos+1]
            sentence = sentence[pos+1:]
            res.append(tmp)
    return res
    
def get_sentence(content):
    if isinstance(content,str):
        content = content.decode('utf-8','ignore')
    content = content.replace(' ','')
    flags = ['。','！','？','?','!','\n']
    flags = [flag.decode('utf-8') for flag in flags]
    sentences = []
    flag = flags[0]
    while True:
        pos = content.find(flag)
#         print pos
        if pos==-1 or len(content)==0:
            sentences.append(content)
            break
        sentence = content[:pos+1]
        sentences.append(sentence)
        content = content[pos+1:]
    for flag in flags[1:]:
        sentences = get_desc_sentence2(sentences,flag)
    return sentences
    
def get_abs(doc_text,keywords):
    start_pos=doc_text.find('<s>')+len('<s>')
    end_pos=doc_text.find('</s>')
    content = doc_text[start_pos:end_pos]
    sentences = get_sentence(content)
#     for sentence in sentences:
#         print sentence
#         print '---'
    keywords = process_keywords(keywords)
    keylist = []
    if len(keywords)==0:
        return None
    elif len(keywords)==1:
        keywords = keywords[0].decode('utf-8','ignore')
        keylist.extend([keywords,keywords,keywords])
    elif len(keywords)>1:
        keywords = [keyword.decode('utf-8','ignore') for keyword in keywords]
        if len(keywords) == 2:
            keylist.extend(keywords.append(keywords[0]))
        else:
            keylist.extend(keywords[:3])
    result = []
#     print keylist
    for key in keylist:
        for sentence in sentences:
            pos = sentence.find(key)
            if pos!=-1:
                result.append(sentence)
                sentences.remove(sentence)
                break
    result = [s.encode('utf-8') for s in result]
    return '... '.join(result)+'...'
# res = get_abs(doc_text,'自由')
# print res
# for s in res:
#     print s
# get_one_result(doc_text)

def get_query_results(query_index,docs):
    """
    @query_index:索引
    @docs
    return:title,abstract,author,date,relevance
    """
    #print 'docs: ',docs
    for doc in docs:
        relevance=getattr(doc,'score')
        doc_id=getattr(doc,'document')  
#         if not relevance or not doc_id:
#             continue
        if not doc_id:
            continue
        try:
            doc_obj=query_index.documents([doc_id])[0]
            doc_text=doc_obj.text
	    #print doc_text
            #doc_text:为创建索引时的pre_index
            result=get_one_result(doc_text)
            result['relevance']=relevance
#             result['url']=doc_obj.metadata['DOCNO']
            yield result
        except Exception,e:
            print e
