from django.core.management import BaseCommand
from mainapp.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        news_list = []
        for i in range(1, 11):
            news_list.append(News(
                title=f"title#{i}",
                preambule=f"preambule#{i}",
                body="Текст новости"
            ))

        News.objects.bulk_create(news_list)

