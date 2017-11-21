from django.conf.urls import url,include
from django.contrib import admin
from api.cms import views

urlpatterns = [
    url(r'^login/$', views.cms_login,name='cms_login'),
    url(r'^register/$', views.cms_register,name='cms_register'),
    url(r'^index/$', views.cms_index,name='cms_index'),
    url(r'^logout/$', views.cms_logout,name='cms_logout'),
    url(r'^add_article/$', views.cms_add_article,name='cms_add_article'),
    url(r'^settings/$', views.cms_settings,name='cms_settings'),
    url(r'^news/$', views.cms_news,name='cms_news'),
    url(r'^add_category/$', views.cms_addcategory,name='cms_addcategory'),
    url(r'^add_tag/$', views.cms_addtag,name='cms_addtag'),
    url(r'^get_token/$', views.cms_get_token,name='cms_get_token'),
    url(r'^update_email/$', views.cms_update_email,name='cms_update_email'),
    url(r'^update_profile/$', views.cms_update_profile,name='cms_update_profile'),
    url(r'^read_article/$', views.cms_read_article,name='cms_read_article'),
    url(r'^discuss/$', views.cms_discuss,name='cms_discuss'),
    url(r'^distodis/$', views.cms_distodis,name='cms_distodis'),
]
