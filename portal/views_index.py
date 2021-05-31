from django.shortcuts import render
from django.http import JsonResponse


rss_links_dict = {
    'na': 'https://www.thehindu.com/news/national/feeder/default.rss',
    'in': 'https://www.thehindu.com/news/international/feeder/default.rss',
    'op': 'https://www.thehindu.com/opinion/feeder/default.rss',
    'sp': 'https://www.thehindu.com/sport/feeder/default.rss',
    'bs': 'https://www.thehindu.com/business/feeder/default.rss'
}

def index(request):
    context = {
        'rss_links_dict': rss_links_dict,
    }
    return render(request, 'landing.html', context=context)
