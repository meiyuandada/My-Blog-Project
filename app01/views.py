from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
import json
from django.db.models import F
from django.db import transaction
from django import forms
from django.forms import widgets
from .models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
import collections
from app01.utils import u_1 as u1
from app01.templatetags import my_tags
# Create your views here.
# 登陆
def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        res = {"state": False, "msg": None}

        # 获取session的验证码
        valid_str = request.session.get("valid_str")

        if valid_code.upper() == valid_str.upper():
            # 调用auth的验证功能
            user = auth.authenticate(username=user, password=pwd)
            if user:
                res["state"] = True
                auth.login(request, user)
            else:
                res["msg"] = "账户密码错误"
        else:
            res['msg'] = "验证码错误"

        return JsonResponse(res)

    return render(request, "login.html")


# 获取验证码
def get_valid_img(request):
    import PIL

    from PIL import Image
    from PIL import ImageDraw, ImageFont
    import random
    # 随机颜色
    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    image = Image.new("RGB", (250, 40), get_random_color())

    # 生成五个随机字符串
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/font/kumo.ttf", size=32)
    temp = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((24 + i * 36, 0), random_char, get_random_color(), font=font)
        # 保存随机字符
        temp.append(random_char)

    print("---", temp)

    # 在内存生成图片
    from io import BytesIO
    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()
    f.close()

    valid_str = "".join(temp)
    # 给浏览器设置session
    request.session["valid_str"] = valid_str

    return HttpResponse(data)


class RegForm(forms.Form):
    user = forms.CharField(max_length=8, label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(min_length=4, label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    repeat_pwd = forms.CharField(min_length=4, label="确认密码",
                                 widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control"})
                             )

    def clean_user(self):
        val = self.cleaned_data.get("user")

        ret = UserInfo.objects.filter(username=val)

        if not ret:
            return val
        else:
            raise ValidationError("该用户已存在")

    def clean(self):
        if self.cleaned_data.get("pwd") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")


def reg(request):
    if request.method == "POST":
        res = {"user": None, "error_dict": None}
        form = RegForm(request.POST)
        # 验证form表单基本参数
        if form.is_valid():
            print(form.cleaned_data)
            print(request.FILES)
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar = request.FILES.get("avatar")
            print("user", user)
            if avatar:  # 看有没有传图片
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, avatar=avatar)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            res["user"] = user.username
        # 把错误信息存一存
        else:
            print(form.errors)  # {"repeat_pwd":["....",],"email":["......",]}
            print(form.cleaned_data)
            res["error_dict"] = form.errors
        return JsonResponse(res)
    form = RegForm()
    return render(request, "reg.html", locals())


from .models import *


# 主页
def index(request):
    # if not request.user.username:
    #     return redirect("/login/")
    article_list = Article.objects.all()
    return render(request, "index.html", {"article_list": article_list})


# 注销
def logout(request):
    auth.logout(request)
    return redirect("/login/")


# 个人站点
def homesite(request, username, **kwargs):
    print("kwargs", kwargs)
    print("username", username)
    # 当前站点对象
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return HttpResponse("404")
    # 当前站点对象
    blog = user.blog
    # 查询当前站点所有文章
    if not kwargs:
        article_list = Article.objects.filter(user=user)
    else:
        condition = kwargs.get("condition")
        param = kwargs.get("param")
        if condition == "cate":
            article_list = Article.objects.filter(user=user).filter(category__title=param)
        elif condition == "tag":
            article_list = Article.objects.filter(user=user).filter(tags__title=param)
        else:
            print(param)
            year, month = param.split("-")
            article_list = Article.objects.filter(user=user).filter(create_time__year=year, create_time__month=month)

    return render(request, "myblog/home1.html", locals())







# 文章详情
def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article = Article.objects.filter(pk=article_id).first()
    comment_list = Comment.objects.filter(article_id=article_id)
    comment_dic_view = u1.comment_dict
    return render(request, "myblog/article.html", locals())


# 点赞

def poll(request):
    print("poll is running-------")
    # 取到当前是点赞了还是反对了
    is_up = json.loads(request.POST.get("is_up"))
    print('11111', is_up)
    # 取到文章的id
    article_id = request.POST.get("article_id")
    # 确定到用户的id
    user_id = request.user.pk
    # 状态默认为True
    res = {"state": True}

    # 正常点击了的情况
    try:
        with transaction.atomic(): # 数据库事务 要成功都成功 否则都不成功
            ArticleUpDown.objects.create(is_up=is_up, article_id=article_id, user_id=user_id)
            if is_up:
                Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
            else:
                Article.objects.filter(pk=article_id).update(down_count=F("down_count") + 1)
    # 重复点击会报错 相当于一个用户重复创建点赞或者反对对象了 但是一个用户和一篇文章是关联唯一的
    except Exception as e:
        # 重复操作后把默认状态改为False
        res["state"] = False
        # 记录用户第一次到底是点赞了还是反对了
        res["first_operate"] = ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).first().is_up

    return JsonResponse(res)


# 评论
def comment(request):
    # 取到ajax传送的数据
    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk

    res = {"state": True}
    #添加事务  创建成功的同时才计数增加
    with transaction.atomic():
        if not pid:
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, )
        else:
            obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content, parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)
    ######################################################
    # comment_dic_view = u1.comment_dict
    # ret = my_tags.tree(comment_dic_view)
    ######################################################
    return JsonResponse(res)





####################
def get_comment_tree(request,id):

    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    ret = list(Comment.objects.filter(article_id=id).values("pk","content","parent_comment_id","user__username"))

    print('################################ret',ret)

    return JsonResponse(ret,safe=False)
