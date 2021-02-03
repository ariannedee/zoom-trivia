from django import template

register = template.Library()


@register.filter(name='get_answer')
def get_answer(answers, question_id):
    return answers.get(question_id, '')
