# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/17 18:11
# @IDE:         PyCharm

import re
# import html
import lxml
from lxml import html
if __name__ == "__main__":
    str = "&#xeb56;&#xe1ca;&#xf4ca;&#xe049"
    print(str.replace('.', '').replace(';', '').replace('&#x', '\\u').encode('utf-8').decode('unicode_escape'))
    # print(html.unescape(str))
    print(b'\u4e2d\u6587'.decode('unicode-escape'))
    print(lxml.html.fromstring("&#xf412;").text)