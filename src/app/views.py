from django.conf import settings
from django.views.generic import TemplateView, View


# def site_name(request):
# 	return {'SITE_NAME': settings.SITE_NAME}


class HomePageView(TemplateView):
	""" Home Page """
	template_name = 'pages/home_page.html'
