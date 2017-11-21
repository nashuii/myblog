from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from api.cms.forms import LoginForm, Register, AddCategoryForm, AddtagForm, AddarticleForm, UpdateEmailForm, \
    UpdateProfileForm,DiscussForm,DiscussToDiscussForm
from api.cms.spider import News
from article.models import CategoryModel, TagModel, ArticleModel, DiscussModel, DiscussToDiscussModel
from api.cms.models import CmsUser
from utils import myjson
from qiniu import Auth


# @login_required
def cms_index(request, category_id=0, tag_id=0):
    category_id = request.GET.get('category_id', 0)
    tag_id = request.GET.get('tag_id', 0)
    # c_url = request.GET.get('last')
    # print(request.user.username)
    if int(category_id):
        articleModel = ArticleModel.objects.filter(category_id=category_id)
    elif int(tag_id):
        articleModel = []
        for article in ArticleModel.objects.all():
            if article.tags.filter(articlemodel__tags=tag_id):
                articleModel.append(article)
    else:
        articleModel = ArticleModel.objects.all()
    # 获取文章所需总页数
    sum = len(articleModel)
    articles_perpage = 5
    page_num = 5
    if sum % articles_perpage:
        page = sum//articles_perpage + 1
    else:
        page = max(1, sum//articles_perpage) # 如果文章数为零，则默认显示第一页
    # 获取当前页
    c_page = min(page, max(1, int(request.GET.get('page',1))))   # 限制当前的页码在1-page（文章总页码）
    # 创建文章页面
    a_start = (c_page - 1) * articles_perpage
    a_stop = c_page * articles_perpage
    # 文章切片
    a_article = articleModel[a_start:a_stop]
    # 跳转分页
    if c_page % page_num:
        current_pages = c_page//page_num +1
    else:
        current_pages = c_page//page_num
    # 创建页码
    p_start = (current_pages - 1) * page_num + 1
    p_stop = current_pages * page_num + 1
    p_page = range( p_start,min(page + 1,p_stop))
    return render(request, 'cms_index.html', {'page': p_page,
                                              'articleModel': a_article,
                                              'add_page':p_start + page_num,
                                              'cut_page':p_start - 1,
                                              # 'current_url':c_url,
                                              'category_id':category_id,
                                              'tag_id':tag_id
                                              })


def cms_login(request):
    if request.method == 'GET':
        return render(request, 'cms_login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            remember = form.cleaned_data.get('remember', None)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                nexturl = request.GET.get('next')
                if nexturl:
                    return redirect(nexturl)
                else:
                    return redirect(reverse('cms_index'))
            else:
                return render(request, 'cms_login.html', {'error': '用户名或密码错误！'})
        else:
            return render(request, 'cms_login.html', {'error': form.errors})


def cms_register(request):
    if request.method == 'GET':
        return render(request, 'cms_register.html')
    else:
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', None)
            password = form.cleaned_data.get('password', None)
            email = form.cleaned_data.get('email', None)
            User.objects.create_user(username=username, password=password, email=email)
            return redirect(reverse('cms_login.html'))
        else:
            return render(request, 'cms_register.html', {'prompt': '注册失败', 'error': form.errors})


def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))


@login_required
def cms_add_article(request):
    categorys = CategoryModel.objects.all()
    tags = TagModel.objects.all()
    # print(categorys)
    if request.method == 'GET':
        article_uid = request.GET.get('article_uid', None)
        articleModel = ArticleModel.objects.filter(uid=article_uid).first()
        article_tags = articleModel.tags.all() if articleModel else []
        return render(request, 'cms_add_article.html', {'categorys': categorys,
                                                        'tags': tags,
                                                        'article': articleModel,
                                                        'article_tags': article_tags})
    else:
        form = AddarticleForm(request.POST)
        if form.is_valid():
            uid = form.cleaned_data.get('uid',None) # 如果请求为修改文章，则uid存在
            title = form.cleaned_data.get('title', None)
            category = form.cleaned_data.get('category', None)
            desc = form.cleaned_data.get('desc', None)
            thumbnail = form.cleaned_data.get('thumbnail', None)
            content_html = form.cleaned_data.get('content_html', None)
            tags = request.POST.getlist('tags[]', None)
            print('ajax:', uid)
            user = request.user

            categoryModel = CategoryModel.objects.filter(id=category).first()

            # 获取article对象，如果存在，则归为修改请求，反之则是创建请求
            article = ArticleModel.objects.filter(uid=uid).first()
            print(article)
            # 修改文章
            if article:
                article.title = title
                article.category = categoryModel
                article.desc = desc
                article.thumbnail = thumbnail
                article.content_html = content_html
                article.tags.clear() # 清除原先的tags列表
            # 创建文章
            else:
                article = ArticleModel(
                        title=title,
                        category=categoryModel,
                        desc=desc,
                        thumbnail=thumbnail,
                        content_html=content_html,
                        author=user
                )

            article.save()
            for tag in tags:
                tagModel = TagModel.objects.filter(id=tag).first()
                print(tagModel)
                article.tags.add(tagModel)
            return myjson.json_result()
        return myjson.json_params_error(message=form.errors.as_json())



@login_required
def cms_settings(request):
    return render(request, 'cms_settings.html')


