#encoding:utf-8
import datetime
import time
from pymur import QueryEnvironment
from math import exp
import jieba
import json

from information_retrieval import get_query_results
from make_query_string import make_query_string
import mysql_api as mysql 
#filreq(#syn( 3.category 4.category 5.category 10.category 11.category ) #weight(1.0 #prior(QualityRank) 0.5 #combine(#wsum( 2.0 #3(福特 林肯 MKC).(keywords)  0.5 #3(福特 林肯 MKC).nz_cx 0.1 #3(福特 林肯 MKC)) #wsum( 2.0 #any:nz_sx_price.(keywords)  0.5 #any:nz_sx_price 0.1 价格))))
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def process_relevance(relevance):
    return min(int(exp(relevance)*1000000),1000000)
    
class FeedData():
    
    def __init__(self,keyword,site=0):
        self.keyword = keyword
        self.site = site
        
    #根据query_string查询结果
    def fetch_query_results(self,query_string,num=200):
        index_path = '/disk1/kol_search_index/index'
        query_index = QueryEnvironment()
        query_index.addIndex(index_path)
        #根据query_string查询结果
        #print query_string
        docs = query_index.runQuery(query_string,num)
        #解析查询的结果
        results = get_query_results(query_index,docs)
        datas = {}
        flag = 0
        conn = ''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flag = 0
        for result in results:
            if flag>=200:
                break
            data = {}
            userid = result['userid']
            site = result['site']
            relevance = process_relevance(result['relevance'])
            data.update({'userid':userid})
            data.update({'site':site})
            data.update({'relevance':relevance})
            datas.update({flag:data})
            flag += 1
        if datas:
            conn = mysql.connect('kol_search')
            results = json.dumps(datas)
            results = conn.escape_string(results)
            query = str(self.keyword)+'#$#'+str(self.site)
            sql = "insert into search_result_cache(query,result,update_time) values('%s','%s','%s');"%(query,results,now)
	    #print sql
            mysql.insert(conn, sql)
            mysql.commit(conn)
            mysql.close(conn)
            query_index.close()
        return datas
    
    def process(self):
        #query_string = '#filreq( #band(#equals(site 1) 冷兔) #weight(5.0 冷兔.(DOCNO) 5.0 冷兔.(author) 2.0 冷兔.(abs) 2.0 冷兔.(authenticate) 1.0 冷兔.(hot)))'
        query_string = make_query_string(self.keyword,self.site)
        results = self.fetch_query_results(query_string)
        #print results
        return json.dumps(results)

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print 'Error:Need two params!!!'
        sys.exit()
    #keyword:utf-8编码
    keyword = sys.argv[1]
    site = sys.argv[2]
    feed = FeedData(keyword,site)
    datas = feed.process()
    print datas
#         keywords = ['老王','老王','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','卡娃微卡','卡娃微卡','卡娃微卡','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','王兮兮Shirley','卡娃微卡','卡娃微卡','卡娃微卡']
#     keywords = ['冷兔']
#     flag = 0
#     for keyword in keywords:
#         site = '0'
#         feed = FeedData(keyword)
#         time.sleep(0.1)
#         datas = feed.process()
#         print datas
        
        
        

