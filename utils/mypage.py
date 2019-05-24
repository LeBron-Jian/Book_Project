#_*_coding:utf-8_*_
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class MyPaginator(object):
    def __init__(self, data, current_page_num, per_count=5, show_page_count=7):
        '''
                自定义分页器
                :param data:  要分页的所有数据
                :param current_page_num:  当前页数
                :param per_count:  每页显示的总数
                :param show_page_count:  显示页面的个数
                '''
        self.data = data
        self.current_page_num = current_page_num
        self.per_count = per_count
        self.show_page_count = show_page_count

        self.half_page = int(self.show_page_count / 2)
        self.paginator = Paginator(self.data, self.per_count)

        # 获取当前页码
        try:
            self.current_page_num = int(self.current_page_num)
            if self.current_page_num < 1:
                self.current_page_num = 1
            elif self.current_page_num > self.paginator.num_pages:
                self.current_page_num = self.paginator.num_pages
        except Exception as e:
            self.current_page_num = 1

        # 显示页码的范围
        if self.paginator.num_pages > self.show_page_count:
            if self.current_page_num - self.half_page < 1:
                self.page_range = range(1, self.show_page_count + 1)
            elif self.current_page_num + self.half_page > self.paginator.num_pages:
                self.page_range = range(self.paginator.num_pages - self.show_page_count + 1,
                                        self.paginator.num_pages + 1)
            else:
                self.page_range = range(self.current_page_num - self.half_page,
                                        self.current_page_num + self.half_page + 1)
        else:
            self.page_range = self.paginator.page_range

        # 获取当前页的数据
        try:
            self.current_page_data = self.paginator.page(self.current_page_num)
        except EmptyPage as e:
            self.current_page_data = self.paginator.page(1)
        except PageNotAnInteger as e:
            self.current_page_data = self.paginator.page(self.paginator.num_pages)
        except Exception as e:
            self.current_page_data = self.paginator.page(1)

    @property
    def show_page(self):
        dic_page = {
            'current_page_data': self.current_page_data,
            'paginator': self.paginator,
            'current_page_num': self.current_page_num,
            'page_range': self.page_range,
            'seque': self.per_count*(self.current_page_num - 1)
        }

        return dic_page
