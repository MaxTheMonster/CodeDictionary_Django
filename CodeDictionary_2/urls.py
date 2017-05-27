from django.conf.urls import url
from django.contrib import admin
from Dictionary import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^search/$', views.search_words, name='search_words'),
    url(r'^search_categories/$', views.search_categories, name='search_categories'),
    url(r'^submit/$', views.CreateWordView.as_view(), name="submit"),
    url(r'^word/(?P<slug>[-\w]+)/$', views.WordDetailView.as_view(), name="word_detail"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^profile/(?P<slug>[-\w]+)/$', views.ProfileView.as_view(), name="profile"),
    url(r'^category/(?P<slug>[-\w]+)/$', views.CategoryView.as_view(), name="category"),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
