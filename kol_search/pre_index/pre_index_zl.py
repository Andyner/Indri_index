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
    
    filetag = 'zl' 
    site = 4
    
#     error_path = config_for_weixin.error_path
    data_path = config.zl_data_path
    def __init__(self):
        self.conn = mysql.connect('mx_kol')
        self.flag = 1
        timetag = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.f = open('%s/kol_search_%s_%s.dat'%(self.data_path,self.filetag,timetag),'w')
        self.total = 0
        
    def fetch_raw_data(self):
        sql = 'select userid,screen_name,description from zl_user_info;'
        cur = self.conn.cursor()
        cur.execute(sql)
        datas = cur.fetchall()
        return datas
    
    def fetch_hot_words(self,userid):
        sql = "select status_hot_words from zl_kol where userid='%s';"%(userid)
        cur = self.conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if not data:
            return ''
        if not data[0]:
            return ''
        hot_word_tmp = json.loads(data[0])
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
            res['abs'] = process_content(data[2])
            res['hot'] = self.fetch_hot_words(userid)
            res['site'] = self.site
            res['authenticate'] = ''
            self.write_to_file(res)
        mysql.close(self.conn)
        return self.total

if __name__ == '__main__':
    handle = HandeData()
    total = handle.process()
    print total

