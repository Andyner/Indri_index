#!/bin/bash
cd /home/dingyong/deal_kol/kol_search/pre_index
#rm /home/dingyong/deal_kol/kol_search/raw_data_from_mysql/kol_search*
echo '==start weibo=='
/bin/python pre_index_weibo.py
echo '==end weibo=='
echo
echo '==start weixin=='
/bin/python pre_index_weixin.py
echo '==end weixin=='
echo
echo '==start zl=='
/bin/python pre_index_zl.py
echo '==end zl=='
