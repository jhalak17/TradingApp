from django.shortcuts import render
from .models import FormModel
import json, os
import time
from datetime import datetime
import pandas as pd
from django.conf import settings

# Create your views here.
def upload_csv(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        try:
            start = time.time()
            print('start ---> ',start)
            timeframe = request.POST.get('close')


            csv_file = request.FILES['csv_file']
            instance = FormModel(csv_file = csv_file)
            instance.register()
           


            df = pd.read_csv(csv_file)


            df_1 = df.iloc[:int(timeframe),:]

            candle_list = []
            candle = {}

            candle['ID'] = df._get_value(0, 'BANKNIFTY')

            candle['OPEN'] = df._get_value(0, 'OPEN')
            high_list = df_1['HIGH'].to_list()

            candle['HIGH'] = max(high_list)
            low_list = df_1['LOW'].to_list()
            candle['LOW'] = min(low_list)

            candle['CLOSE'] = df._get_value(int(timeframe)-1, 'CLOSE')

          
            candle['DATE'] = int(df._get_value(int(timeframe)-1, 'DATE'))
            

            print(candle)
            candle_list.append(candle)
  
        except Exception as e:
            print("Exception",e)
            candle = f"Unable to uplaod file - {e}"

        with open("media/candledata.json", "w") as final:
            json.dump(candle_list, final)
        
        print("end ---> ",time.time()-start)

    return render(request,'csv_data.html',{'context':candle})
