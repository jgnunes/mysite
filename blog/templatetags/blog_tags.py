import datetime
import json

from django import template
from django.utils import timezone

from ..forms import PublicationForm

register = template.Library()


@register.inclusion_tag('blog/_form.html')
def blog_form():
    form = PublicationForm()
    return {'form': form}