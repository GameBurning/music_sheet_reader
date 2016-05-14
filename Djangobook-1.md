# Django Book 笔记 -- 为什么要框架

了解Django之前,先要了解一些关于Web开发的历史.
## 什么是Web框架?
### 没有Web框架的世界
使用Python开发Web,最简单,原始和直接的办法是使用***CGI标准***.
CGI标准的工作流程如下:首先做一个Python脚本,输出HTML代码,然后保存成.cgi扩展名的文件,通过浏览器访问此文件.

下面是一个CGI脚本的例子,用来显示数据库中最新出版的10本书:
```python
#!/usr/bin/env python

import MySQLdb

print "Content-Type: text/html\n"
print "<html><head><title>Books</title></head>"
print "<body>"
print "<h1>Books</h1>"
print "<ul>"

connection = MySQLdb.connect(user='me', passwd='letmein', db='my_db')
cursor = connection.cursor()
cursor.execute("SELECT name FROM books ORDER BY pub_date DESC LIMIT 10")

for row in cursor.fetchall():
    print "<li>%s</li>" % row[0]

print "</ul>"
print "</body></html>"

connection.close()
```

***优点:***
* 清晰易懂,不需要太多知识

***缺点:***
* 应用中多处连接数据库怎么处理?应当写一个共享函数,被多个代码调用
* 每次都要关闭数据库会增加犯错几率.初始化和释放工作应该交给通用框架完成.
* 这段代码被重用的话,每一次都要改变其中的数据库名和密码吗?一个环境级别的总体设置显得至关重要.
* 如果一个没有Python经验的想修改这个网页,一个错误的字母可能会让整个网页崩溃.所以我们需要把不同的任务用不同的模块区分开来.

### MVC设计模式
如果我们把之前这个CGI文件,用Django重写,我们看看会变成什么样?

我们用Django把项目分成4个Python文件(\__init__.py,models.py, views.py, urls.py)和一个HTML的模板.

```python
# models.py (the database tables)

from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    pub_date = models.DateField()


# views.py (the business logic)

from django.shortcuts import render_to_response
from models import Book

def latest_books(request):
    book_list = Book.objects.order_by('-pub_date')[:10]
    return render_to_response('latest_books.html', {'book_list': book_list})


# urls.py (the URL configuration)

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    (r'^latest/$', views.latest_books),
)


# latest_books.html (the template)

<html><head><title>Books</title></head>
<body>
<h1>Books</h1>
<ul>
{% for book in book_list %}
<li>{{ book.name }}</li>
{% endfor %}
</ul>
</body></html>
```

不用关心细节,只要关心整体设计,关注分割后的几个文件:
* model.py 用一个python类描述数据表
* views.py 包含了页面的业务逻辑, 其中的latest_books()函数叫做视图
* urls.py 指出了什么样的URL调用什么样的视图. 在这个例子中 /latest/ URL 将会调用 latest_books() 这个函数。 换句话说，如果你的域名是example.com，任何人浏览网址http://example.com/latest 将会调用latest_books()这个函数。
* latest_books.html 是 html 模板，它描述了这个页面的设计是如何的。 使用带基本逻辑声明的模板语言，如{% for book in book_list %}

MVC的优点在于松散组合,每个Django驱动的Web应用都有明确的目的,并且可以独立更改而不影响到其他的部分.开发者更改一个应用程序中的URL而不用影响到这个程序底层的实现.

## 获取帮助
* Django邮件列表是很多Django用户提出问题、回答问题的地方。 可以通过http://www.djangoproject.com/r/django-users 来免费注册。
* 如果Django用户遇到棘手的问题,希望得到及时地回复，可以使用Django IRC channel。 在Freenode IRC network加入#django