def cms_news(request):
    news = News().result()
    # print(news)
    return render(request, 'cms_news.html', {'news': news})


@login_required
@require_http_methods(['POST'])
def cms_addcategory(request):
    form = AddCategoryForm(request.POST)
    if form.is_valid():
        categoryname = form.cleaned_data.get('categoryname', None)
        resultcategory = CategoryModel.objects.filter(name=categoryname).first()
        if not resultcategory:
            categoryModel = CategoryModel(name=categoryname)
            categoryModel.save()
            return myjson.json_result(data={'id': categoryModel.id, 'name': categoryModel.name})
        else:
            return myjson.json_result(code=201, data={'id': resultcategory.id, 'name': resultcategory.name})
    else:
        return myjson.json_params_error(message='表单验证失败')


def cms_addtag(request):
    form = AddtagForm(request.POST)
    if form.is_valid():
        tagname = form.cleaned_data.get('tagname', None)
        resulttag = TagModel.objects.filter(name=tagname).first()
        if not resulttag:
            tagModel = TagModel(name=tagname)
            tagModel.save()
            return myjson.json_result(data={'id': tagModel.id, 'name': tagModel.name})
        else:
            return myjson.json_params_error(message='不能创建同名的标签！')
    else:
        return myjson.json_params_error(message='表单验证失败')


@require_http_methods(['GET'])
def cms_get_token(request):
    """
	1. 客户端在上传图片到七牛之前,需要先从业务服务器
	上获取token,本函数就是获取token的函数
	2. 客户端获取到token后,拿到token后把token和图片一起上传到七牛服务器
	3. 七牛收到token和图片后,会判断当前token是否有效,如果有效,则会
	返回图片名到客户端和业务服务器.
	"""
    # 1. 先要设置AccessKey和SecretKey
    access_key = "K3rmN5wqiS2nsXTGldrWCz1c3tYS8oj9Fy2uZLj-"
    secret_key = "7ynwR7skMO2DOcfxz7wfSJWgekBIOdoTczYSypC7"
    # 2. 授权
    q = Auth(access_key, secret_key)
    # 3. 设置七牛空间
    bucket_name = 'project01-of-django'
    # 4. 生成token
    token = q.upload_token(bucket_name)
    # 5. 返回token,key必须为uptoken
    return myjson.json_result(kwargs={'uptoken': token})

@login_required
@require_http_methods(['POST'])
def cms_update_profile(request):
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username', None)
        avatar = form.cleaned_data.get('avatar', None)
        print(avatar)
        print(username)
        user = User.objects.all().first()
        user.username = username
        user.save()

        cmsuser = CmsUser.objects.filter(user_id=user.id).first()
        if not cmsuser:
            cmsuser = CmsUser(user=user, avatar=avatar)
        else:
            cmsuser.avatar = avatar
        cmsuser.save()
        return myjson.json_result()
    return myjson.json_params_error(message=form.errors.as_json())


def cms_update_email(request):
    return 1

def cms_read_article(request):
    article_uid = request.GET.get('article_uid',None)
    article = ArticleModel.objects.filter(uid=article_uid).first()
    discussModel = DiscussModel.objects.filter(article=article).all()
    discuss = []
    if discussModel:
        for dis in discussModel:
            auth = dis.auth
            avatar = CmsUser.objects.filter(user=auth).first().avatar
            id = dis.id
            content = dis.content
            distodisModel = DiscussToDiscussModel.objects.filter(discuss=dis).all()
            distodis = []
            if distodisModel:
                for dis2 in distodisModel:
                    auth2 = dis2.auth
                    avatar2 = CmsUser.objects.filter(user=auth2).first().avatar
                    content2 = dis2.content
                    distodis.append({
                        'auth': auth2,
                        'avatar': avatar2,
                        'content': content2
                    })
            discuss.append({
                'id': id,
                'auth': auth,
                'avatar': avatar,
                'content': content,
                'distodis': distodis
            })
    return render(request,'cms_read_article.html',{'article':article,
                                                   'discuss':discuss})

@login_required
def cms_discuss(request):
    form = DiscussForm(request.POST)
    if form.is_valid():
        auth = request.user
        article_uid = form.cleaned_data.get('article_uid')
        text = form.cleaned_data.get('text')
        # print(text,article_uid)
        articleModel = ArticleModel.objects.filter(uid=article_uid).first()
        # print(articleModel)
        cms_user = CmsUser.objects.filter(user=auth).first()

        discuss = DiscussModel(auth=auth, article=articleModel, content=text)
        discuss.save()

        return myjson.json_result(data={'auth':auth.username,'avatar':cms_user.avatar})
    return myjson.json_params_error(message=form.errors.as_json())

@login_required
def cms_distodis(request):
    form = DiscussToDiscussForm(request.POST)
    if form.is_valid():
        auth = request.user
        discuss_id = form.cleaned_data.get('discuss_id')
        text = form.cleaned_data.get('text')
        print(discuss_id)
        discussModel = DiscussModel.objects.filter(id=discuss_id).first()

        cms_user = CmsUser.objects.filter(user=auth).first()

        distodis = DiscussToDiscussModel(auth=auth, discuss=discussModel, content=text)
        distodis.save()

        return myjson.json_result(data={'auth':auth.username,'avatar':cms_user.avatar})
    return myjson.json_params_error(message=form.errors.as_json())