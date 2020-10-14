from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createaution", views.createaution, name="createaution"),
    path("auctionlisting", views.auctionlisting, name="auctionlisting"),
    path("auctionview/<int:auction_id>", views.viewauction, name="viewauction"),
    path("<int:auction_id>/bid", views.bid, name="bid"),
    path("<int:auction_id>/com", views.addcomment, name="addcomment"),
    path("<int:auction_id>/watch", views.watchlist, name="watchlist"),
    path("viewuserswatchlist", views.viewuserswatchlist, name="viewuserswatchlist"),
    path("watchview/<int:watchlist_id>", views.singlewatchlistview, name="singlewatchlistview"),
    path("<int:watchlist_id>/removeitem", views.removewatchlistitem, name="removewatchlistitem"),
    path("categories", views.categories, name="categories"),
    path("listcategory/<category>", views.listcategory, name="listcategory"),
    path("closedbid/<int:auction_id>", views.closedbid, name="closedbid"),
    path("closedbidlisting", views.closedbidlisting, name="closedbidlisting"),
    path("viewwinner/<int:auction_id>/<fbid_amount>", views.viewwinner, name="viewwinner"),
    #path("bidlisting", views.bidlisting, name="bidlisting"),//watchlistwatchlist
]
