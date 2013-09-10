from django.http import Http404
from django.shortcuts import get_object_or_404


def preview(view):
    """
    Decorator that takes a model class and returns an instance based on whether
    the model is viewable by the current user.
    """
    def is_staff(request, **kwargs):
        if request.user.is_staff:
            return view
        else:
            raise Http404

    return is_staff
