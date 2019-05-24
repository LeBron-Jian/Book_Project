import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'mybms.settings')
    import django
    django.setup()

    from Book_project import models
    import random

    # 批量插入book
    ret1 = [models.Book(title='水浒传{}'.format(i), price=random.randint(10, 100), publisher_id=1)
            for i in range(50)]
    ret2 = [models.Book(title='三国演义{}'.format(i), price=random.randint(10, 100), publisher_id=2)
            for i in range(50)]
    models.Book.objects.bulk_create(ret1)
    models.Book.objects.bulk_create(ret2)

    # 批量插入publisher
    ret1 = [models.Publisher(name='机械{}出版社'.format(i)) for i in range(50)]
    models.Publisher.objects.bulk_create(ret1)

    # 批量插入Author
    ret = [models.AuthorDetail(age=random.randint(20, 50), addr='北京{}'.format(i))
           for i in range(50)]
    models.AuthorDetail.objects.bulk_create(ret)

    li = []
    for item in models.AuthorDetail.objects.all().values('id'):
        ret = models.Author(name='james_' + str(item.get('id')), detail_id=item.get('id'))
        li.append(ret)

    models.Author.objects.bulk_create(li)

    # 作者绑定书  author  book
    for item in models.Author.objects.all():
        item.books.add(random.randint(100, 200), random.randint(100, 200), random.randint(100, 200),
                       random.randint(100, 200))

