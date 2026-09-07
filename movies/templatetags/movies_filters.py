from django import template
from movies.models import Review, Report
register = template.Library()

@register.filter(name='get_reports')
def get_reports(review):
    r = Review(review)
    return int(Report.objects.filter(review=review).count())