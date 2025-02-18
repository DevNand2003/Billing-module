
from django.urls import path
from .views import invoice_form, search_invoice, send_invoice_email, get_invoice , invoice_detail ,delete_invoice

urlpatterns = [
    path('', invoice_form, name='invoice_form'),
    path('search/', search_invoice, name='search_invoice'),
    path('send_email/<int:invoice_id>/', send_invoice_email, name='send_invoice_email'),
    path('get_invoice/<int:invoice_id>/', get_invoice, name='get_invoice'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice_detail'),  # New route
    path('delete_invoice/<int:invoice_id>/', delete_invoice, name='delete_invoice'),
]
