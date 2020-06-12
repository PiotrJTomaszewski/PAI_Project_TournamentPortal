from django import template
from libgravatar import Gravatar

register = template.Library()

# @register.filter(name='longifyDeckFormat')
# def longifyDeckFormat(value):
#     return TournamentDeckFormatChoice[value].value

# @register.filter(name="longifyGameFormat")
# def longifyGameFormat(value):
#     return TournamentGameFormatChoice[value].value

# @register.filter(name="longifyLocationType")
# def longifyLocationType(value):
#     return TournamentLocationChoice[value].value

@register.filter(name='bootstrapAlertType')
def bootstrapAlertType(value):
    if value == 'error':
        return 'alert-danger'
    if value == 'success':
        return 'alert-success'
    if value == 'info':
        return 'alert-primary'
    return 'NOTFOUND'+value

@register.filter(name='gravatar')
def gravatar_url(email, size=40):
    return Gravatar(email).get_image(size=size, default='retro')
