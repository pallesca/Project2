from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path('watchlist/<str:user_id>', views.watchlist, name='watchlist'),
    path('watchlist/add/', views.add_watchlist, name='add_watchlist'),
    path('watchlist/delete/', views.delete_watchlist, name='delete_watchlist')
    # path(r'^category-detail/(?P<slug>[-\w]+)/$', views.category-detail, name='category-detail')
]
