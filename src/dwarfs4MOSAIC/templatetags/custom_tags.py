from django import template

register = template.Library()

@register.simple_tag
def html_title(title):
    return f"{title} | Dwarfs4MOSAIC"

@register.simple_tag
def html_observatory_title(observatoy_name):
    base_title = f"Observatory: {observatoy_name}"
    return html_title(base_title)

@register.simple_tag
def html_telescope_title(telescope_name):
    base_title = f"Telescope: {telescope_name}"
    return html_title(base_title)

@register.simple_tag
def html_observing_run_title(observing_run_name):
    base_title = f"Observing Run: {observing_run_name}"
    return html_title(base_title)