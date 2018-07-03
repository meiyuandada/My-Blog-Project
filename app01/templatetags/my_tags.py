from django import template
register = template.Library()
from django.utils.safestring import mark_safe
from ..models import *
import collections


# 左侧菜单栏

@register.inclusion_tag("menu.html")
def get_menu(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    # 查询当前站点所有分类
    cate_list = Category.objects.filter(blog=blog)
    # 查询每一个分类以及对应的文章数
    from django.db.models import Count
    cate_list = Category.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    print(cate_list)
    # 查询每一个标签对应的文章数
    tag_list = Tag.objects.filter(blog=blog).annotate(c=Count("article")).values_list("title", "c")
    print(tag_list)
    # 查询每一个年月和对应的文章数
    date_list = Article.objects.filter(user=user).extra(
        select={"create_ym": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("create_ym").annotate(
        c=Count("nid")).values_list("create_ym", "c")
    print(date_list)

    return {"username":username,"cate_list":cate_list,"tag_list":tag_list,"date_list":date_list,"user":user,"blog":blog,}


# 评论树

TEMP1 = '''
<li class = 'list-group-item' style = 'margin-left:%spx;'>
    <a href="">#%s楼</a>
    <span>%s</span>
    <a class="pull-right reply" pk="%s" >回复</a>
'''

def generate_commnet_html(sub_comment_dic,margin_left_val):

    html = '<ul class = "list-group">'
    # html = ''

    for k,v_dic in sub_comment_dic.items():

        html += TEMP1 % (margin_left_val,'子',k[1],k[0])

        if v_dic:

            html += generate_commnet_html(v_dic,margin_left_val)

        html += "</li>"

    html += "</ul>"

    return html



@register.simple_tag

def tree(comment_dic):
    print("--------------------------->tree")
    html = '<ul class = "list-group">'
    index = 0
    for k,v in comment_dic.items():
        index += 1
        html += TEMP1 % (0,index,k[1],k[0])
        html += generate_commnet_html(v,30)
        html += "</li>"
    html += '</ul>'

    return mark_safe(html)