from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
from django.core.files import File
import shutil
from core.settings import BASE_DIR

from product.models import Category, SubCategory, Product

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 '
                  'Safari/537.36',
    'accept': '*/*'
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Clearing DB')

        # удаляем записи и картинки
        Category.objects.all().delete()
        # SubCategory.objects.all().delete()
        Product.objects.all().delete()
        try:
            shutil.rmtree('%s/media' % BASE_DIR)
        except:
            pass

        # достаем главную страницу и парсим
        URL = 'https://rozetka.com.ua/rasprodaja/c83850/'
        print('Start importing from %s' % URL)
        rez = requests.get(URL, headers=HEADERS, verify=False)
        soup = BeautifulSoup(rez.text, 'html.parser')

        # находим нужный див и в нем картинки
        content = soup.find('ul', {'class': 'portal-navigation'})
        cont_li = content.find_all('li', {'class': 'portal-navigation__item'})
        print('[INFO] - %s' % content)
        print('[INFO] - %s' % cont_li)
        for item in cont_li.findAll('a'):
            c = Category()
            c.slug = item.get('href')
            c.name = item.find('span', {'class': 'class="portal-navigation__link-text'})
        #     img_url = img.get('src')
            # img_response = requests.get(img_url, stream=True, verify=False)
            #
            # # сохраняем временный файл
            # with open('tmp.png', 'wb') as out_file:
            #     shutil.copyfileobj(img_response.raw, out_file)
            #
            # # читаем временный файл и загружаем его программно в модель
            # with open('%s/tmp.png' % BASE_DIR, 'rb') as img_file:
            #     c.icon.save('cat.png', File(img_file), save=True)

            c.save()
            # print(item)
            # print('Saving ... %s' % c.name)
            # print('Saving ... %s' % c.slug)



            # c.save()
            # # забираем подкатегории
            # for subcat in img.find_parent('tr').find('div').findAll('a'):
            #     sc = SubCategory()
            #     sc.category = c
            #     sc.name = subcat.text
            #     sc.save()
            #     get_products(c, sc, subcat.get('href'))
