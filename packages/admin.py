from django.contrib import admin

from packages.models import DemoPackage, Package, PackageSelfManagement

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageSelfManagement)
admin.site.register(DemoPackage)
