from django import template

register = template.Library()


def is_empty(value, alt):
    if value:
        return value
    return alt


def format_code(code: str):
    return code.replace("\n", "<br>")


register.filter('is_empty', is_empty)
register.filter('format_code', format_code)
