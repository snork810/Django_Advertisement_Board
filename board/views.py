from django.shortcuts import render, redirect, get_object_or_404
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
    """Отображение главной страницы сайта с данными о пользователе."""
    if request.user.is_authenticated:  # Проверка, авторизован ли пользователь
        # Получаем профиль пользователя и количество его объявлений
        advertisement_count = request.user.profile.advertisement_count
    else:
        advertisement_count = 0

    return render(request, 'home.html', {
        'username': request.user.username,
        'advertisement_count': advertisement_count,
    })


def advertisement_list(request):
    """Отображение списка всех объявлений на доске."""
    advertisements = Advertisement.objects.all()
    return render(request, 'board/advertisement_list.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    """Отображение деталей конкретного объявления по его идентификатору (PK)."""
    advertisement = Advertisement.objects.get(pk=pk)
    print(f"Image URL: {advertisement.image.url if advertisement.image else 'No image'}")
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})


@login_required
def add_advertisement(request):
    """Добавление нового объявления пользователем. Доступно только для авторизованных пользователей."""
    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES)
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
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            form.save()
            return redirect('board:advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)

    return render(request, 'board/edit_advertisement.html', {'form': form, 'advertisement': advertisement})


@login_required
def like_advertisement(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)

    if request.user in advertisement.likes.all():
        advertisement.likes.remove(request.user)
    else:
        advertisement.likes.add(request.user)

    return redirect('board:advertisement_detail', pk=advertisement.pk)


@login_required
def dislike_advertisement(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)

    if request.user in advertisement.dislikes.all():
        advertisement.dislikes.remove(request.user)
    else:
        advertisement.dislikes.add(request.user)

    return redirect('board:advertisement_detail', pk=advertisement.pk)


@login_required
def delete_advertisement(request, pk):
    """Удаление объявления с подтверждением пользователя."""
    advertisement = Advertisement.objects.get(pk=pk)

    if request.method == "POST":
        advertisement.delete()
        return redirect('board:advertisement_list')

    return render(request, 'board/delete_advertisement.html', {'advertisement': advertisement})
