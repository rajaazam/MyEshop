from django import template

register = template.Library()


@register.filter(name='currency')
def currency(number):
    return "₨."+str(number)

@register.filter(name='multiply')
def multiply(no1,no2):

    return no1*no2