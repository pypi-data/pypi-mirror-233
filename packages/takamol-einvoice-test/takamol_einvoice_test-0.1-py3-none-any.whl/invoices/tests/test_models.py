from django.contrib.auth.models import User
from django.test import TestCase

from takamol_einvoice.invoices.models import Invoice
from takamol_einvoice.invoices.services.invoice_service import InvoiceService


class InvoiceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.buyer = User.objects.create(username='username', password='password', email='email@example.com')

        # Create some items for the invoice
        cls.items_data = [
            {
                "description_en": "Item 1 des",
                "unit_price": 10.00,
                "quantity": 2,
                # Please inform that we don't sell people as products, but this is only for experiment purposes
                # This isn't Dexter's laboratory :))
                "product": cls.buyer
            },
            {
                "description_en": "Item 2 des",
                "unit_price": 5.00,
                "quantity": 3,
                "product": cls.buyer

            },
        ]
        cls.invoice_data = {
            "type": Invoice.TAX,
            "template_name": 'MyTemplate',
            "buyer": cls.buyer
        }

        cls.standard_invoice = InvoiceService.generate_invoice(Invoice.STANDARD, cls.items_data, cls.invoice_data)

    def test_create_invoice(self):
        invoice = InvoiceService.generate_invoice(Invoice.SIMPLIFIED, self.items_data, self.invoice_data)

        self.assertIsInstance(invoice, Invoice)
        self.assertEqual(invoice.items.count(), len(self.items_data))

        for item, item_data in zip(invoice.items.all(), self.items_data):
            self.assertEqual(item.invoice, invoice)
            for key, value in item_data.items():
                if isinstance(value, float):
                    self.assertAlmostEqual(float(getattr(item, key)), value)
                else:
                    self.assertEqual(getattr(item, key), value)
        invoice.delete()

    def test_invoice_total_excluding_vat(self):
        standard_invoice = Invoice.objects.get(pk=self.standard_invoice.pk)

        expected_total_excluding_vat = sum(item.unit_price * item.quantity for item in standard_invoice.items.all())

        self.assertAlmostEqual(standard_invoice.total_excluding_vat, expected_total_excluding_vat, places=2)

    def test_serial_number_auto_created(self):
        self.assertIsNotNone(self.standard_invoice.serial_number)
        self.assertIsInstance(self.standard_invoice.serial_number, str)

    def test_serial_number_generation(self):
        num_obj = Invoice.objects.filter(model_name=Invoice.STANDARD).count()

        expected_serial_number = f"{Invoice.PREFIX_SERIAL[self.standard_invoice.type]}-{Invoice.PREFIX_SERIAL[self.standard_invoice.model_name]}-{str(num_obj).zfill(4)}"
        self.assertEqual(self.standard_invoice.serial_number, expected_serial_number)


class ItemModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.unit_price = 100
        cls.quantity = 2
        cls.vat_rate = 0.15

        cls.buyer = User.objects.create(username='username', password='password', email='email@example.com')
        cls.items_data = [
            {
                "description_en": 'Item 1',
                "description_ar": 'بند 1',
                'product': cls.buyer,
                "unit_price": cls.unit_price,
                "quantity": cls.quantity,
                "vat_rate": cls.vat_rate,
            }
        ]
        cls.invoice_data = {
            "type": Invoice.TAX,
            "template_name": 'MyTemplate',
            "buyer": cls.buyer
        }

        cls.standard_invoice = InvoiceService.generate_invoice(Invoice.STANDARD, cls.items_data, cls.invoice_data)

    def test_calculate_vat_amount(self):
        expected_vat_amount = self.unit_price * self.quantity * self.vat_rate

        item = self.standard_invoice.items.first()

        self.assertEqual(item.vat_amount, expected_vat_amount)

    def test_calculate_subtotals(self):
        expected_subtotal_excluding_vat = self.unit_price * self.quantity
        expected_subtotal_including_vat = expected_subtotal_excluding_vat + (
                self.unit_price * self.quantity * self.vat_rate)

        item = self.standard_invoice.items.first()

        self.assertEqual(item.subtotal_excluding_vat, expected_subtotal_excluding_vat)
        self.assertEqual(item.subtotal_including_vat, expected_subtotal_including_vat)
