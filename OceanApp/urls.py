from django.urls import path
from . import views

urlpatterns = [
    path('res', views.res, name='res'),
    path('home', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('check/user', views.check_user, name='check_user'),
    path('logout', views.logout, name='logout'),
    path('blog', views.blog, name='blog'),
    path('me/blog', views.my_blog, name='my_blog'),
    path('blog/detail/<str:idPost>', views.blogDetail, name='blogDetail'),
    path('create/blog', views.createBlog, name='createBlog'),
    path('delete/blog/<str:idPost>', views.deleteBlog, name='deleteBlog'),
    path('contact', views.contact, name='contact'),
    path('latest/blog', views.get_latest_blogs, name='latest_blogs'),
    path('create/comment', views.createComment, name='createComment'),
    path('blog/search', views.searchBlog, name='searchBlog'),
    path('profile', views.profile, name='profile'),

]
