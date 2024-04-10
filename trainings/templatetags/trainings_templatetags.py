from django import template
from datetime import timedelta


register = template.Library()


@register.filter
def round_dt(value):
    if value is None:
        return None

    msec = round(value.microseconds, -5)
    output = timedelta(seconds=value.seconds, microseconds=msec)

    if output.microseconds:
        output = str(output)[:-5]
    else:
        output = str(output) + '.0'

    return output
