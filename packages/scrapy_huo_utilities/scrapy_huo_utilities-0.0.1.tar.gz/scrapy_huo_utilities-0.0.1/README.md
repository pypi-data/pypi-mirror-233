# scrapy_huo_utilities

#### 介绍

包含一个随机UserAgent和基于leveldb的DuplicateUrls中间件、几个清洗html的函数,自用的几个常用功能。

#### 安装教程

pip install scrapy_huo_utilities

#### 使用说明

1. RandomUserAgent_DOWNLOADER_MIDDLEWARES:

   在`settings.py`的`DOWNLOADER_MIDDLEWARES`中修改添加：
   `"scrapy_utils.MIDDLEWARES.Downloader_Middleware_Utils.RandomUserAgent_DOWNLOADER_MIDDLEWARES": 543,`


2. DuplicateUrls_SPIDER_MIDDLEWARES:
   在`settings.py`的`SPIDER_MIDDLEWARES`中修改添加：
   `"scrapy_utils.MIDDLEWARES.Spider_Middleware_Utils.DuplicateUrls_SPIDER_MIDDLEWARES": 543,`

3. html_clean:
   `from scrapy_huo_utilities.PROCESSORS import clean_html_attributes,clean_html_tags,clean_empty_img_tags`

   `clean_empty_img_tags`:清除没有src属性或src属性为空字符串的img标签。

   `clean_empty_a_tags`:清除没有href属性或href属性为空字符串的a标签。

   `clean_html_tags`:用于清除指定列表中的HTML标签。
   ```
   :param html_data:  传入html
   :param remove_tags:删除标签列表
   :param reserve_content:是否保留删除标签的文本内容，默认保留。
   :return: 处理后的html
   ```

   `clean_html_attributes`：用于清除HTML标签中的属性，除了白名单中包含的属性。
   ```
   :param html_data:传入html
   :param whitelist:白名单
   :return: html_data处理后的html
   ```
