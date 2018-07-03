from django.conf.urls import url
from .views import homesite,article_detail,poll,comment,get_comment_tree
urlpatterns=[
    url("poll/$",poll,),
    url("comment/$",comment,),
    url("get_comment_tree/(\d+)$",get_comment_tree,),
    url("(?P<username>\w+)/(?P<condition>tag|cate|achrive)/(?P<param>.*)", homesite, ),
    url("(?P<username>\w+)/articles/(?P<article_id>\d+)/$",article_detail,),
    url("(?P<username>\w+)/$",homesite,),
]