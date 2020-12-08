from django.contrib import admin
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from .models import TempHumRecord

# Inheriting from Wagtail's ModelAdmin to consolidate functionality to Wagtail's Admin Site 
class TempHumRecordAdmin(ModelAdmin):
    model = TempHumRecord
    menu_label = "Temp/Hum Log"
    menu_icon = "list-ul"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('temp', 'humidity', 'date_time_logged')
    search_fields = ('date_time_logged')
    index_template_name = 'modeladmin/api/temphumrecord/index.html'
    index_view_extra_js = ('js/chart.js', 'js/utils.js')
    index_view_extra_css = ['css/modeladmin/skeleton.css']

modeladmin_register(TempHumRecordAdmin)