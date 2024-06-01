from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list", views.list, name="list"),
    path("list/<int:listing_id>", views.details, name="details"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("close_bid", views.close_bid, name="close_bid"),
    path("comment", views.comment, name="comment"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.category_list, name="category_list")
]
