#encoding:utf-8
import jieba
import datetime
import time
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import mysql_api as mysql
import config

def _tag_text(tag,text):
    return '<%s>%s</%s>'%(tag,text,tag)

def process_content(content):
    word_list=jieba.cut(content.strip())
    content = ' '.join(word_list).strip()
    return content.encode('utf-8','ignore')

class HandeData():
    
    filetag = 'weixin' 
    site = 2
    
#     error_path = config_for_weixin.error_path
    data_path = config.zl_data_path
    def __init__(self):
        self.conn = mysql.connect('mx_kol')
        self.flag = 1
        timetag = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.f = open('%s/kol_search_%s_%s.dat'%(self.data_path,self.filetag,timetag),'w')
        self.total = 0
        
    def fetch_raw_data(self):
        sql = 'select userid,screen_name,status_hot_words from weixin_kol;'
        cur = self.conn.cursor()
        cur.execute(sql)
        datas = cur.fetchall()
        return datas
    
    def fetch_excess_data(self,userid):
        sql = "select verified_reason,description from weixin_user_info where userid='%s';"%(userid)
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        return data
    
    def process_hot_words(self,hot_words):
        if not hot_words:
            return ''
        hot_word_tmp = json.loads(hot_words)
        hot_words = []
        for word in hot_word_tmp.iterkeys():
            hot_words.append(word)
        return ' '.join(hot_words)
    
    def write_to_file(self,res):
        if self.flag%1000==0:
            self.f.close()
            self.flag = 1
            timetag = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#             self.f = open('./data/%s/web_kol_%s_%s.dat'%(self.filetag,self.filetag,timetag),'w')
            self.f = open('%s/kol_search_%s_%s.dat'%(self.data_path,self.filetag,timetag),'w')
        else:
            self.flag += 1
        self.total += 1
        result = []
        result.append('<DOC>')
        result.append(_tag_text('DOCNO', res['DOCNO']))
        result.append('<TEXT>')
        result.append(_tag_text('author',res['author']))
        result.append(_tag_text('userid',res['userid']))
        result.append(_tag_text('site',res['site']))
        result.append(_tag_text('abs',res['abs']))
        result.append(_tag_text('authenticate',res['authenticate']))
        result.append(_tag_text('hot',res['hot']))
        result.append('</TEXT>')
        result.append('</DOC>')
        data = '\n'.join(result)
        self.f.write('%s\n'%(data))
        self.f.flush()
        
    def process(self):
        datas = self.fetch_raw_data()
        res = dict()
        for data in datas:
            userid = data[0]
            res['DOCNO'] = userid
            res['author'] = process_content(data[1])
            res['userid'] = process_content(userid)
            res['hot'] = self.process_hot_words(data[2])
            res['site'] = self.site
            excess_data = self.fetch_excess_data(userid)
            try:
                res['abs'] = process_content(excess_data[1])
            except:
                res['abs'] = ''
            try: 
                res['authenticate'] = process_content(excess_data[0])
            except:
                res['authenticate'] = ''
            self.write_to_file(res)
        mysql.close(self.conn)
        return self.total

if __name__ == '__main__':
    handle = HandeData()
    total = handle.process()
    print total

