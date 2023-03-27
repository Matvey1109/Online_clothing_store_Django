from .models import *
def get_user_context(dict):
    context = dict
    genders = Gender.objects.all()
    context["genders"] = genders
    context["gender_selected"] = -1
    context["cat_selected"] = -1
    return context
