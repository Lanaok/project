from functools import reduce

from django.db.models import Q
from django.shortcuts import render

from company.models import Company, Service


def search(request):
    query = request.GET['query']
    search_subject = request.GET['search_subject']
    object_list = None
    if search_subject == 'company':
        if query:
            split_query = str.split(query)
            object_list = list(Company.objects.filter(
                reduce(lambda x, y: x | y,
                       [Q(name__contains=word) | Q(description__contains=word) for word in split_query])).values())
        else:
            object_list = list(Company.objects.all())
    elif search_subject == 'service':
        if query:
            split_query = str.split(query)
            object_list = list(Service.objects.filter(
                reduce(lambda x, y: x | y,
                       [Q(name__contains=word) | Q(description__contains=word) for word in split_query])).values())
        else:
            object_list = list(Service.objects.filter())

    return render(request, 'search/search_results.html',
                  {'object_list': object_list, 'last_search_query': query, 'last_search_subject': search_subject})
