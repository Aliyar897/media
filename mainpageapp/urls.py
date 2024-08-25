from django.urls import path
from . import views
from .views import SummarizePendingNewsAPIView

urlpatterns = [
    path('home', views.home, name='home'),
    path('get_new_post', views.get_new_post, name='get_new_post'),
    path('', views.news_list, name='news_list'),  # URL pattern
    path('summary/', views.summary_api, name='summary_api'),  # URL pattern
    path('get_text/', views.get_text, name='get_text'),  # URL pattern
    path('test_req/', views.test_req, name='test_req'),  # URL pattern
    path('get_news_posts/', views.get_news_api, name='get_news_api'),
    path('api/summarize_pending/', SummarizePendingNewsAPIView.as_view(), name='summarize-pending-news'),
    path('increment-view-count/<int:post_id>/', views.like_post, name='increment_view_count'),
    
]