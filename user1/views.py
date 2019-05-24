from django.shortcuts import render,HttpResponse, redirect, reverse
from django.utils.decorators import method_decorator
from django.core import serializers
from django.views import View
import json
import datetime
import logging
from functools import wraps

# Create your views here.
from user1 import models
from user1 import myforms
from utils.mypage import MyPaginator
from utils.hash_pwd import salt_pwd

logger = logging.getLogger(__name__)
# 生成一个名为collect的实例
collect_logger = logging.getLogger('collect')

def check_login(func):
    # 判断用户有没有登录的装饰器
    @wraps(func)
    def inner(request, *args, **kwargs):
        # 拿到当前访问网址
        url = request.get_full_path()
        if request.session.get('user'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/?next={}'.format(url))
    return inner

# def login(request):
#     login_form = myforms.LoginForm()
#     return render(request, 'user1/login.html', {'login_form': login_form})
#
# def register(request):
#     register_form = myforms.LoginForm()
#     return render(request, 'user1/register.html', {'register_form': register_form})

class LoginView(View):
    '''
        CBV 登录视图
        '''
    def get(self, request):
        login_form = myforms.LoginForm()
        return render(request, 'user1/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = myforms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            password = salt_pwd(password, username)
            if models.UserInfo.objects.filter(name=username, pwd=password):
                # 设置session
                request.session['user'] = username
                # 设置session的失效时间
                # request.session.set_expiry(1800)

                # 登录成功，写log
                logger.info('用户: ' + username + '登录成功')

                next_url = request.GET.get('next')
                if next_url:
                    # 跳转到之前访问的页面
                    return redirect(next_url)
                else:
                    return redirect(reverse('user1:book_list'))
            else:
                # 登录失败，写log
                logger.error('用户： '+username+'登录时，用户名或者密码错误')

                return render(request, 'user1/login.html', {'login_form': login_form,
                                                            'error_msg': '用户名或密码错误'})
        else:
            return render(request, 'user1/login.html', {'login_form': login_form})

class RegisterView(View):
    '''
        CBV 注册视图
        '''
    # 逻辑上装饰器不该加在这里，但是可以验证装饰器加成功了
    # @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        register_form = myforms.LoginForm()
        return render(request, 'user1/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = myforms.LoginForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            r_password = request.POST.get('r_password')
            if r_password == password:
                # 后台也需要判断用户名是否已经存在
                if not models.UserInfo.objects.filter(name=username).first():
                    password = salt_pwd(password, username)
                    models.UserInfo.objects.create(name=username, pwd=password)

                    # 注册成功之后，设置session登录状态
                    request.session['user'] = username

                    # 注册成功之后，写入log，并收集特定信息的日志
                    collect_logger.info('用户'+username+'注册')

                    return redirect(reverse('user1:book_list'))

            else:
                return render(request, 'user1/register.html', {'register_form': register_form,
                                                               'error_msg': '确认密码不符合'})
        return render(request, 'user1/register.html', {'register_form': register_form})

def exist_user(request):
    '''
        查看用户是否已经存在
        :param request:
        :return:
        '''
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = models.UserInfo.objects.filter(name=username).first()

        reg = {'status': 1, 'msg': '用户已存在'} if user_obj else {
            'status': 0, 'msg': '用户不存在'
        }
        return HttpResponse(json.dumps(reg))

def logout(request):
    '''
        注销
        :param request:
        :return:
        '''
    request.session.delete()
    return redirect(reverse('user1:login'))

@check_login
def book_list(request, field_id=0, field_type='src'):
    '''
        书列表 三种情况 从book_list下来的书，从publisher_list下来的书  从author_list下来的书
        :param request:
        :param field_id:
        :param filed_type:
        :return:
        '''
    books = None

    filter_field = {
        'publisher': 'publisher_id',
        'author': 'author_id',
    }
    field_dict = {filter_field.get(field_type): field_id} if field_type in (
        'publisher', 'author') else {}
    books = models.Book.objects.filter(**field_dict).values(
        'id', 'title', 'price', 'publish_date', 'publisher__name').order_by('-id')

    ''' 注意上面得简化方法
        if field_type == 'publisher':
            books = models.Book.objects.filter(publisher_id=field_id).values(
            'id','title','price','publish_date','publisher__name').order_by('-id')
        elif field_type == 'author':
            books = models.Book.objects.filter(authors__id=field_id).values(
            'id','title','price','publish_date','publisher__name').order_by('-id')
        else:
             books = models.Book.objects.all().values('id', 'title', 'price', 
             'publish_date', 'publisher__name').order_by('-id')
    '''

    current_page_num = request.GET.get('page', 1)
    page_obj = MyPaginator(books, current_page_num)

    current_path = {'path': request.path}
    # 页码返回的是字典
    ret_dic = page_obj.show_page
    # 两个字典拼接
    ret_dic.update(current_path)

    # return render(request, 'user1/book_list.html', page_obj.show_page)
    return render(request, 'user1/book_list.html', ret_dic)

def del_book(request, field_id=0, field_type='src'):
    '''
        删除一本书，三种情况 从book_list下来的书，从publisher_list下俩的书  从author_list下来的书
        :param request:
        :param field_id:
        :param field_type:
        :return:
        '''
    delete_id = request.POST.get('delete_id')
    # 清除绑定关系
    if field_type == 'author':
        author_id = field_id
        author_obj = models.Author.objects.filter(id=author_id).first()
        try:
            author_obj.books.remove(delete_id)
            reg = {'status': 1, 'msg': '删除成功'}
        except Exception as e:
            reg = {'status': 0, 'msg': '删除失败'}
    # 其他情况都删除书   book_list  publisher_list 下来的书
    else:
        try:
            models.Book.objects.filter(id=delete_id).delete()
            reg = {'status': 1, 'msg': '删除成功'}
        except Exception as e:
            reg = {'status': 0, 'msg': '删除失败'}

    return HttpResponse(json.dumps(reg))

def add_book(request, field_id=0, field_type='src'):
    '''
        增加书
        :param request:
        :param field_id:
        :param field_type:
        :return:
        '''
    current_publisher_id = 0
    current_author_id = 0
    if field_type == 'publisher':
        current_author_id = int(field_id)
    elif field_type == 'author':
        current_author_id = int(field_id)

    book_form = myforms.BookForm()

    if request.method == 'POST':
        if current_publisher_id:
            # 前台设置select_disabled 不能传到后台了，因此需要这样做
            publisher_id = current_publisher_id
        else:
            publisher_id = int(request.POST.get('publisher'))

        if request.POST.get('publish_date') != '':
            publish_date = request.POST.get('publish_date')
        else:
            publish_date = datetime.datetime.now()

        book_form = myforms.BookForm(request.POST)

        if book_form.is_valid():
            book_obj = models.Book.objects.create(
                title=book_form.cleaned_data.get('title'),
                price=book_form.cleaned_data.get('price'),
                publish_date=publish_date,
                publisher_id=publisher_id,
            )
            if current_author_id:
                # 绑定多对多关系
                book_obj.authors.add(current_author_id)

            # return redirect(reverse('book:book_list'))
            # 因为有三种情况，分别跳到自己对应的页面下
            return redirect(request.path.replace('add_book', 'book_list'))

    publisher = models.Publisher.objects.all().values('id', 'name').order_by('-id')

    return render(request, 'user1/add_book.html', {'book_form': book_form,
                                             'publisher': publisher,
                                             "current_publisher_id": current_publisher_id})

def update_book(request, book_id, field_id=0, field_type='src'):
    # 修改书
    book = models.Book.objects.filter(id=book_id).first()
    book_form = myforms.BookForm()
    book_form.initial = {'title': book.title, 'price': book.price}

    if request.method == 'POST':
        if request.POST.get('publish_date') != '':
            publish_date = request.POST.get('publish_date')
        else:
            publish_date = datetime.datetime.now()

        book_form = myforms.BookForm(request.POST)

        if book_form.is_valid():
            models.Book.objects.filter(id=book_id).update(
                title=book_form.cleaned_data.get('title'),
                price=book_form.cleaned_data.get('price'),
                publish_date=publish_date,
                publisher_id=request.POST.get('publisher'),
            )
            # 有三种情况，分别跳到自己对应的页面下
            if field_type in ('publisher', 'author'):
                new_url = reverse('user1:book_list') + field_id + '/' + field_type
            else:
                new_url = reverse('user1:book_list')

            return redirect(new_url)

    publisher = models.Publisher.objects.all().values('id', 'name').order_by('-id')
    return render(request, 'user1/update_book.html', {'book_form': book_form,
                                                'publisher': publisher,
                                                'current_publisher_id': book.publisher_id,
                                                'publish_date': book.publish_date})

# @check_login
def publisher_list(request):
    # 出版社列表
    publishers = models.Publisher.objects.all().order_by('-id')
    current_page_num = request.GET.get('page', 1)
    page_obj = MyPaginator(publishers, current_page_num)

    return render(request, 'user1/publisher_list.html', page_obj.show_page)

def del_publisher(request):
    # 删除出版社
    delete_id = request.POST.get('delete_id')
    try:
        models.Publisher.objects.filter(id=delete_id).delete()
        reg = {'status': 1, 'msg': '删除成功'}
    except Exception as e:
        reg = {'status': 0, 'msg': '删除失败'}

    return HttpResponse(json.dumps(reg))

def add_publisher(request):
    # 增加出版社
    publisher_form = myforms.PublisherForm()
    if request.method == 'POST':
        publisher_form = myforms.PublisherForm(request.POST)
        if publisher_form.is_valid():
            models.Publisher.objects.create(**publisher_form.cleaned_data)
            return redirect(reverse('user1:publisher_list'))

    return render(request, 'user1/add_publisher.html', {'publisher_form': publisher_form})

def update_publisher(request, publisher_id):
    # 修改出版社
    publisher = models.Publisher.objects.filter(id=publisher_id).first()
    publisher_from = myforms.PublisherForm()
    # 对form组件初始化
    publisher_from.initial = {'name': publisher.name}
    if request.method == 'POST':
        publisher_form = myforms.PublisherForm(request.POST)
        if publisher_form.is_valid():
            models.Publisher.objects.filter(id=publisher_id).update(**publisher_form.cleaned_data)
            return redirect(reverse('user1:publisher_list'))

    return render(request, 'user1/update_publisher.html', {'publisher_form': publisher_form})

# @check_login
def author_list(request):
    # 作者列表
    authors = models.Author.objects.all().values('id','detail_id', 'name', 'detail_age', 'detail_addr').order_by('-id')
    current_page_num = request.GET.get('page')
    page_obj = MyPaginator(authors, current_page_num)

    return render(request, 'user1/author_list.html')

def del_author(request):
    # 删除一个作者
    delete_id = request.POST.get('delete_id')
    try:
        # 删Author关联的不会被删掉
        # models.Author.objects.filter(id=delete_id).delete()

        # 删AuthorDetail关联的才会被删掉
        models.AuthorDetail.objects.filter(id=delete_id).delete()
        reg = {'status': 1, 'msg': '删除成功'}
    except Exception as e:
        reg = {'status': 0, 'msg': '删除失败'}

    return HttpResponse(json.dumps(reg))

def add_author(request):
    # 增加作者
    author_form = myforms.AuthorForm()
    if request.method == 'POST':
        author_form = myforms.AuthorForm(request.POST)
        if author_form.is_valid():
            name = author_form.cleaned_data.get('name')
            age = author_form.cleaned_data.get('age')
            addr = author_form.cleaned_data.get('addr')

            authordetail = models.AuthorDetail.objects.create(age=age, addr=addr)
            models.Author.objects.create(name=name, detail=authordetail)

            return redirect(reverse('user1:author_list'))
    return render(request, 'user1/add_author.html', {'author_form': author_form})

def update_author(request, author_id):
    # 修改作者
    author = models.Author.objects.filter(id=author_id).values('name', 'detail__age', 'detail__addr').first()
    author_form = myforms.AuthorForm()
    author_form.initial = {'name': author.get('name'), 'age': author.get('detail__age'),
                           'addr': author.get('detail__addr')}

    if request.method == 'POST':
        author_form = myforms.AuthorForm(request.POST)
        if author_form.is_valid():
            name = author_form.cleaned_data.get('name')
            age = author_form.cleaned_data.get('age')
            addr = author_form.cleaned_data.get('addr')

            models.Author.objects.filter(id=author_id).update(name=name)
            models.AuthorDetail.objects.filter(author__id=author_id).update(age=age, addr=addr)

            return redirect(reverse('user1:author_list'))

    return render(request, 'user1/update_author.html', {'author_form': author_form})




