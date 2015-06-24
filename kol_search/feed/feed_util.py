#encoding:utf-8
import re

from special_chars_tool import get_special_chars
space_re = re.compile(u"(\s){2,}")
special_chars=get_special_chars()

def process_keywords(keywords):
    '''
    This function will process the standard name to make it for lemur query
    '''
    if isinstance(keywords,str):
        keywords = keywords.decode('utf8',errors='ignore')
    elif isinstance(keywords,unicode):
        pass
    else:
        return

    other_chars = [u'(',u')',u'·',u'-']
    for char in other_chars:
        keywords = keywords.replace(char,u' ')
    for char in special_chars:
        keywords = keywords.replace(char,u' ')
    keywords = space_re.sub(u' ',keywords)
    return keywords.split()
