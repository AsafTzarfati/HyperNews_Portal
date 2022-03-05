from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from datetime import datetime
from .ArticleForm import ArticleForm
from .news import sort_by_date, Links, update_json, search_news, read_json

my_links = Links()
news_list = list()


class ComingSoon(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return redirect("/news/")


class MainView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        search = request.GET.get("q")
        if search is None:
            context = sort_by_date(my_links, news_list)
            return render(request, f"news/index.html", context=context)
        else:
            context = search_news(search, news_list)
            if context:
                return render(request, f"news/index.html", context=context)
            else:
                return render(request, f"news/not_found.html", context={"search": search})


class NewsView(View):
    def get(self, request: HttpRequest, link, *args, **kwargs) -> HttpResponse:
        context = sort_by_date(my_links, news_list)
        if my_links.is_occupied(link):
            for news in news_list:
                if link == news['link']:
                    context = news
            return render(request, f"news/news_page.html", context=context)
        else:
            return render(request, f"news/not_found.html", context={"search": link})


class FormView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "news/creating_new_articles.html", {"form": ArticleForm()})

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        new_article = dict()
        # create a form instance and populate it with data from the request:
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article["created"] = str(datetime.now().isoformat(' ', 'seconds'))
            new_article["text"] = form.cleaned_data["text"]
            new_article["title"] = form.cleaned_data["title"]
            new_article["link"] = my_links.get_uniq_link()
            update_json(new_article, news_list)
            news_list.append(new_article)

        return redirect("/news/")


news_list = read_json()

