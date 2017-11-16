from api.cms.models import CmsUser
from article.models import CategoryModel,TagModel,ArticleModel
from django.contrib.auth.models import User

def get_cmsuser_avatar(request):
    user = User.objects.all().first()
    cmsUser = CmsUser.objects.filter(user_id=user.id).first()
    return {'cmsuser_avatar':cmsUser.avatar}

def get_category(request):
    category = CategoryModel.objects.all()
    return {'extension_category':category}

def get_tag(request):
    tag = TagModel.objects.all()
    return {'extension_tag':tag}

def cms_pagination(request):
    article = ArticleModel.objects.all()
    sum = len(article)
    if sum % 5:
        page = sum//5 + 1
    else:
        page = sum/5