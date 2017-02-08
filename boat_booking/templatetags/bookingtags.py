from __future__ import division

import datetime
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from django.utils.dateformat import format
from django.utils.html import escape
from django.utils import timezone
from django.utils.safestring import mark_safe


from schedule.settings import CHECK_EVENT_PERM_FUNC, CHECK_CALENDAR_PERM_FUNC, SCHEDULER_PREVNEXT_LIMIT_SECONDS
from schedule.models import Calendar
from schedule.periods import weekday_names, weekday_abbrs

register = template.Library()

@register.filter
def month_name(value):
    return value.strftime('%B')[0:3]

    
