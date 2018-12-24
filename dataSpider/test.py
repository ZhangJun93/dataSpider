# -*- coding: utf-8 -*-
import re
import time
#
# url = 'http://www.cmbchina.com/cmbinfo/news/?PcgeNo=2/index'
# match = re.match("(.*/)index.*", url)
# print match.group(1)
#
# date = "2018年05月07日"
# dateArray = time.strptime(date, "%Y年%m月%d日")
# otherStyleDate = time.strftime("%Y-%m-%d", dateArray)
# print otherStyleDate
# url = 'http://www.jiqirenku.com/2018/11/11/35190.html'
# match = re.match(".*com/([0-9]*)/([0-9]*)/([0-9]*)/.*html", url)
# if match:
#     date = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
#     print date
#
#
# import numpy as np
#
# list = [1, 3, 6, 7, 3, 8, 8, 1, 6, 3]
# unque, count = np.unique(list,return_counts=True)
# print unque,count
# print  np.array([0, 3])



# import scipy.sparse as sp
# import numpy as np
# indptr = np.array([0, 2, 3, 6])
# indices = np.array([0, 2, 2, 0, 1, 2])
# data = np.array([1, 2, 3, 4, 5, 6])
# print sp.csr_matrix((data, indices, indptr), shape=(3, 3)).toarray()
#
# cnts = np.array([[1,5,7,9.2,-5, -3,6]])
# print (cnts > 0).astype(int)

import difflib

score = difflib.SequenceMatcher(a=u"上海迪士尼可以带吃的进去吗",b=u"完全密封的可以，其它不可以。")
print score.ratio()
a = "avce"
if 'c' in a:
    print "0x9a"
import re
c = "[发布日期： 2018-03-07]"
match = re.search(r'([0-9-]+)',c)
print match.group(1)

# print time.strftime("%Y-%m-%d", time.localtime(time.time()))
# for i in range(1, 6+1):
#     print i
# url = "http://jrb.xinjiang.gov.cn/xwdt/index_1.htm"
# # url = "http://www.xinjr.com/caijing/caijingzixun/2018-12-11/632518.html"
# match = re.match(r'.*/index', url)
# if match:
#     print "ok"
# else:
#     print "no"
url = 'http://www.abchina.com/cn/AboutABC/nonghzx/NewsCenter/201811/t20181102_1703026.htm'
match = re.search(r't([0-9]+)_', url)
date_str = match.group(1)
date = date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:8]
print date

t = 'http://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7158/7162/list_1.shtml?channelId=7158'
t.replace("_.*.shtml", "xxx")

match_url = re.search(r'(.*list_)[0-9]+(\.shtml.*)', t)

end_url_index = int(3)
for i in range(1, end_url_index + 1):
    next_url = match_url.group(1) + str(i) + match_url.group(2)
    print next_url
