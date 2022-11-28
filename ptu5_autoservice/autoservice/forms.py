from django import forms 
from . models import OrderReview, Order
from django.utils.timezone import timedelta, datetime

class OrderReviewForm(forms.ModelForm):
    def is_valid(self):
        valid = super().is_valid()
        if valid:
            reviewer = self.cleaned_data.get("reviewer")
            recent_posts = OrderReview.objects.filter(reviewer=reviewer, created_at__gte=(datetime.now() - timedelta(days=1)))
            if recent_posts:
                return False
        return valid

    class Meta:
        model = OrderReview
        fields = ('content', 'order', 'reviewer')
        widgets = {
            'order': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class UserOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'due_back', )
        widgets = {'due_back': DateInput()}


class UserOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('car', 'due_back', )
        widgets = {'due_back': DateInput(), 'car':forms.HiddenInput()}