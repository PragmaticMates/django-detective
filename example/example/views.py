from django.views.generic import TemplateView


class ViewA(TemplateView):
    template_name = 'example/A.html'


class ViewB(TemplateView):
    template_name = 'example/B.html'


class ViewC(TemplateView):
    template_name = 'example/C.html'
