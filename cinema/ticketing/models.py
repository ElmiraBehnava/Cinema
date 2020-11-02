from django.db import models

# Create your models here.


class Movie(models.Model):
    """
    Represents a Movie
    """
    name = models.CharField("عنوان فیلم",max_length=100)
    director = models.CharField("نام کارگردان", max_length=50)
    year = models.IntegerField("سال تولید")
    length = models.IntegerField("مدت زمان")
    description = models.TextField("خلاصه فیلم")
    poster = models.ImageField("پوستر", upload_to='movie_poster/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم"


class Cinema(models.Model):
    """
    Represents a Cinema
    """
    name = models.CharField("نام", max_length=50)
    city = models.CharField("شهر", max_length=30, default="تهران")
    capacity = models.IntegerField("ظرفیت")
    phone = models.CharField("تلفن", max_length=20, null=True)
    address = models.TextField("آدرس")
    image = models.ImageField("تصویر", upload_to='cinema_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "سینما"
        verbose_name_plural = "سینما"


class ShowTime(models.Model):
    """
    Represnts a movie show in a cinema at a specific time
    """
    movie = models.ForeignKey("Movie", on_delete=models.PROTECT, verbose_name="عنوان فیلم")
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name = "نام سینما")
    start_time = models.DateTimeField("زمان شروع")
    price = models.IntegerField("قیمت")
    salable_seats = models.IntegerField("صندلی‌های قابل فروش")
    free_seats = models.IntegerField("صندلی‌های خالی")

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELD = 6
    status_choices = (
        (SALE_NOT_STARTED, "فروش آغاز نشده" ),
        (SALE_OPEN,"در حال فروش بلیط"),
        (TICKETS_SOLD,"بلیط‌های تمام شد"), 
        (SALE_CLOSED,"فروش بلیط بسته‌شد"),
        (MOVIE_PLAYED,"فیلم پخش شد"),
        (SHOW_CANCELD,"سانس لغو شد"),
    )
    status = models.IntegerField("وضعیت", choices=status_choices)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return 'تومان {}'.format(self.price)

    def is_full(self):
        """
        Returns True if all seats are sold
        """
        return self.free_seats == 0 

    def open_sale(self):
        """
        Opens ticket sale
        If sale was opened before, raises an exception
        """
        if self.status == ShowTime.SALE_NOT_STARTED:
            self.status = ShowTime.SALE_OPEN
            self.save()
        else:
            raise Exception('Sale has been started before')
    
    def close_sale(self):
        """
        Closes ticket sale
        If sale is not open, raises an exception
        """
        if self.status == ShowTime.SALE_OPEN:
            self.status = ShowTime.SALE_CLOSED
            self.save()
        else:
            raise Exception('Sale isnt open')

    
    def expire_showtime(self, is_canceled=False):
        """
        Expires showtime and updates the status
        :param is_canceled: A boolean indicating whether the show is canceled or not, default is False
        """
        if self.status not in (ShowTime.MOVIE_PLAYED, ShowTime.SHOW_CANCELED):
            self.status = ShowTime.SHOW_CANCELED if is_canceled else ShowTime.MOVIE_PLAYED
            self.save()
        else:
            raise Exception('Show has been expired before')
    
    def reserve_seats(self, seat_count):
        """
        Reserves one or more seats for a customer
        :param seat_count: An integer as the number of seats to be reserved
        """
        assert isinstance(seat_count, int) and seat_count > 0, 'Number of seats should be a positive integer'
        assert self.status == ShowTime.SALE_OPEN, 'Sale is not open'
        assert self.free_seats >= seat_count, 'Not enough free seats'
        self.free_seats -= seat_count
        if self.free_seats == 0:
            self.status = ShowTime.TICKETS_SOLD
        self.save()
    


    
    class Meta:
        verbose_name = "سانس"
        verbose_name_plural = "سانس"
    


class Ticket(models.Model):
    
    """
    Represent a Ticket
    """
    showtime = models.ForeignKey('ShowTime', on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name='خریدار')
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید', auto_now_add=True)


    def __str__(self):
        return "{} بلیت به نام {} برای فیلم {}".format(self.seat_count, self.customer, self.showtime.movie)
        
    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'