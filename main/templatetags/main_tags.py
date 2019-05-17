from django import template

register = template.Library()

# Returns the text for like button for current user at the publication page
@register.filter
def like_btn_text(publication, user):
    if (user not in publication.likes.all()):
        return "нравится"
    else:
        return "не нравится"

# Returns the text for subscribe button for current user
@register.filter
def subscribe_btn_text(profile, user):
    if (user not in profile.subscribers.all()):
        return "подписаться"
    else:
        return "отписаться"
