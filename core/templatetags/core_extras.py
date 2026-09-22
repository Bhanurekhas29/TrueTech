from django import template

register = template.Library()


@register.filter
def split_csv(value):
    """Split a comma-separated string into a list of trimmed, non-empty strings."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@register.filter
def split_lines(value):
    """Split a newline-separated string into a list of trimmed, non-empty lines."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]
