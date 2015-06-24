#!/bin/bash
echo 'start pre_index ...'
rm /home/dingyong/deal_kol/kol_search/raw_data_from_mysql/kol_search*
cd /home/dingyong/deal_kol/kol_search/pre_index/
/bin/sh run.sh
echo 'rm old index ...'
rm -r /disk1/kol_search_index/index
echo 'build index ...'
cd /home/dingyong/deal_kol/kol_search/build_index/
/bin/sh run.sh
echo 'Done!!!'

