from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import data

# Register your models here.
@admin.register(data)#mendaftarkan model data ke dalam admin panel
class dataAdmin(ImportExportModelAdmin):
	list_display = ('invoice','almond','alpukat','anggur','apel',
		'asam_bangkok','avomango','blueberry_arg','buah_naga','buah_tin',
		'cherry_aus','chia_seed','delima','durian','grapeola','jambu_kristal',
		'jeruk','kiwi','kurma','lemon','lengkeng','mangga','melon_golden',
		'nanas_honi','nectarin_aus','peach_aus','pear','pisang','plum','salak_pondoh')