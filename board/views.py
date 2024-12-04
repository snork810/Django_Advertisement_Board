from django.shortcuts import render, redirect
from board.models import Advertisement
from board.forms import AdvertisementForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def logout_view(request):
    """Выход пользователя из системы и перенаправление на главную страницу."""
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate


def signup(request):
    """Регистрация нового пользователя. При успешной регистрации происходит автоматический вход."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/board')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    """Отображение главной страницы сайта."""
    return render(request, 'home.html')


def advertisement_list(request):
    """Отображение списка всех объявлений на доске."""
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    """Отображение деталей конкретного объявления по его идентификатору (PK)."""
    advertisement = Advertisement.objects.get(pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


@login_required
def add_advertisement(request):
    """Добавление нового объявления пользователем. Доступно только для авторизованных пользователей."""
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.save()
            return redirect('board:advertisement_list')
    else:
        form = AdvertisementForm()
    return render(request, 'board/add_advertisement.html', {'form': form})


@login_required
def edit_advertisement(request, pk):
    """Редактирование существующего объявления. Доступно только для авторизованных пользователей и авторов объявления."""
    advertisement = Advertisement.objects.get(pk=pk)

    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})
