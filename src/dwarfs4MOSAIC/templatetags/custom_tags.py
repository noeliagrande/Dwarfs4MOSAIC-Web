"""
Custom template tags for generating HTML titles in the Dwarfs4MOSAIC project.
Each function returns a formatted title string for different entities.
"""

from django import template

# Register a new template library
register = template.Library()

# Base HTML title with the project name appended
@register.simple_tag
def html_title(title):
    return f"{title} | Dwarfs4MOSAIC data"

# Formatted HTML title for an observatory
@register.simple_tag
def html_observatory_title(observatoy_name):
    base_title = f"Observatory: {observatoy_name}"
    return html_title(base_title)

# Formatted HTML title for a telescope
@register.simple_tag
def html_telescope_title(telescope_name):
    base_title = f"Telescope: {telescope_name}"
    return html_title(base_title)

# Formatted HTML title for an observing run.
@register.simple_tag
def html_observing_run_title(observing_run_name):
    base_title = f"Observing Run: {observing_run_name}"
    return html_title(base_title)