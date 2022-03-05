from django.urls import path
from .views import MainView, ComingSoon, FormView, NewsView    # importing all handlers from views.py
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", ComingSoon.as_view(), name='COMING_SOON'),
    path("news/", MainView.as_view(), name='MAIN_VIEW'),
    path("news/create/", FormView.as_view(), name='FORM_VIEW'),
    path('news/<int:link>/', NewsView.as_view(), name='NEWS_VIEW'),

]
urlpatterns += static(settings.STATIC_URL)
