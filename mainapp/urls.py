from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.IndexView.as_view(), name='home'),
    path('yandex/', RedirectView.as_view(url='https://yandex.ru/search/', query_string=True), name='yandex'),

    # News
    # path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),
    # path('news/<int:page>/', views.NewsWithPagination.as_view(), name='news_page'),
    path('news/', cache_page(300)(views.NewsListView.as_view()), name='news'),

    # Courses
    # path('courses/', views.CoursesListView.as_view(), name='courses'),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name="courses_detail"),
    path('courses/course_feedback/', views.CourseFeedbackFormView.as_view(), name="course_feedback"),
    path('courses/', cache_page(300)(views.CoursesListView.as_view()), name='courses'),  # 10 minutes

    # Logs
    path('logs/', views.LogView.as_view(), name='logs_list'),
    path('logs/download/', views.LogDownloadView.as_view(), name='logs_download'),
]
