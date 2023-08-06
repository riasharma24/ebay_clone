from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('add',views.addListing, name='addListing'),
    path('show_watchlist',views.show_watchlist,name='show_watchlist'),
    path('show_categories',views.show_categories,name='show_categories'),
    path('displayCategoryListings/<str:category>',views.displayCategoryListings,name='displayCategoryListings'),
    path('getDetails/<int:listing_id>',views.getDetails,name='getDetails'),
    path('removeFromWatchist/<int:list_id>',views.removeFromWatchlist,name='removeFromWatchlist'),
    path('addToWatchlist/<int:list_id>',views.addToWatchlist,name='addToWatchlist'),
    path('commentOnListing/<int:list_id>',views.commentOnListing,name='commentOnListing'),
    path('bidOnListing/<int:list_id>',views.bidOnListing,name='bidOnListing'),
    path('declareWinner/<int:list_id>',views.declareWinner,name='declareWinner'),
]
