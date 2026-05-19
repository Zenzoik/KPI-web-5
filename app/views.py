from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .auth import authenticate_user, get_current_user, is_admin, page_context, set_flash
from .forms import FuelItemForm, FuelTypeForm, IssueRecordForm
from .models import FuelItem, FuelType, IssueRecord, User


def render_page(request, template_name, context=None):
    return render(request, template_name, page_context(request, context))


def require_login(request):
    user = get_current_user(request)
    if user is None:
        set_flash(request, "Для цієї дії потрібно увійти в систему.")
    return user


def require_admin(request):
    user = require_login(request)
    if user is not None and not is_admin(user):
        set_flash(request, "Ця дія доступна тільки адміністратору.")
        return None
    return user


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate_user(username, password)

        if user is None:
            set_flash(request, "Неправильний логін або пароль.")
            return redirect("login")

        request.session["user_id"] = user.id
        return redirect("home")

    return render_page(request, "app/login.html")


def logout(request):
    request.session.flush()
    return redirect("home")


def home(request):
    fuels = FuelItem.objects.select_related("fuel_type").all()
    context = {
        "fuels": fuels[:3],
        "fuel_count": FuelItem.objects.count(),
        "type_count": FuelType.objects.count(),
        "issue_count": IssueRecord.objects.count(),
    }
    return render_page(request, "app/index.html", context)


def sqlite_info(request):
    context = {
        "database_name": "db.sqlite3",
        "fuel_count": FuelItem.objects.count(),
        "type_count": FuelType.objects.count(),
        "issue_count": IssueRecord.objects.count(),
        "user_count": User.objects.count(),
        "recent_fuels": FuelItem.objects.select_related("fuel_type").all()[:5],
    }
    return render_page(request, "app/sqlite.html", context)


def fuels(request):
    selected_type = request.GET.get("type")
    fuels_list = FuelItem.objects.select_related("fuel_type").all()

    if selected_type:
        fuels_list = fuels_list.filter(fuel_type_id=selected_type)

    context = {
        "fuels": fuels_list,
        "fuel_types": FuelType.objects.all(),
        "selected_type": selected_type,
    }
    return render_page(request, "app/fuels.html", context)


def fuel_detail(request, fuel_id):
    fuel = get_object_or_404(FuelItem.objects.select_related("fuel_type"), id=fuel_id)
    context = {
        "fuel": fuel,
    }
    return render_page(request, "app/fuel_detail.html", context)


def fuel_create(request):
    if require_admin(request) is None:
        return redirect("home")

    if request.method == "POST":
        form = FuelItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fuels")
    else:
        form = FuelItemForm()

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Додати ПММ", "cancel_url": "fuels"},
    )


def fuel_edit(request, fuel_id):
    if require_admin(request) is None:
        return redirect("home")

    fuel = get_object_or_404(FuelItem, id=fuel_id)

    if request.method == "POST":
        form = FuelItemForm(request.POST, instance=fuel)
        if form.is_valid():
            form.save()
            return redirect("fuel_detail", fuel_id=fuel.id)
    else:
        form = FuelItemForm(instance=fuel)

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Редагувати ПММ", "cancel_url": "fuels"},
    )


def fuel_delete(request, fuel_id):
    if require_admin(request) is None:
        return redirect("home")

    fuel = get_object_or_404(FuelItem, id=fuel_id)

    if request.method == "POST":
        try:
            fuel.delete()
            return redirect("fuels")
        except ProtectedError:
            context = {
                "object_name": fuel.name,
                "cancel_url": "fuels",
                "error": "Позицію не можна видалити, бо вона є у журналі операцій.",
            }
            return render_page(request, "app/confirm_delete.html", context)

    return render_page(
        request,
        "app/confirm_delete.html",
        {"object_name": fuel.name, "cancel_url": "fuels"},
    )


