from django.core.management.base import BaseCommand, CommandError
import json
import requests
import re
from core.settings import FIXTURE_DIR
from product.models import Category, SubCategory, GroupCategory
from os.path import join, isfile


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
group_category_file = join(FIXTURE_DIR, 'group_category.json')
category_file = join(FIXTURE_DIR, 'category.json')
subcategory_file = join(FIXTURE_DIR, 'subcategory.json')


# def get_group_category():
#     url = 'https://comfy.ua/api/categories/list/5'
#     request = requests.get(url, headers=headers)
#     result = re.search(r'\{\"items\":(.*?)\]\}\]\}\]\}', request.text)
#     tmpstr = result.group(1)
#     ready = tmpstr + ']}]}]}]'
#     with open(group_category_file, 'w') as f:
#         f.write(ready)
#     print('Saving ' + group_category_file)


# def get_category():
#     url = 'https://comfy.ua/api/categories/list/5'
#     request = requests.get(url, headers=headers)
#     result = re.search(r'\{\"items\":(.*?)\]\}\]\}\]\}', request.text)
#     tmpstr = result.group(1)
#     ready = tmpstr + ']}]}]}]'
#     with open(category_file, 'w') as f:
#         f.write(ready)
#     print('Saving ' + category_file)
#
#
# def get_subcategory():
#     url = 'https://comfy.ua/api/categories/list/5'
#     request = requests.get(url, headers=headers)
#     result = re.search(r'\"childs\":(.*?)\}\]', request.text)
#     tmpstr = result.group(1)
#     ready = tmpstr + '}]'
#     with open(subcategory_file, 'w') as f:
#         f.write(ready)
#     print('Saving ' + subcategory_file)


def save_group_category():
    GroupCategory.objects.all().delete()

    with open(group_category_file, 'r') as f:
        content = f.read()
        data = json.loads(content)
        for i in data:
            url = i['manual_url']
            manual = url.replace('https://rozetka.com.ua/', '').partition('/')[0]
            GroupCategory.objects.create(
                name=i['title'],
                category_id=i['id'],
                slug=manual,
                order=i['order'],
                # icon='https://comfy.ua/' + i['thumbnail'].split.partition('/')[1]
            )
            print(i['title'])


def save_category():
    Category.objects.all().delete()

    with open(category_file, 'r') as f:
        content = f.read()
    data = json.loads(content)
    for cat in data:
        group_cat = GroupCategory.objects.get(category_id=cat['parent_id'])
        url = cat['manual_url']
        manual = url.replace('https://rozetka.com.ua/', '').partition('/')[0]
        Category.objects.create(
            name=cat['title'],
            category_id=cat['id'],
            slug=manual,
            group_category=group_cat
        )
        print(cat['title'])


def save_subcategory():
    SubCategory.objects.all().delete()

    with open(subcategory_file, 'r') as f:
        content = f.read()
    data = json.loads(content)
    for sub_cat in data:
        cat = Category.objects.get(category_id=sub_cat['parent_id'])
        url = sub_cat['manual_url']
        manual = url.replace('https://rozetka.com.ua/', '').partition('/')[0]
        SubCategory.objects.create(
            name=sub_cat['title'],
            category_id=sub_cat['id'],
            slug=manual,
            parent_category=cat
        )
        print(sub_cat['title'])

    # with open(subcategory_file, 'r') as f:
    #     content = f.read()
    #     data = json.loads(content)
    #     for sub in data:
    #         with open(category_file, 'r') as f:
    #             content = f.read()
    #             data = json.loads(content)
    #             for cat in data:
    #                 parent_id = Category.objects.get(category_id=cat['id'])
    #             # sub_cat.parent.add(parent_id)
    #                 print(parent_id)
    #         sub_cat = SubCategory.objects.create(
    #             name = sub['Name'], 
    #             cat_id = sub['id'], 
    #             slug = sub['urlKey'], 
    #             parent = parent_id
    #         )
    #         print(sub['Name'])


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Parser')

        # if not isfile(group_category_file):
        #     get_group_category()
        # if not isfile(category_file):
        #     get_category()
        # if not isfile(subcategory_file):
        #     get_subcategory()

        save_group_category()
        save_category()
        save_subcategory()
