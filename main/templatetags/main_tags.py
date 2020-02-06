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

# Counts comments and replies at publication together
@register.filter
def count_comments(publication):
    query = publication.comment_set
    count = query.count()

    for comment in query.all():
        count += comment.reply_set.count()

    return count
