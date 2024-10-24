from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]
