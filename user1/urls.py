from django.urls import path, re_path
from user1 import views

urlpatterns = [
    # path('login/', views.login),   #FVB
    # path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),   #CBV
    path('register/', views.RegisterView.as_view(), name='register'),
    path('exist_user/', views.exist_user),
    path('logout/', views.logout),

    path('book_list/', views.book_list, name='book_list'),
    # re_path(r'^book_list/(\d+)/(author)', views.book_list),
    re_path(r'^book_list/(?P<field_id>\d+)/(?P<field_type>publisher)', views.book_list),
    # 有名分组
    # re_path(r'^book_list/(\d+)/(author)', views.book_list),
    re_path(r'^book_list/(?P<field_id>\d+)/(?P<field_type>author)', views.book_list),
    # 有名分组
    path('del_book/', views.del_book, name='del_book'),
    re_path(r'^del_book(\d+)/(publisher)', views.del_book),
    re_path(r'^del_book(\d+)/(author)', views.del_book),

    path('add_book/', views.add_book, name='add_book'),
    re_path(r'^add_book(\d+)/(publisher)', views.add_book),
    re_path(r'^add_book(\d+)/(author)', views.add_book),

    re_path(r'^update_book/(?P<book_id>\d+)/(?P<field_id>\d+)/(?P<field_type>publisher)', views.update_book),
    re_path(r'^update_book/(?P<book_id>\d+)/(?P<field_id>\d+)/(?P<field_type>author)', views.update_book),
    # 这个必须放到下面，否则会截走上面两个，因为第一个也是正则
    re_path(r'^update_book/(?P<book_id>\d+)', views.update_book),

    path('publisher_list/', views.publisher_list, name='publisher_list'),
    path('del_publisher/', views.del_publisher, name='del_publisher'),
    path('add_publisher/', views.add_publisher, name='add_publisher'),
    re_path(r'^update_publisher/(\d+)', views.update_publisher),

    path('author_list/', views.author_list, name='author_list'),
    path('del_author/', views.del_author, name='del_author'),
    path('add_author/', views.add_author, name='add_author'),
    re_path(r'^update_author/(\d+)', views.update_author),


]

