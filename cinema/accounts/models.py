from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    
    """
    Represents a user's profile
    """

    user = models.OneToOneField(User,on_delete=models.CASCADE, verbose_name='حساب کاربری')
    mobile = models.CharField('تلفن همراه', max_length=11)
    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('تصویر', upload_to='users/profile_images/', null=True, blank=True)
    
    MALE = 1
    FEMALE = 2
    gender_choices = (
        (MALE, 'مرد'),
        (FEMALE, 'زن')
    )
    gender = models.IntegerField('جنسیت', choices=gender_choices)
    balance = models.IntegerField('اعتبار', default=0)

    class Meta:
        verbose_name = 'نمایه کاربری'
        verbose_name_plural = 'نمایه کاربری'

    def __str__(self):
        return self.user.get_full_name()
    
    def get_balance_display(self):
        return '{} تومان'.format(self.balance)

    def deposite(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True

class Payment(models.Model):
    """
    Represents a payment done by a user
    """

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.PositiveIntegerField('مبلغ')
    transaction_time = models.DateTimeField('زمان تراکنش', auto_now_add=True)
    transaction_code = models.CharField('رسید تراکنش', max_length=30)
    
    def __str__(self):
        return '{} تومان افزایش اعتبار برای {}'.format(self.amount, self.profile)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'