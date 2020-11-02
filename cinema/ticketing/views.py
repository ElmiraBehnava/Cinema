from django.shortcuts import render, reverse
from .models import Movie, Cinema, ShowTime, Ticket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import ShowTimeSearchForm


# Create your views here.


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'ticketing/movie_list.html', {"movies" : movies})


def cinema_list(request):
    cinemas = Cinema.objects.all()
    return render(request, 'ticketing/cinema_list.html', {"cinemas" : cinemas})


def movie_details(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'ticketing/movie_details.html', {"movie" : movie})


def cinema_details(request, cinema_id):
    cinema = Cinema.objects.get(pk=cinema_id)
    return render(request, 'ticketing/cinema_details.html', {"cinema" : cinema})


def showtime_list(request):
    showtimes = ShowTime.objects.all()
    search_form = ShowTimeSearchForm(request.GET)
    if search_form.is_valid():
        showtimes = showtimes.filter(movie__name__contains=search_form.cleaned_data['movie_name'])
        if search_form.cleaned_data['sale_is_open']:
            showtimes = showtimes.filter(status=ShowTime.SALE_OPEN)
        if search_form.cleaned_data['movie_length_min'] is not None:
            showtimes = showtimes.filter(movie__length__gte=search_form.cleaned_data['movie_length_min'])
        if search_form.cleaned_data['movie_length_max'] is not None:
            showtimes = showtimes.filter(movie__length__lte=search_form.cleaned_data['movie_length_max'])
        if search_form.cleaned_data['cinema'] is not None:
            showtimes = showtimes.filter(cinema=search_form.cleaned_data['cinema'])
        min_price, max_price = search_form.get_price_boundries()
        if min_price is not None:
            showtimes = showtimes.filter(price__gt=min_price)
        if max_price is not None:
            showtimes = showtimes.filter(price__lte=max_price)
    showtimes = showtimes.order_by('start_time')
    context = {
        'search_form': search_form,
        "showtimes" : showtimes

    }
    return render(request, 'ticketing/showtime_list.html', context)

@login_required
def showtime_details(request, showtime_id):
    showtime = ShowTime.objects.get(pk=showtime_id)
    context = {
        'showtime': showtime,
    }
    if request.method == 'POST':
        try:
            seat_count = int(request.POST['seat_count'])
            assert showtime.status == showtime.SALE_OPEN, 'فروش بلیت برای این سانس ممکن نیست.'
            assert showtime.free_seats >= seat_count, 'این سانس به اندازه کافی صندلی خالی ندارد.'
            price = showtime.price * seat_count
            assert request.user.profile.spend(price), 'اعتبار شما برای خرید بلیت کافی نیست.'
            showtime.reserve_seats(seat_count)
            ticket = Ticket.objects.create(showtime=showtime, customer=request.user.profile, seat_count=seat_count)
        except Exception as e:
            context['error'] = str(e)
        else:
            return HttpResponseRedirect(reverse('ticketing:ticket_details', kwargs={'ticket_id': ticket.id}))

    
    return render(request, 'ticketing/showtime_details.html', context)



@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    return render(request, 'ticketing/ticket_list.html', {"tickets":tickets})


@login_required
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    return render(request, 'ticketing/ticket_details.html', {"ticket":ticket})