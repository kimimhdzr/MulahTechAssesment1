from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .scraper import scrape_the_verge

def headlines_api(request):
    articles = scrape_the_verge()
    return render(request, 'webscrape/headlines.html', {'articles': articles})
