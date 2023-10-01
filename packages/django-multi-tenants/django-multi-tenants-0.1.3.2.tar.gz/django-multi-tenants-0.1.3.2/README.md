# django-multi-tenant

This project is based on [django-tenant-schemas.readthedocs.io](https://django-tenant-schemas.readthedocs.io/en/latest/). All our thanks to its creators.

This is a customisation we need in order to have details of the tenants' applications.

There are three variables that we need to declare in the **settings.py** file to describe the application schema:
- `SHARED_APPS` describe the applications whose migration is carried out in the public scheme.
- `TENANT_APPS` describe the applications whose migration is carried out in the main tenant scheme.
- `TENANT_DETAIL_APPS` describe the applications whose migration is carried out in the detailed
tenant scheme. The detailed tenant scheme is associated with a single main tenant.
For example, if you want to separate information between years, such as accounting software.
