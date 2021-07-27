from django.contrib import admin

from .models import Komen, Pertanyaan


class PertanyaanAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['pertanyaan_text']}),
    ]
    list_display = ('pertanyaan_text', 'pub_date', 'votes')
    list_filter = ['pub_date']
    search_fields = ['pertanyaan_text']

class KomenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['komen_text']}),
    ]
    list_display = ('komen_text', 'pub_date', 'votes')
    list_filter = ['pub_date']
    search_fields = ['komen_text']

admin.site.register(Pertanyaan, PertanyaanAdmin)

admin.site.register(Komen, KomenAdmin)
