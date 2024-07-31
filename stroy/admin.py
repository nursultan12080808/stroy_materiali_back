from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *



class MateralAdminForm(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget(), label='Описание материала')

    class Meta:
        model = Material
        fields = '__all__'



class MaterialImageStackedInline(admin.TabularInline):

    model = Images
    extra = 1


@admin.register(Material)
class NftAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category', 'price', 'currency', 'get_image')
    list_display_links = ('id','name',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image')
    filter_horizontal = ('tags',)
    search_fields = ('name','tags', 'category')
    list_filter = ('category', 'created_at', 'updated_at')
    inlines = [MaterialImageStackedInline,]
    form = MateralAdminForm


    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.images.first():
            return mark_safe(f'<img src="{item.images.first().image.url}" width="100px">')
        return '-'
    
    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.images.first():
            return mark_safe(f'<img src="{item.images.first().image.url}" width="100%">')
        return '-'
    
    
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Tags)

# Register your models here.
