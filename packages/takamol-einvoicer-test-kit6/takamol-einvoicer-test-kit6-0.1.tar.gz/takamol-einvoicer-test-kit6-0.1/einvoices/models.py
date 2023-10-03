import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from simple_history.models import HistoricalRecords

from einvoices.constants import SELLER_INFO


class Invoice(models.Model):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    TAX = 'TAX'
    STANDARD = 'STANDARD'
    SIMPLIFIED = 'SIMPLIFIED'

    TYPE_CHOICES = [
        (DEBIT, 'Debit',),
        (CREDIT, 'Credit',),
        (TAX, 'Tax',),
    ]
    MODEL_NAME_CHOICES = [
        (STANDARD, 'Standard'),
        (SIMPLIFIED, 'Simplified')
    ]

    REPORTED = 'REPORTED'
    NOT_REPORTED = 'NOT_REPORTED'

    ZATCA_RESPONSE_CHOICES = [
        (REPORTED, 'Reported',),
        (NOT_REPORTED, 'Not Reported',)
    ]
    PREFIX_SERIAL = {
        STANDARD: '01',
        SIMPLIFIED: '02',
        TAX: 'INV',
        CREDIT: 'CRE',
        DEBIT: 'DEB',
    }
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=10, choices=MODEL_NAME_CHOICES)
    parent_id = models.UUIDField(null=True, blank=True, db_index=True)  # mandatory when type is credit or debit
    note = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    tax_number = models.CharField(default=SELLER_INFO["company_ID"], max_length=15, blank=True,
                                  null=True)  # company tax number
    serial_number = models.CharField(max_length=20, unique=True, blank=True, null=True, )
    seller_name = models.CharField(default=SELLER_INFO["registration_name"], max_length=100, blank=True, null=True)
    total_excluding_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_including_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # TODO remove: Should we keep this field? It’s important to consider that the data will be returned as JSON,
    #  which means that the user might want to store it in a different location along with the logo and other.
    #  information the above might be changed according to generating PDF/a-3b per ZATCA regulation
    template_name = models.CharField(max_length=120, blank=True, null=True, )
    has_warnings = models.BooleanField(default=False, blank=True, null=True)
    encoded_invoice = models.TextField(blank=True, null=True, max_length=55000)
    zatca_status = models.CharField(max_length=25, choices=ZATCA_RESPONSE_CHOICES, blank=True, null=True)
    hash_key = models.CharField(max_length=250, blank=True, null=True, )
    icv = models.IntegerField(null=True, blank=True, db_index=True)
    qr_code = models.CharField(max_length=700, blank=True, null=True, )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    buyer = GenericForeignKey('content_type', 'object_id')
    # this is specified to Standard model
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords(table_name='invoice_history')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "takamol_einvoice.invoices"

    def save(self, *args, **kwargs):

        if not self.serial_number:
            num_obj = Invoice.objects.filter(model_name=self.model_name).count()
            self.serial_number = f"{self.PREFIX_SERIAL[self.type]}-{self.PREFIX_SERIAL[self.model_name]}-{str(num_obj + 1).zfill(4)}"
        super().save(*args, **kwargs)

    @property
    def get_phk(self):
        latest_invoice = Invoice.objects.latest('created_at')

        # Get the Invoice objects that were created before the latest one
        previous_invoices = Invoice.objects.filter(created_at__lt=latest_invoice.created_at)

        # Get the previous Invoice object
        if previous_invoices.exists():
            previous_invoice = previous_invoices.latest('created_at')
            hash_key = previous_invoice.hash_key
        else:
            # if this is the first invoice we will return 0 after hash it using SHA-256
            hash_key = 'NWZlY2ViNjZmZmM4NmYzOGQ5NTI3ODZjNmQ2OTZjNzljMmRiYzIzOWRkNGU5MWI0NjcyOWQ3M2EyN2ZiNTdlOQ=='
        return hash_key

    @property
    def get_previous_icv(self):
        obj = Invoice.objects.exclude(zatca_status__isnull=True).order_by('-created_at').first()
        return obj.icv if obj else 0

    @property
    def get_parent_id_invoice_number(self):
        try:
            obj = Invoice.objects.get(id=self.parent_id)
            return obj.serial_number
        except Invoice.DoesNotExist:
            return None

    @property
    def items(self):
        return Item.objects.filter(invoice_object_id=self.pk,
                                   invoice_content_type=ContentType.objects.get_for_model(self))


class Item(models.Model):
    """
           This model to be linked with each issued invoice to represent all the items paid
           For each invoice there will be many items

           quantity: it will be always 1 for now
           content_type, object_id, content_object: to link the service / product (Course, ..) paid for
           invoice_content_type, invoice_object_id, invoice: to link the invoice (standard, simplified) with their items

       """
    description_en = models.CharField(max_length=100, blank=True, null=True)
    description_ar = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=10, blank=False, null=False)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    vat_rate = models.DecimalField(default=0.15, max_digits=10, decimal_places=2, blank=True,
                                   null=False)  # now it is a 15%, but it might change in the future
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal_excluding_vat = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=False)
    subtotal_including_vat = models.DecimalField(max_digits=20, decimal_places=10, blank=True, null=False)
    product_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product_object_id = models.UUIDField()
    product = GenericForeignKey('product_content_type', 'product_object_id')
    invoice_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='takamol_einvoice_items')
    invoice_object_id = models.UUIDField()
    invoice = GenericForeignKey('invoice_content_type', 'invoice_object_id')
    history = HistoricalRecords(table_name='items_history')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'takamol_einvoice.items'

    def save(self, *args, **kwargs):
        """
        modify the save function to calculate the vat amount, subtotal_excluding_vat and subtotal_including_vat
        dynamically
        """
        if not self.vat_amount:
            self.vat_amount = self.quantity * self.unit_price * self.vat_rate

        if not self.subtotal_excluding_vat:
            self.subtotal_excluding_vat = self.quantity * self.unit_price

        if not self.subtotal_including_vat:
            self.subtotal_including_vat = self.quantity * self.unit_price + self.vat_amount

        super(Item, self).save(*args, **kwargs)

        # Calculate the totals for the related Invoice
        invoice = self.invoice
        items = invoice.items.all()

        invoice.total_excluding_vat = round(sum(item.subtotal_excluding_vat for item in items), 2)
        invoice.total_including_vat = round(sum(item.subtotal_including_vat for item in items), 2)
        invoice.vat_amount = round(sum(item.vat_amount for item in items), 2)

        invoice.save()
