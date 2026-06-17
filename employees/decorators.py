from django.contrib.auth.decorators import user_passes_test


def hr_required(view_func):
    decorated_view = user_passes_test(
        lambda user: user.is_staff,
        login_url='login'
    )(view_func)

    return decorated_view