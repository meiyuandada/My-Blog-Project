import os
import collections
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myfirstblog.settings")

import django

django.setup()

from app01.models import Comment


# 评论树


def create_list():
    print("--------------------------------------->create_tree")
    comment_all = Comment.objects.all()

    comment_list = []

    for i in comment_all:

        comment_list_item = []
        comment_list_item.append(i.nid)
        comment_list_item.append(i.content)
        comment_list_item.append(i.parent_comment_id)
        comment_tuple = tuple(comment_list_item)
        comment_list.append(comment_tuple)

    return comment_list


def tree_search(d_dic, comment_obj):
    print("--------------------------------------->tree_search")
    for k, v_dic in d_dic.items():
        if k[0] == comment_obj[2]:
            d_dic[k][comment_obj] = collections.OrderedDict()
            return
        else:
            tree_search(d_dic[k], comment_obj)

def build_tree(comment_list):
    print("--------------------------------------->build_tree")
    # 创建一个有序字典 按创建键值时的顺序排序内部
    comment_dic = collections.OrderedDict()

    for comment_obj in comment_list:
        print(comment_dic)
        if comment_obj[2] is None:
            # 如果是根评论 就添加到comment_dic[评论对象] ＝ {}
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            # 如果是回复的评论，则需要在 comment_dic 中找到其回复的评论
            tree_search(comment_dic, comment_obj)

    return comment_dic


comment_dict = build_tree(create_list())
# print(comment_dict)