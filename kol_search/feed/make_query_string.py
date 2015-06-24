#encoding:utf-8
import datetime
from feed_util import process_keywords
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def make_query_string(keywords,site='0'):
    ##filreq(#band(#datebetween(05/26/2015 06/02/2015) 长安 福特) #weight(2.0 #2(长安 福特).(title) 1.0 #2(长安 福特).(s)))
    ##filreq(长安 福特  #weight(2.0 #2(长安 福特).(title) 1.0 #2(长安 福特).(s)))
    
    query_string='#filreq( %s #weight(%s))'
    
    #根据权重排序
    keywords = jieba.cut(keywords)
    keywords = ' '.join(keywords).strip()
    keywords = process_keywords(keywords)
    if int(site)==0:
        reqstr = '#band(%s)'%(' '.join(keywords).encode('utf-8','ignore'))
    else:
        reqsite = '#equals(site %s)'%(site)
        reqstr = '#band(%s %s)'%(reqsite,' '.join(keywords).encode('utf-8','ignore'))
    if len(keywords)==0:
        return None
    elif len(keywords)==1:
        keywords = keywords[0].encode('utf-8','ignore')
        weitht = '10.0 %s.(userid) 10.0 %s.(author) 2.0 %s.(abs) 2.0 %s.(authenticate) 1.0 %s.(hot)'%(keywords,keywords,keywords,keywords,keywords)
    elif len(keywords)>1:
        length = len(keywords)
        keywords = [keyword.encode('utf-8','ignore') for keyword in keywords]
        keywords = ' '.join(keywords)
        weitht = '10.0 #%s(%s).(userid) 10.0 #%s(%s).(author) 2.0 #%s(%s).(abs) 2.0 #%s(%s).(authenticate) 1.0 #%s(%s).(hot)'%(length,keywords,length,keywords,length,keywords,length,keywords,length,keywords)
    query_string = query_string%(reqstr,weitht)
    return query_string

# print make_query_string('长安福特')
