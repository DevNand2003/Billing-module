from django.shortcuts import render, get_object_or_404 , redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Invoice
from .forms import InvoiceForm
from django.contrib import messages

def invoice_form(request):
    form = InvoiceForm()
    invoices = Invoice.objects.all().order_by('-invoice_number')
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', invoice_id=invoice.invoice_number)  # Redirect instead of render
    
    return render(request, 'billing/invoice_form.html', {'form': form, 'invoices': invoices})


def invoice_detail(request, invoice_id):
    invoice = Invoice.objects.get(invoice_number=invoice_id)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})


def search_invoice(request):
    invoice_number = request.GET.get('invoice_number')
    invoice = get_object_or_404(Invoice, invoice_number=invoice_number)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})

def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    subject = f"Invoice {invoice.invoice_number} from Gaurdian Warehouse"
    message = f"""
    Company         : {invoice.company}
    Rent per Day   : {invoice.rent_per_day}
    Start Date       : {invoice.start_date}
    End Date         : {invoice.end_date}
    Discount         : {invoice.discount}%
    GST                : {invoice.gst}%
    Total Amount : {invoice.total_amount()}
    """
    
    send_mail(subject, message, 'devnand2003@gmail.com', [invoice.email])
    return JsonResponse({'message': 'Invoice sent successfully!'})



from django.shortcuts import render, get_object_or_404
from .models import Invoice

def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    return render(request, 'billing/print_invoice.html', {'invoice': invoice})



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Invoice

def get_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    data = {
        'invoice_number': invoice.invoice_number,
        'company': invoice.company,
        'rent_per_day': str(invoice.rent_per_day),
        'start_date': str(invoice.start_date),
        'end_date': str(invoice.end_date),
        'discount': str(invoice.discount),
        'gst': str(invoice.gst),
        'due': str(invoice.due),
        'total_amount': invoice.total_amount()
    }
    return JsonResponse(data)
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, invoice_number=invoice_id)
    
    if request.method == "POST":  # Ensure it only works with POST requests
        invoice.delete()
        messages.success(request, "Invoice deleted successfully.")
        return redirect('invoice_form')  # Redirect to invoice list
    
    return redirect('invoice_detail', invoice_id=invoice_id)  # In case of GET request