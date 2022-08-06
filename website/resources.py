from import_export import resources
from .models import data

class dataResource(resources.ModelResource):#membuat resource data transaksi penjualan
	class meta:
		model = data