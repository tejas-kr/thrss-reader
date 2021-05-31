from django.shortcuts import render
from django.http import JsonResponse

from .helper_functions import get_data, get_rss_links_dict, predict_sentiment

def news(request, type='na'):
    rss_links_dict = get_rss_links_dict()

    rss_link = rss_links_dict[type]

    all_data_dict = get_data(rss_link)

    context = {
        'all_data_dict': all_data_dict,
        'rss_links_dict': rss_links_dict,
        'type': type
    }

    return render(request, 'index.html', context)


def nlp(request, type):
    req_data = request.POST

    process = req_data['process']
    
    rss_links_dict = get_rss_links_dict()

    rss_link = rss_links_dict[type]

    result = {}
    result = get_data(rss_link)

    if process != 'all':
        result = predict_sentiment(raw_data=result, process=process)

    return JsonResponse(result)

