from .models import User


def get_current_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def authenticate_user(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if user.check_password(password):
        return user
    return None


def set_flash(request, message):
    request.session["flash_message"] = message


def pop_flash(request):
    return request.session.pop("flash_message", None)


def page_context(request, context=None):
    if context is None:
        context = {}

    context["current_user"] = get_current_user(request)
    context["flash_message"] = pop_flash(request)
    return context


def is_admin(user):
    return user is not None and user.role == "admin"
