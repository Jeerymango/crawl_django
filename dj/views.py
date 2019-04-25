from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from douban.models import Dj
class JdShow(ListView):
    model = Dj
    template_name = 'jd.html'
    paginate_by = 15
    context_object_name = 'jd'

    def get_context_data(self, **kwargs):
        context = super(JdShow, self).get_context_data(**kwargs)

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
            category_dict = {'价格小于':'price__lt','价格等于':'price','价格大于':'price__gt','型号':'title__icontains'}
            category = category_dict[select]
            search_dict = {}
            search_dict[category] = search
            search_obj= Dj.objects.filter(**search_dict)

            return search_obj

        return Dj.objects.all()
