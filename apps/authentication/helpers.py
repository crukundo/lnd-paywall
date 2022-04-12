from django.core.exceptions import PermissionDenied
from django.views.generic import View

class AuthorRequiredMixin(View):
    """Mixin to validate than the loggedin user is the creator of the object
    to be edited or updated."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)