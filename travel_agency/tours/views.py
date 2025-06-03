from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Destination, Tour
from django.db.models import Q
from .forms import BookingForm

def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    destinations = Destination.objects.all()[:5]
    tours = Tour.objects.all().order_by('-id')[:4]  # заменили '-created' на '-id'
    return render(request, 'index.html', {'destinations': destinations, 'tours': tours})

def tours_list(request):
    query = request.GET.get('q', '')
    if query:
        tours = Tour.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(destination__name__icontains=query)
        )
    else:
        tours = Tour.objects.all()
    return render(request, 'tours_list.html', {'tours': tours, 'query': query})

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour_detail.html', {'tour': tour})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте данные.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.save()
            messages.success(request, 'Тур успешно забронирован!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка при бронировании.')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'tour': tour, 'form': form})