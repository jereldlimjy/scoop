from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from newsapi import NewsApiClient

import requests, os, datetime

API_KEY = os.environ['API_KEY']
news_API_KEY = os.environ['news_API_KEY']
newsapi = NewsApiClient(api_key=f'{news_API_KEY}')

# Create your views here.
def index(request):

	popular_articles = newsapi.get_everything(q='technology', language='en', sort_by='popularity')
	latest_articles = newsapi.get_everything(q='technology', language='en', sort_by='publishedAt')
	relevant_articles = newsapi.get_everything(q='technology', language='en', sort_by='relevancy')

	articles = [popular_articles, latest_articles, relevant_articles]

	for category in articles:
		for article in category['articles']:
			date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
			date = date.strftime("%d %B, %Y")
			article['publishedAt'] = date

			if article['urlToImage'] == '' or article['urlToImage'] == None:
				article['urlToImage'] = 'https://i.chzbgr.com/full/6486163968/hF3BC25F1/attachment-link-y-u-no-available'
		
	context = {
		'popular_articles': popular_articles['articles'],
		'latest_articles': latest_articles['articles'],
		'relevant_articles': relevant_articles['articles'],
	}

	return render(request, "main/index.html", context)


def finance(request):

	popular_articles = newsapi.get_everything(q='stocks', language='en', sort_by='popularity')
	latest_articles = newsapi.get_everything(q='stocks', language='en', sort_by='publishedAt')
	relevant_articles = newsapi.get_everything(q='stocks', language='en', sort_by='relevancy')

	articles = [popular_articles, latest_articles, relevant_articles]

	for category in articles:
		for article in category['articles']:
			date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
			date = date.strftime("%d %B, %Y")
			article['publishedAt'] = date

			if article['urlToImage'] == '' or article['urlToImage'] == None:
				article['urlToImage'] = 'https://i.chzbgr.com/full/6486163968/hF3BC25F1/attachment-link-y-u-no-available'
		
	context = {
		'popular_articles': popular_articles['articles'],
		'latest_articles': latest_articles['articles'],
		'relevant_articles': relevant_articles['articles'],
	}

	return render(request, "main/finance.html", context)


def search(request):

	if request.method == "POST":

		symbol = request.POST["symbol"]

		try:
			response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{symbol}/quote?token={API_KEY}")
			response1 = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{symbol}/company?token={API_KEY}")
			response2 = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{symbol}/news?token={API_KEY}")

			news = newsapi.get_everything(q=f'{symbol}', language='en', sort_by='publishedAt')

			response.raise_for_status()
			response1.raise_for_status()
			response2.raise_for_status()

		except requests.RequestException:
			messages.error(request, 'Something went wrong! Please ensure you enter a proper symbol.')
			return HttpResponseRedirect(reverse('index'))

		try:
			quote = response.json()
			company = response1.json()
			news = response2.json()

			counter = 0

			for article in news:

				dt = datetime.datetime.fromtimestamp(int(article["datetime"]) / 1000)
				article["datetime"] = dt.strftime("%d %B, %Y")

				if len(article["summary"]) > 260:
					article["summary"] = article["summary"][:260] + '...'

				if article["lang"] != "en":
					del news[counter]

				counter += 1

			if float(quote["change"]) > 0:
				colour = "text-success"
			else:
				colour = "text-danger"

			context = {
				"name": quote["companyName"],
            	"price": '{:,.2f}'.format(float(quote["latestPrice"])),
            	"symbol": quote["symbol"],
            	"news": news,
            	"change": round(float(quote["change"]), 2),
            	"changePercent": round(float(quote["changePercent"]) * 100, 2),
            	"colour": colour,
            	"exchange": company["exchange"],
            	"industry": company["industry"],
            	"sector": company["sector"],
            	"employees": '{:,}'.format(int(company["employees"])),
            	"description": company["description"],
            	"website": company["website"],
			}

		except (KeyError, TypeError, ValueError):
			messages.error(request, 'Something went wrong! Please ensure you enter a valid symbol.')
			return HttpResponseRedirect(reverse('index'))

		return render(request, "main/stock.html", context)

def singapore(request):

	response = requests.get(f"http://newsapi.org/v2/top-headlines?country=sg&apiKey={news_API_KEY}")

	articles = response.json()

	for article in articles['articles']:
		date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
		date = date.strftime("%d %B, %Y")
		article['publishedAt'] = date

		if article['description'] == None:
			article['description'] = ''

		if article['urlToImage'] == '' or article['urlToImage'] == None:
			article['urlToImage'] = 'https://i.chzbgr.com/full/6486163968/hF3BC25F1/attachment-link-y-u-no-available'

	context = {
		'articles': articles['articles']
	}

	return render(request, 'main/singapore.html', context)