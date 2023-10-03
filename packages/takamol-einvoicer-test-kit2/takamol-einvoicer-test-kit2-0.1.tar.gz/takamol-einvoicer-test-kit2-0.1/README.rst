==============================
Takamol E-invoicer Test Kit 2
==============================

This package is an implementation for e-invoices that comply with ZATCA regulations.

Quick start
-----------

1. Add "takamol-einvoicer-test-kit2" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'takamol-einvoicer-test-kit2',
    ]

2. Include the takamol_einvoicer_test_kit2 URLconf in your project urls.py like this::
url(r'^takamol_einvoicer_test_kit2/', include('takamol_einvoicer_test_kit2.urls')),

3. Run `python manage.py migrate` to create the invoices models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
