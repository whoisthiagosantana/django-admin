import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Brand, Category, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'brand', 'category')
    search_fields = ('name', 'brand__name', 'category__name')

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nome', 'Marca', 'Categoria', 'Ativo', 'Preço', 'Descrição', 'Criado em', 'Atualizado em'])

        for product in queryset:
            writer.writerow([product.name, product.brand.name, product.category.name, product.is_active, product.price, product.description, product.created_at, product.updated_at])

        return response
    
    export_to_csv.short_description = 'Exportar para CSV'
    actions = ['export_to_csv']