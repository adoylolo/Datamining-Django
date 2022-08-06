from django.shortcuts import render
from .models import data
from .resources import dataResource
import datetime as dt
import pandas as pd
import os
import json
import time
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import F
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

rules1 = pd.DataFrame({'A' : [1, 2, 3, 4],
                     'B' : [1,2,3,4]})
rules2 = pd.DataFrame({'A' : [1, 2, 3, 4],
                     'B' : [1,2,3,4]})

# Create your views here.
def index(request):#membuat fungsi untuk view.index
    #menampilkan data dari database sebanyak 5 data pertama
    datas = data.objects.all()[:5]

    context ={
        'Data':datas,
    }

    #membuat fungsi untuk upload data dengan import excel
    if request.method == 'POST' and 'submit_excel' in request.POST:
        data_resource = dataResource()
        dataset = Dataset()
        new_data = request.FILES['myfile']

        if not new_data.name.endswith('xlsx'):
            messages.info(request, 'salah format')
            return render(request, 'index.html')

        imported_data = dataset.load(new_data.read(),format='xlsx')
        for buah in imported_data:
            value = data(
                buah[0],
                buah[1],
                buah[2],
                buah[3],
                buah[4],
                buah[5],
                buah[6],
                buah[7],
                buah[8],
                buah[9],
                buah[10],
                buah[11],
                buah[12],
                buah[13],
                buah[14],
                buah[15],
                buah[16],
                buah[17],
                buah[18],
                buah[19],
                buah[20],
                buah[21],
                buah[22],
                buah[23],
                buah[24],
                buah[25],
                buah[26],
                buah[27],
                buah[28],
                buah[29]
                )
            value.save()

    #membuat fungsi untuk association rules dengan minimum support dan minimum confidence yang diinput manual oleh user
    if request.method == 'POST' and 'submit_rule' in request.POST:
        print(request.POST['minsup'])
        context['minsup'] = request.POST['minsup']
        minsupport = float(request.POST['minsup'])
        print(request.POST['minconf'])
        context['minconf'] = request.POST['minconf']
        minconfidence = float(request.POST['minconf'])

        data_buah = data.objects.all().values()
        df = pd.DataFrame(data_buah)
        produk = (df.set_index('invoice'))
        context['df'] = df.to_html()

        start1 = time.time()
        frequent_itemsets1 = apriori(produk, min_support = minsupport, use_colnames = True)
        global rules1
        rules1 = association_rules(frequent_itemsets1, metric = "confidence", min_threshold = minconfidence)
        rules1.drop(columns = "leverage", inplace = True)
        rules1.drop(columns = "conviction", inplace = True)
        rules1 = rules1[ (rules1['lift'] >= 1) ]
        rules1['kekuatan'] = rules1['support'] * rules1['confidence']
        jumlah_rules_apriori = len(rules1.index)
        kekuatan_asosiasi_apriori = sum(rules1['kekuatan']) / jumlah_rules_apriori
        json_records_apriori = rules1.reset_index().to_json(orient = 'records')
        AR_apriori = []
        AR_apriori = json.loads(json_records_apriori)
        context['rules_apriori'] = rules1.to_html()
        context['jumlah_rules_apriori'] = jumlah_rules_apriori
        context['kekuatan_aturan_apriori'] = kekuatan_asosiasi_apriori
        context['apriori'] = AR_apriori
        kecepatan_apriori = time.time() - start1
        context['kecepatan_apriori'] = round(kecepatan_apriori * 1000.0, 2)

        start2 = time.time()
        frequent_itemsets2 = fpgrowth(produk, min_support = minsupport, use_colnames = True)
        global rules2
        rules2 = association_rules(frequent_itemsets2, metric = "confidence", min_threshold = minconfidence)
        kecepatan_fpgrowth = time.time() - start2
        rules2.drop(columns = "leverage", inplace = True)
        rules2.drop(columns = "conviction", inplace = True)
        rules2 = rules2[ (rules2['lift'] >= 1) ]
        rules2['kekuatan'] = rules2['support'] * rules2['confidence']
        jumlah_rules_fpgrowth = len(rules2.index)
        kekuatan_asosiasi_fpgrowth = sum(rules2['kekuatan']) / jumlah_rules_fpgrowth
        json_records_fpgrowth = rules2.reset_index().to_json(orient = 'records')
        AR_fpgrowth = []
        AR_fpgrowth = json.loads(json_records_fpgrowth)
        context['rules_fpgrowth'] = rules2.to_html()
        context['jumlah_rules_fpgrowth'] = jumlah_rules_fpgrowth
        context['kekuatan_aturan_fpgrowth'] = kekuatan_asosiasi_fpgrowth
        context['fpgrowth'] = AR_fpgrowth
        context['kecepatan_fpgrowth'] = round(kecepatan_fpgrowth * 1000.0, 2)

        return render(request, 'result.html', context)

    #membuat fungsi untuk association rules dengan parameter tuning perulangan
    if request.method == 'POST' and 'parameter_tuning' in request.POST:
        minimal_rule = int(request.POST['min_rule'])
        min_sup_parameter = [0.6, 0.7, 0.8, 0.85, 0.9]
        min_conf_parameter = [0.6, 0.7, 0.8, 0.9, 1]
        max_support_parameter = 0
        max_confidence_parameter = 0
        max_rule_parameter = 0
        max_kekuatan_parameter = 0

        data_buah = data.objects.all().values()
        df = pd.DataFrame(data_buah)
        produk = (df.set_index('invoice'))
        context['df'] = df.to_html()

        for sup_parameter in min_sup_parameter:
            for conf_parameter in min_conf_parameter:
                frequent_itemsets_parameter = apriori(produk, min_support=sup_parameter, use_colnames=True) 
                rules_parameter = association_rules(frequent_itemsets_parameter, metric="confidence", min_threshold=conf_parameter)
                rules_parameter = rules_parameter[ (rules_parameter['lift'] >= 1) ]

                rules_parameter['kekuatan']=rules_parameter['support']*rules_parameter['confidence']
                jumlah_rule_parameter = len(rules_parameter.index)

                if (jumlah_rule_parameter == 0):
                    print("Tidak Terdapat Rekomendasi yang Terbentuk")
                    print("")
                elif (jumlah_rule_parameter > 0):
                    kekuatan_parameter = sum(rules_parameter['kekuatan'])/jumlah_rule_parameter
                    if (kekuatan_parameter >= max_kekuatan_parameter and jumlah_rule_parameter >= minimal_rule):
                        max_support_parameter = sup_parameter
                        max_confidence_parameter = conf_parameter
                        max_rule_parameter = jumlah_rule_parameter
                        max_kekuatan_parameter = kekuatan_parameter
                    else:
                        max_support_parameter = max_support_parameter
                        max_confidence_parameter = max_confidence_parameter
                        max_rule_parameter = max_rule_parameter
                        max_kekuatan_parameter = max_kekuatan_parameter

        start1 = time.time()
        frequent_itemsets1 = apriori(produk, min_support = max_support_parameter, use_colnames = True)
        rules1 = association_rules(frequent_itemsets1, metric = "confidence", min_threshold = max_confidence_parameter)
        rules1.drop(columns = "leverage", inplace = True)
        rules1.drop(columns = "conviction", inplace = True)
        rules1 = rules1[ (rules1['lift'] >= 1) ]
        rules1['kekuatan'] = rules1['support'] * rules1['confidence']
        jumlah_rules_apriori = len(rules1.index)
        kekuatan_asosiasi_apriori = sum(rules1['kekuatan']) / jumlah_rules_apriori
        json_records_apriori = rules1.reset_index().to_json(orient = 'records')
        AR_apriori = []
        AR_apriori = json.loads(json_records_apriori)
        context['rules_apriori'] = rules1.to_html()
        context['jumlah_rules_apriori'] = jumlah_rules_apriori
        context['kekuatan_aturan_apriori'] = kekuatan_asosiasi_apriori
        context['apriori'] = AR_apriori
        kecepatan_apriori = time.time() - start1
        context['kecepatan_apriori'] = round(kecepatan_apriori * 1000.0, 2)

        start2 = time.time()
        frequent_itemsets2 = fpgrowth(produk, min_support = max_support_parameter, use_colnames = True)
        rules2 = association_rules(frequent_itemsets2, metric = "confidence", min_threshold = max_confidence_parameter)
        kecepatan_fpgrowth = time.time() - start2
        rules2.drop(columns = "leverage", inplace = True)
        rules2.drop(columns = "conviction", inplace = True)
        rules2 = rules2[ (rules2['lift'] >= 1) ]
        rules2['kekuatan'] = rules2['support'] * rules2['confidence']
        jumlah_rules_fpgrowth = len(rules2.index)
        kekuatan_asosiasi_fpgrowth = sum(rules2['kekuatan']) / jumlah_rules_fpgrowth
        json_records_fpgrowth = rules2.reset_index().to_json(orient = 'records')
        AR_fpgrowth = []
        AR_fpgrowth = json.loads(json_records_fpgrowth)
        context['max_support_parameter'] = "Minimum Support yang Digunakan Adalah : ", max_support_parameter
        context['max_confidence_parameter'] = "Minimum Confidence yang Digunakan Adalah : ", max_confidence_parameter
        context['rules_fpgrowth'] = rules2.to_html()
        context['jumlah_rules_fpgrowth'] = jumlah_rules_fpgrowth
        context['kekuatan_aturan_fpgrowth'] = kekuatan_asosiasi_fpgrowth
        context['fpgrowth'] = AR_fpgrowth
        context['kecepatan_fpgrowth'] = round(kecepatan_fpgrowth * 1000.0, 2)

        return render(request, 'result.html', context)

    if request.method == 'POST' and 'submit_rekomendasi' in request.POST:
        jumlah_itemset_produk = int(request.POST['kombinasi_itemset'])

        rules1["jumlah itemset"] = rules1["antecedents"].apply(lambda x: len(x)) + rules1["consequents"].apply(lambda x: len(x))
        rules1 = rules1[rules1['jumlah itemset'] == jumlah_itemset_produk]
        context['rekomendasi_apriori'] = rules1.to_html()
        json_rekomendasi_apriori = rules1.reset_index().to_json(orient = 'records')
        Rec_apriori = []
        Rec_apriori = json.loads(json_rekomendasi_apriori)
        context['rec_apriori'] = Rec_apriori

        rules2["jumlah itemset"] = rules2["antecedents"].apply(lambda x: len(x)) + rules2["consequents"].apply(lambda x: len(x))
        rules2 = rules2[rules2['jumlah itemset'] == jumlah_itemset_produk]
        context['rekomendasi_fpgrowth'] = rules2.to_html()
        json_rekomendasi_fpgrowth = rules2.reset_index().to_json(orient = 'records')
        Rec_fpgrowth = []
        Rec_fpgrowth = json.loads(json_rekomendasi_fpgrowth)
        context['rec_fpgrowth'] = Rec_fpgrowth

        return render(request, 'result.html', context)

    return render(request, 'index.html', context)

def datatransaksi(request):#menampilkan semua data transaksi penjualan
    datas = data.objects.all()

    context ={
        'Data':datas,
    }

    #membuat fungsi untuk menghapus semua data transaksi penjualan
    if request.method == 'POST' and 'delete_data' in request.POST:
        deletes = data.objects.all().delete()
        context ={
            'Data':datas,
            'Delete':deletes,
        }
        return render(request, 'data.html', context)

    return render(request, 'data.html', context)

def result(request):#fungsi untuk berpindah ke view result
    return render(request, 'result.html')