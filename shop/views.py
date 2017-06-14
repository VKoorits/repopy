from django.shortcuts import render
import requests
import json

def get_quote():
    url_random_quote = "http://api.forismatic.com/api/1.0/"
    params = {
        'method': 'getQuote',
        'format': 'json'
    }
    try:
        quote_obj = requests.get(url_random_quote, params=params)
        json_quote = json.loads(quote_obj.content.decode())
        quote = json_quote['quoteText']
        if json_quote['quoteAuthor'] != "":
            quote = quote + "<br></h1><h3>***" + json_quote['quoteAuthor'] + "***</h3><h1>"
        return quote
    except Exception:
        return "что-то не припомню ни одной цитаты"

def main_page(request):
    return render(request, 'shop/main_page.html', {"text": get_quote()})