def issue_fuel(request, fuel_id):
    user = require_login(request)
    if user is None:
        return redirect("login")

    fuel = get_object_or_404(FuelItem, id=fuel_id)

    if request.method == "POST":
        form = IssueRecordForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = user
            issue.fuel_item = fuel
            if issue.amount_liters > fuel.quantity_liters:
                form.add_error("amount_liters", "На складі немає такого обсягу.")
            else:
                issue.save()
                fuel.quantity_liters -= issue.amount_liters
                fuel.save()
                return redirect("issues")
    else:
        form = IssueRecordForm(initial={"fuel_item": fuel})

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Оформити видачу", "cancel_url": "fuels"},
    )


def fuel_types(request):
    context = {
        "fuel_types": FuelType.objects.all(),
    }
    return render_page(request, "app/fuel_types.html", context)


def fuel_type_create(request):
    if require_admin(request) is None:
        return redirect("home")

    if request.method == "POST":
        form = FuelTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fuel_types")
    else:
        form = FuelTypeForm()

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Додати тип ПММ", "cancel_url": "fuel_types"},
    )


def fuel_type_edit(request, type_id):
    if require_admin(request) is None:
        return redirect("home")

    fuel_type = get_object_or_404(FuelType, id=type_id)

    if request.method == "POST":
        form = FuelTypeForm(request.POST, instance=fuel_type)
        if form.is_valid():
            form.save()
            return redirect("fuel_types")
    else:
        form = FuelTypeForm(instance=fuel_type)

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Редагувати тип ПММ", "cancel_url": "fuel_types"},
    )


def fuel_type_delete(request, type_id):
    if require_admin(request) is None:
        return redirect("home")

    fuel_type = get_object_or_404(FuelType, id=type_id)

    if request.method == "POST":
        try:
            fuel_type.delete()
            return redirect("fuel_types")
        except ProtectedError:
            context = {
                "object_name": fuel_type.name,
                "cancel_url": "fuel_types",
                "error": "Тип не можна видалити, бо до нього прив'язані позиції ПММ.",
            }
            return render_page(request, "app/confirm_delete.html", context)

    return render_page(
        request,
        "app/confirm_delete.html",
        {"object_name": fuel_type.name, "cancel_url": "fuel_types"},
    )


def issues(request):
    user = require_login(request)
    if user is None:
        return redirect("login")

    issues_list = IssueRecord.objects.select_related("fuel_item", "user").all()
    if not is_admin(user):
        issues_list = issues_list.filter(user=user)

    context = {
        "issues": issues_list,
    }
    return render_page(request, "app/issues.html", context)


def issue_create(request):
    user = require_login(request)
    if user is None:
        return redirect("login")

    if request.method == "POST":
        form = IssueRecordForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = user
            fuel = issue.fuel_item
            if issue.amount_liters > fuel.quantity_liters:
                form.add_error("amount_liters", "На складі немає такого обсягу.")
            else:
                issue.save()
                fuel.quantity_liters -= issue.amount_liters
                fuel.save()
                return redirect("issues")
    else:
        form = IssueRecordForm(initial={"issued_at": timezone.localtime().strftime("%Y-%m-%dT%H:%M")})

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Додати операцію", "cancel_url": "issues"},
    )


def issue_edit(request, issue_id):
    if require_admin(request) is None:
        return redirect("home")

    issue = get_object_or_404(IssueRecord, id=issue_id)

    if request.method == "POST":
        form = IssueRecordForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect("issues")
    else:
        form = IssueRecordForm(instance=issue)

    return render_page(
        request,
        "app/form.html",
        {"form": form, "form_title": "Редагувати операцію", "cancel_url": "issues"},
    )


def issue_delete(request, issue_id):
    if require_admin(request) is None:
        return redirect("home")

    issue = get_object_or_404(IssueRecord, id=issue_id)

    if request.method == "POST":
        issue.delete()
        return redirect("issues")

    return render_page(
        request,
        "app/confirm_delete.html",
        {"object_name": str(issue), "cancel_url": "issues"},
    )
