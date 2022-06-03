from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig
from django.views.generic.base import RedirectView

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('docsite/', views.DocSiteView.as_view(), name='docsite'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.IndexView.as_view(), name='home'),
    path('yandex/', RedirectView.as_view(url='https://yandex.ru/search/', query_string=True), name='yandex'),


    # News
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/add/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:page>/', views.NewsWithPagination.as_view(), name='news_page'),


    #Courses
    path('courses/', views.CoursesListView.as_view(), name="courses"),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name="courses_detail"),
    path('courses/course_feedback/', views.CourseFeedbackFormView.as_view(), name="course_feedback"),
    path('courses/', views.CoursesView.as_view(), name='courses'),
]

