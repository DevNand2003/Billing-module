from django.db import models

class Invoice(models.Model):
    invoice_number = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255)
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = models.EmailField()

    def total_amount(self):
        days = (self.end_date - self.start_date).days + 1
        base_amount = days * self.rent_per_day
        discount_amount = (base_amount * self.discount) / 100
        gst_amount = ((base_amount - discount_amount) * self.gst) / 100
        return round(base_amount - discount_amount + gst_amount, 2)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.company}"
