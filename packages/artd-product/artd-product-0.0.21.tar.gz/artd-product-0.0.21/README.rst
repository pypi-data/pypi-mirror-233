=================
Products
=================

A Django app to create products.


Quick start
-----------

1. Add "artd_product" to your INSTALLED_APPS setting like this:
    
        INSTALLED_APPS = [
            ...
            'artd_product',
        ]

2. Run ``python manage.py migrate`` to create the product models.

3. Run ``python manage.py create_taxes`` to create tax types.

4. Start the development server and visit http://127.0.0.1:8000/admin/