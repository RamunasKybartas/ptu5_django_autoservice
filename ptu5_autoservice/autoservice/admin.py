from django.contrib import admin
from . import models


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 0
    can_delete = False


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'license_plate_number', 'car_model', 'vin_code')
    list_filter = ('client', 'car_model')
    search_fields = ('license_plate_number', 'vin_code')


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_date', 'is_overdue')
    list_display = ('id', 'car', 'order_date', 'due_back', 'total_amount', 'owner')
    inlines = (OrderLineInline, )
    list_editable = ('due_back', 'owner')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'amount', 'price', 'total', 'order')
    ordering = ('order', 'id')
    list_filter = ('order', )

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'reviewer', 'created_at')

admin.site.register(models.CarModel)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.OrderReview, OrderReviewAdmin)

