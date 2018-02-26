from django.contrib import admin

from .models import Company, Product, Profile, Stock, ProductType, ProductVariant, ProductAttribute, StockLocation, ProductImage


# Register your models here.
admin.site.register(ProductImage)
admin.site.register(Stock)
admin.site.register(StockLocation)
admin.site.register(ProductType)
admin.site.register(ProductVariant)
admin.site. register(ProductAttribute)

class CompanyAdmin(admin.ModelAdmin): 
    #sets up values for how admin site lists categories
    list_display = ('name', 'slug')
    list_display_links = ('name',)
    list_per_page = 20
    list_filter = ['name', 'location']
    ordering = ['name']
    search_fields = ['name', 'description']  

    # sets up slug to be generated from category name
    prepopulated_fields = {'slug' : ('name',)} 

admin.site.register(Company, CompanyAdmin)



class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'price', 'available_on', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ['available_on', 'updated_at', 'company']
    list_per_page = 50
    ordering = ['-price'] 
    search_fields = ['name']
   

admin.site.register(Product, ProductAdmin)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('birth_date', 'gender', 'bio')
    ordering = ['gender']
   