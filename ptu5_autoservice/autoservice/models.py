from django.db import models
from datetime import date
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _

class CarModel(models.Model):
    YEAR_CHOICES = ((year, str(year)) for year in reversed(range(1899, date.today().year+1)))
    make = models.CharField(_('make'), max_length=50)
    model = models.CharField(_('model'), max_length=50)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES)
    engine = models.CharField(_('engine'), max_length=50)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}), {self.engine}"

    class Meta:
        ordering = ['make']
        verbose_name = _('Car model')
        verbose_name_plural = _('Car models')


class Service(models.Model):
    title = models.CharField(_('title'), max_length=50)
    price = models.DecimalField(_('price'), max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.title}: {self.price}"

    class Meta:
        ordering = ['title']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Car(models.Model):
    license_plate_number = models.CharField(_('license plate number'), max_length=10)
    vin_code = models.CharField(_('vin code'), max_length=17)
    client = models.CharField(_('client name'), max_length=200)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name=_('car model'), related_name='cars')
    photo = models.ImageField(_("photo"), upload_to='photos', blank=True, null=True)
    description = HTMLField(_('description'),  max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.car_model.make} {self.car_model.model} {self.license_plate_number}, {self.vin_code}, {self.client}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    STATUS_CHOICES = (
        ('n', _('new')),
        ('a', _('advance payment taken')),
        ('o', _('ordered parts')),
        ('w', _('working')),
        ('d', _('done')),
        ('c', _('cancelled')),
        ('p', _('paid')),
    )
    order_date = models.DateTimeField(_('order date'), auto_now_add=True, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(_('total amount'), max_digits=18, decimal_places=2, default=0)
    due_back = models.DateField(_('due back'), null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), verbose_name=_("owner"), on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(_("status"), max_length=1, choices=STATUS_CHOICES, default='n')
    
    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False

    def __str__(self) -> str:
        return f" {self.car}: {self.total_amount}, {self.order_date}"

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.total
        return total
    
    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.total_amount = self.get_total()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order_date'] 
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderLine(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_('service'), related_name='order_lines')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'), related_name='order_lines')
    amount = models.IntegerField(_('amount'), default=1)
    price = models.DecimalField(_('price'), max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f" {self.service.title}: {self.amount} x {self.price}"

    @property
    def total(self):
        return self.amount * self.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.save()

class OrderReview(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"), on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(get_user_model(), verbose_name=_('reviewer'), on_delete=models.CASCADE, related_name='order_reviews')
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=2000)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return f"{self.reviewer} on {self.order} at {self.created_at}"