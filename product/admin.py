from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product,Category,CarouselOffer,HomePageOffer,HomePageCarouselOffer


admin.site.site_header = 'ShopStar'
admin.site.site_title = 'ShopStar'
admin.site.index_title = 'ShopStar.com'


class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","image_tag","product_name","price","total_quantity","cr_date"]
    search_fields = ["id","product_name","price",'cr_date']
    list_filter = ["product_name","price","cr_date"]
    list_display_links = list_display
    readonly_fields = ['image_tag',] 
    
admin.site.register(Product,ProductAdmin)

class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","category_name"]
    search_fields = ["id","category_name"]
    list_filter = ["category_name"]
    list_display_links = list_display
    
admin.site.register(Category,CategoryAdmin)

class CarouselOfferAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","carousel_product"]
    search_fields = ["id","carousel_product__product_name"]
    list_filter = ["carousel_product"]
    autocomplete_fields = ["carousel_product"]
    list_display_links = list_display
    
admin.site.register(CarouselOffer,CarouselOfferAdmin)

class HomePageOfferAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","product_offer"]
    search_fields = ["id","product_offer__category_name"]
    list_filter = ["product_offer"]
    autocomplete_fields = ["product_offer"]
    list_display_links = list_display
    
admin.site.register(HomePageOffer,HomePageOfferAdmin)


class HomePageCarouselOfferAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ["id","other_offer"]
    search_fields = ["id","other_offer__category_name"]
    list_filter = ["other_offer"]
    autocomplete_fields = ["other_offer"]
    list_display_links = list_display
    
admin.site.register(HomePageCarouselOffer,HomePageCarouselOfferAdmin)