from api.cms.models import CmsUser
from django.contrib.auth.models import User

def get_cmsuser_avatar(request):
    user = User.objects.all().first()
    cmsUser = CmsUser.objects.filter(user_id=user.id).first()
    return {'cmsuser_avatar':cmsUser.avatar}