from django.contrib.auth.decorators import login_required


class LoginRequiredMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        return login_required(view_func)(request, *view_args, **view_kwargs)
