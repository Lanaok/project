from functools import reduce

from django.db.models import Q
from django.views.generic import ListView

from company.models import Company, Service


class SearchResultList(ListView):
    template_name = "search/search_results.html"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET['query']
        search_subject = self.request.GET['search_subject']
        object_list = None
        if search_subject == 'company':
            if query:
                split_query = str.split(query)
                object_list = Company.objects.filter(
                    reduce(lambda x, y: x | y,
                           [Q(name__contains=word) | Q(description__contains=word) for word in split_query])).values()
            else:
                object_list = Company.objects.all()
        elif search_subject == 'service':
            if query:
                split_query = str.split(query)
                object_list = Service.objects.filter(
                    reduce(lambda x, y: x | y,
                           [Q(name__contains=word) | Q(description__contains=word) for word in split_query])).values()
            else:
                object_list = Service.objects.filter()

        return object_list

    # 'last_search_query': query, 'last_search_subject': search_subject
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_search_query'] = self.request.GET['query']
        context['last_search_subject'] = self.request.GET['search_subject']
        return context
