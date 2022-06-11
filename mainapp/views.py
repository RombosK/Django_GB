import logging

logger = logging.getLogger(__name__)
# from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, DeleteView, View
# import json
from mainapp.models import News, Courses, Lesson, CourseTeachers, CourseFeedback

from config import settings
from django.core.cache import cache

from mainapp import tasks
from mainapp.forms import CourseFeedbackForm
from mainapp import forms


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['contacts'] = [
            {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHcrhA',
                'city': 'Санкт‑Петербург',
                'phone': '+7-999-11-11111',
                'email': 'geeklab@spb.ru',
                'adress': 'территория Петропавловская крепость, 3Ж'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHX3xB',
                'city': 'Казань',
                'phone': '+7-999-22-22222',
                'email': 'geeklab@kz.ru',
                'adress': 'территория Кремль, 11, Казань, Республика Татарстан, Россия'
            }, {
                'map': 'https://yandex.ru/map-widget/v1/-/CCUAZHh9kD',
                'city': 'Москва',
                'phone': '+7-999-33-33333',
                'email': 'geeklab@msk.ru',
                'adress': 'Красная площадь, 7, Москва, Россия'
            }
        ]
        return context_data

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


# class CoursesView(TemplateView):
#     template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsListView(ListView):
    model = News
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News

    def get_object(self, queryset=None):
        return get_object_or_404(News, pk=self.kwargs.get('pk'), deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


# class NewsWithPagination(NewsListView):
#
#     def get_context_data(self, page, **kwargs):
#         context = super().get_context_data(page=page, **kwargs)
#         context["page_num"] = page
#         return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = forms.CourseFeedbackForm(
                user=self.request.user
            )
        return context

    # def post(self, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         cache_lock_flag = cache.get(
    #             f"mail_feedback_lock_{self.request.user.pk}"
    #         )
    #
    #         if not cache_lock_flag:
    #             cache.set(
    #                 f"mail_feedback_lock_{self.request.user.pk}",
    #                 "lock",
    #                 timeout=300,
    #             )
    #             messages.add_message(
    #                 self.request, messages.INFO, f"Message sended"
    #             )
    #             tasks.send_feedback_mail.delay(
    #                 {
    #                     "user_id": self.request.POST.get("user_id"),
    #                     "message": self.request.POST.get("message"),
    #                 }
    #             )
    #         else:
    #             self.message = messages.add_message(self.request, messages.WARNING,
    #                                                 f"You can send only one message per 5 minutes", )
    #     return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class CoursesListView(TemplateView):
    template_name = "mainapp/courses_list.html"
    model = Courses
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context['objects'] = Courses.objects.all()

        return context


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Courses, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeachers.objects.filter(course=context_data['course_object'])
        feedback_list_key = f"course_feedback{context_data['course_object'].pk}"
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=300)
        else:
            context_data['feedback_list'] = cached_feedback_list

        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(
                    course=context_data["course_object"],
                    user=self.request.user).count():
                context_data['feedback_form'] = CourseFeedbackForm(
                    course=context_data['course_object'],
                    user=self.request.user
                )

        return context_data


class CourseFeedbackFormView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string('mainapp/includes/feedback_block.html', context={'item': self.object})
        return JsonResponse({'card': rendered_card})


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):

        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        logs_line = 1000  # Заданное кол-во строк последних логов
        last_line = sum(1 for line in open(settings.LOG_FILE))
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                cnt = (last_line - logs_line)
                if i < cnt:
                    continue
                log_slice.insert(0, f'{i} {line}')
            context["logs"] = log_slice
        return context


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
