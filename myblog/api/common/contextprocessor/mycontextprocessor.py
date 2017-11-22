from api.cms.models import CmsUser
from article.models import CategoryModel,TagModel,ArticleModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def get_cmsuser_avatar(request):
    user = request.user
    if user.is_authenticated():
        cmsUser = CmsUser.objects.filter(user=user).first()
        return {'cmsuser_avatar':cmsUser.avatar}
    return {'cmsuser_avatar':'/static/images/default_avatar.jpg'}

def get_category(request):
    category = CategoryModel.objects.all()
    return {'extension_category':category}

def get_tag(request):
    tag = TagModel.objects.all()
    return {'extension_tag':tag}

