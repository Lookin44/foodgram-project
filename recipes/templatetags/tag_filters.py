from django import template

from recipes.models import Tag

register = template.Library()


@register.filter
def get_filter_tags(request, tag):
    new_request = request.GET.copy()
    all_tags = Tag.objects.all()
    tags_list = request.GET.getlist('tags')

    if not tags_list:
        for tag_item in all_tags:
            tags_list.append(tag_item.value)

    if tag in tags_list:
        tags_list.remove(tag)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag)
    return new_request.urlencode()
