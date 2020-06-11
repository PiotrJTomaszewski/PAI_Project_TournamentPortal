from django import template

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