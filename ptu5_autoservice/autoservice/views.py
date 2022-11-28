from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Car, Order, Service, OrderLine
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormMixin
from . forms import OrderReviewForm, UserOrderForm, UserOrderUpdateForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

def index(request):
    # return HttpResponse("Welcome!")
    car_count = Car.objects.count()
    order_count = Order.objects.count()
    service_count = Service.objects.count(),
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count+1

    context = {
        'car_count': car_count,
        'order_count': order_count,
        'service_count': service_count,
        'visits_count': visits_count,
    }
    
    return render(request, 'autoservice/index.html', context=context)

def car_list_view(request):
    car_list = Car.objects.all()
    search = request.GET.get('search')
    if search:
        car_list = car_list.filter(
            Q(client__icontains=search) |
            Q(license_plate_number__icontains=search) |
            Q(car_model__make__icontains=search) |
            Q(car_model__model__icontains=search)
        )
    paginator = Paginator(car_list, 2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    return render(request, 'autoservice/car_list.html', {
        'car_list': paged_cars
    })

def car_detail_view(request, pk):
    return render(request, 'autoservice/car_detail.html', {
        'object': get_object_or_404(Car, pk=pk),
    })

class OrderListView(ListView):
    model = Order
    paginate_by = 2
    template_name = 'autoservice/order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            try:
                queryset = queryset.filter(id__exact=search)
            except ValueError:
                queryset = queryset.filter(
                    Q(car__client__icontains=search) |
                    Q(car__plate__icontains=search)
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_count'] = self.get_queryset().count()
        return context


class OrderDetailView(FormMixin, DetailView):
    model = Order
    template_name = 'autoservice/order_detail.html'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, _("You're posting too much!"))
            return self.form_invalid(form)

    def get_initial(self):
        return {
            'order': self.get_object(), 
            'reviewer': self.request.user
        }

    def form_valid(self, form):
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, _("Your review has been posted."))
        return super().form_valid(form)


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'autoservice/user_order_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user).order_by('due_back')
        return queryset


class UserNewOrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    # fields = ('car', 'due_back')
    form_class = UserOrderForm
    template_name = 'autoservice/user_order_form.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'n'
        return super().form_valid(form)

class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    # fields = ('car', 'due_back')
    form_class = UserOrderUpdateForm
    template_name = 'autoservice/user_order_form.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = 'n'
        messages.success(self.request, _("Order updated."))
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object().status == 'n':
            context['action'] = _('Update')
        else:
            context['action'] = _('Create')
        return context


class UserOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'autoservice/user_delete_order.html'
    success_url = reverse_lazy('user_orders')

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.owner

    def form_valid(self, form):
        messages.success(self.request, _("Order canceled."))
        return super().form_valid(form)     