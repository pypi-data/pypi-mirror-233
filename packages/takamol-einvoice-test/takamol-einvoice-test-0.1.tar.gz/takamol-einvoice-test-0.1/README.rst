=======================
Takamol E-invoice Test
=======================

This package is an implementation for e-invoices that comply with ZATCA regulations.

Quick start
-----------

1. Add "takamol-einvoice" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'takamol-einvoice-test',
    ]

2. Include the takamol_einvoice URLconf in your project urls.py like this::
url(r'^takamol_einvoice/', include('takamol_einvoice.urls')),

3. Run `python manage.py migrate` to create the invoices models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
