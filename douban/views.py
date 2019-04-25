from django.shortcuts import render,HttpResponse
import requests
from bs4 import BeautifulSoup
import re
from .models import Movie,Dj
from django.views.generic import ListView
import os
# Create your views here.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}

def get_data(headers):
    top250 = []
    for j in range(0, 226, 25):
        url = 'https://movie.douban.com/top250?start=' + str(j)
        res = requests.get(url,headers=headers)
        bsobj = BeautifulSoup(res.content)

        info_list = bsobj.find_all('div',class_='item')
        for i in info_list:
            movie =[]

            id = i.find('em',class_='').get_text()
            name = i.find('img',class_='')['alt']
            infos =i.find('div',class_='bd').p.get_text()
            director = re.search('导[^\xa0]*', infos).group()
            tct_info = re.search('\d.+', infos).group()
            tct_info = tct_info.split(' / ')
            img_url = i.find('img',class_='')['src']
            marks = i.find('span',class_='rating_num').get_text()
            movie += [id,name,director,tct_info[0],tct_info[1],tct_info[2],marks]
            top250.append(movie)
    return top250

def save_data(get_data):
    top250 = get_data(headers)
    print(top250)
    save_list = []
    for i in top250:
        save_list.append(Movie(top=i[0],name=i[1],director=i[2],time=i[3],country=i[4],style=i[5],mark=i[6]))
    print(Movie.objects.count())
    if Movie.objects.count()==0:
        img = requests.get(top250[7], headers=headers)
        file_name = '/Users/mango/python/yybzuoye/static/movie/{}.jpg'.format(id)
        with open(file_name, 'wb') as f:
            f.write(img.content)
        Movie.objects.bulk_create(save_list)

def deal(request):
    save_data(get_data)
    return HttpResponse('ok')

class MovieShow(ListView):
    model = Movie
    template_name = 'douban.html'
    paginate_by = 15
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        context = super(MovieShow, self).get_context_data(**kwargs)

        paginator = context.get('paginator')
        page_obj = context.get('page_obj')

        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)

        return context

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current = page_obj.number
        num = paginator.num_pages

        left_has_more = False
        right_has_more = False
        if current <= around_count+2:
            left_page = range(1,current)
        else:
            left_has_more = True
            left_page = range(current-around_count,current)

        if current >= num -around_count -1:
            right_page = range(current +1 ,num+1)
        else:
            right_has_more = True
            right_page = range(current+1,current+around_count+1)

        print(self.request.get_full_path())
        last_request = self.request.get_full_path()
        if last_request.find('select') !=-1:
            select = self.request.GET.get('select')
            search = self.request.GET.get('search')
            last_request = '?select={}&search={}'.format(select,search)
        else:
            last_request = None

        data={
            'last_request':last_request,
            'left_page':left_page,
            'right_page':right_page,
            'current':current,
            'num':num,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more
        }
        return data

    def get_queryset(self):
        select = self.request.GET.get('select')
        search = self.request.GET.get('search')

        if select:
            category_dict = {'排名': 'top', '电影名': 'name__contains', '导演': 'director__contains', '国家': 'country__contains', '时间': 'time__contains', '类型': 'style__contains'}
            category = category_dict[select]
            search_dict = {}
            search_dict[category] = search
            search_obj= Movie.objects.filter(**search_dict)

            return search_obj

        return Movie.objects.all()

def download_img(request):
    dj_obj = Dj.objects.all().values()
    for img_url in dj_obj:
        img = 'https:'+img_url['imgurl']
        images = requests.get(img)
        file_name = '/Users/mango/python/yybzuoye/static/images/jd/{}.jpg'.format(img_url['id'])
        if not os.path.exists(file_name):
            with open(file_name,'wb') as f:
                f.write(images.content)
        print(img_url['id'])

    return HttpResponse('ok')


