from django import template

# from django.template import engines
from django.template import Template, Context
register = template.Library()


@register.filter(name='render_str')
def render_str(content):
    template = Template(content)

    context = Context({'title': 'Hello, world!'})
    rendered_html = template.render(context)
    
    return rendered_html

# @register.filter(name='render_str')
# def render_str(content):
#     django_engine = engines["django"]
#     template = django_engine.from_string(content)

#     return template

