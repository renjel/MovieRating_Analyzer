# -*- coding: utf-8 -*-
# @Author:      lirj
# @Date:        2020/3/17 18:11
# @IDE:         PyCharm

import re
# import html
import lxml
from lxml import html
if __name__ == "__main__":
    # str = "&#xeb56;&#xe1ca;&#xf4ca;&#xe049"
    # print(str.replace('.', '').replace(';', '').replace('&#x', '\\u').encode('utf-8').decode('unicode_escape'))
    # # print(html.unescape(str))
    # print(b'\u4e2d\u6587'.decode('unicode-escape'))
    # print(lxml.html.fromstring("&#xf412;").text)

    # a = [2, 3, 4, 5]
    # b = [8]
    # tmp = [val for val in a if val in b]
    # print(tmp)
    # # [2, 5]
    #
    # # 方法二
    # print(list(set(a).intersection(set(b))))

    str = '''{
  "@context": "http://schema.org",
  "name": "游侠情 遊俠情",
  "url": "/subject/1531948/",
  "image": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2509467069.webp",
  "director": 
  [
    {
      "@type": "Person",
      "url": "/celebrity/1432102/",
      "name": "龙逸升 Tang Tak-Cheung"
    }
  ]
,
  "author": 
  [
    {
      "@type": "Person",
      "url": "/celebrity/1432102/",
      "name": "龙逸升 Tang Tak-Cheung"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1003376/",
      "name": "梁羽生 Yusheng Liang"
    }
  ]
,
  "actor": 
  [
    {
      "@type": "Person",
      "url": "/celebrity/1016847/",
      "name": "惠英红 Kara Wai Ying Hung"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1014913/",
      "name": "何家劲 Kenny Ho"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1028360/",
      "name": "陈观泰 Kuan Tai Chen"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1297716/",
      "name": "薛春炜 Ailen Sit"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1351454/",
      "name": "李耀景 Yiu Ging Lee"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1290162/",
      "name": "刘家荣 Chia Yung Liu"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1323182/",
      "name": "龙天翔 Tien Hsiang Lung"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1397224/",
      "name": "冯明 Ming Fung"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1379557/",
      "name": "凌汉 Hon Ling"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1304876/",
      "name": "元秋 Qiu Yuen"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1028064/",
      "name": "关之琳 Rosamund Kwan"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1315563/",
      "name": "李丽丽 Lily Li"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1329428/",
      "name": "关锋 Kwan Fung"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1278657/",
      "name": "元彬 Bun Yuen"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1299382/",
      "name": "唐季礼 Stanley Tong"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1417197/",
      "name": "金天柱 Tien-Chu Chin"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1320776/",
      "name": "白彪 Jason Pai"
    }
    ,
    {
      "@type": "Person",
      "url": "/celebrity/1432989/",
      "name": "钟荣 Chung Wing"
    }
  ]
,
  "datePublished": "",
  "genre": ["\u6b66\u4fa0", "\u53e4\u88c5"],
  "duration": "PT1H28M",
  "description": "本武侠片由龙逸升编导，惠英红、何家劲及关之琳主演。
故事描述，游侠杜孟飞（何家劲）奉师命下山闯荡江湖，途遇黑道中人捉拿沐龙门女弟子沐婉儿（关之琳），杜挺身相救，沐万分感激。未几，杜又见黑道中人围攻少...",
  "@type": "Movie",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingCount": "285",
    "bestRating": "10",
    "worstRating": "2",
    "ratingValue": "6.1"
  }
}'''
    str0 = str.replace("\n","")
    print(str0)