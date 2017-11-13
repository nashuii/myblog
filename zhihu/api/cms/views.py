
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from api.cms.forms import LoginForm,Register,AddCategoryForm,AddtagForm,AddarticleForm
from api.cms.spider import News
from article.models import CategoryModel,TagModel,ArticleModel
from utils import myjson
from qiniu import Auth

@login_required
def cms_index(request):
    articleModel = ArticleModel.objects.all()
    return render(request,'cms_index.html',{'articleModel':articleModel})


def cms_login(request):
    if request.method == 'GET':
        return render(request,'cms_login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username',None)
            password = form.cleaned_data.get('password',None)
            remember = form.cleaned_data.get('remember',None)
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
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
                return render(request,'cms_login.html',{'error':'用户名或密码错误！'})
        else:
            return render(request,'cms_login.html',{'error':form.errors})


def  cms_register(request):
    if request.method == 'GET':
        return render(request,'cms_register.html')
    else:
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username',None)
            password = form.cleaned_data.get('password',None)
            email = form.cleaned_data.get('email',None)
            User.objects.create_user(username=username,password=password,email=email)
            return redirect(reverse('cms_login.html'))
        else:
            return render(request,'cms_register.html',{'prompt':'注册失败','error':form.errors})


def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))

@login_required
def cms_add_article(request):
    categorys = CategoryModel.objects.all()
    tags = TagModel.objects.all()
    # print(categorys)
    if request.method == 'GET':
        return render(request,'cms_add_article.html',{'categorys':categorys,'tags':tags})
    else:
        form = AddarticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title',None)
            category = form.cleaned_data.get('category',None)
            desc = form.cleaned_data.get('desc',None)
            thumbnail = form.cleaned_data.get('thumbnail',None)
            content_html = form.cleaned_data.get('content_html',None)
            tags = request.POST.getlist('tags',None)
            user = request.user

            categoryModel = CategoryModel.objects.filter(id=category).first()

            article = ArticleModel(
                title = title,
                category = categoryModel,
                desc = desc,
                thumbnail = thumbnail,
                content_html = content_html,
                author = user
            )

            article.save()

            for tag in tags:
                tagModel = TagModel.objects.filter(id=tag).first()
                ArticleModel.tags.add(tag)
            return myjson.json_result()
        return myjson.json_params_error(message=form.errors.as_json())


def cms_settings(request):
    return HttpResponse('个人设置')


def cms_news(request):
    news = News().result()
    # print(news)
    return render(request,'cms_news.html',{'news':news})


@login_required
@require_http_methods(['POST'])
def cms_addcategory(request):
    form = AddCategoryForm(request.POST)
    if form.is_valid():
        categoryname = form.cleaned_data.get('categoryname',None)
        resultcategory = CategoryModel.objects.filter(name=categoryname).first()
        if not resultcategory:
            categoryModel = CategoryModel(name=categoryname)
            categoryModel.save()
            return myjson.json_result(data={'id':categoryModel.id,'name':categoryModel.name})
        else:
            return myjson.json_result(code=201,data={'id':resultcategory.id,'name':resultcategory.name})
    else:
        return myjson.json_params_error(message='表单验证失败')


def cms_addtag(request):
    form = AddtagForm(request.POST)
    if form.is_valid():
        tagname = form.cleaned_data.get('tagname',None)
        resulttag = TagModel.objects.filter(name=tagname).first()
        if not resulttag:
            tagModel = TagModel(name=tagname)
            tagModel.save()
            return myjson.json_result(data={'id':tagModel.id,'name':tagModel.name})
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
	q = Auth(access_key,secret_key)
	# 3. 设置七牛空间
	bucket_name = 'project01-of-django'
	# 4. 生成token
	token = q.upload_token(bucket_name)
	# 5. 返回token,key必须为uptoken
	return myjson.json_result(kwargs={'uptoken':token})