#Created on Thu Nov 23 23:40:27 2017

#TO DO
#temperature proxy
#US Oil enventory levels
#Natural gas prices
#central bank intervetions (RED has AUD up to 2006)



import pandas as pd
import numpy as np
from datetime import datetime
from datetime import  date
from scipy import interpolate 
from scipy.interpolate import UnivariateSpline
from sklearn.preprocessing import MinMaxScaler
from collections import OrderedDict

import wget                  #pip install wget
from fredapi import Fred     #pip install fredapi
import eiagov                #eiagov.py file
import quandl                # pip install quandl  
import holidays              #pip install holidays
           

DO_DOWNLOAD = False
        
codes = {  'AU_FX'    :'DEXUSAL'
          ,'CA_FX'    :'DEXCAUS'
          ,'CH_FX'    :'DEXSZUS'          
          ,'EU_FX'    :'DEXUSEU'
          ,'JP_FX'    :'DEXJPUS'
          ,'UK_FX'    :'DEXUSUK'

          ,'AU_INT_TB'    : 'INTGSTAUM193N'
          ,'CA_INT_TB'    : 'INTGSTCAM193N'
          ,'CH_INT_TB'    : 'IRLTLT01CHM156N' # 10 Year
          ,'JP_INT_TB'    : 'INTGSTJPM193N'
          ,'UK_INT_TB'    : 'INTGSTGBM193N'
          ,'US_INT_TB'    : 'TB3MS' #3month
          #EURO    
          ,'DE_INT_TB':'INTGSTDEM193N'
          ,'FR_INT_TB':'INTGSTFRM193N'  
          
          ,'AU_INT_ON':'IRSTCI01AUM156N' #overnight interbank interest rates
          ,'CA_INT_ON':'IRSTCI01CAQ156N'
          ,'JP_INT_ON':'IRSTCI01JPM156N'    
          ,'US_INT_ON':'IRSTCI01USM156N'
          ,'UK_INT_ON':'IRSTCI01GBQ156N'
          
          ,'US_INT_MORTGAGE':'MORTGAGE5US'

          ,'GOLD'     :'GOLDAMGBD228NLBM'
          ,'OIL_US'   :'DCOILWTICO'
          ,'Aluminium':'PALUMUSDM'
          ,'Copper'   :'PCOPPUSDM'
          ,'wood'     :'WPU0911'
          ,'Wheat'    :'PWHEAMTUSDM'
          ,'Tia_Rice' :'PRICENPQUSDM'
          ,'Beef'     :'PBEEFUSDQ'
 
         ,'AU_GDP': 'NAEXKP01AUQ657S' #Growth Rate Previous Period, Seasonally Adjusted
         ,'CA_GDP': 'NAEXKP01CAQ657S' 
         ,'CH_GDP': 'NAEXKP01CHQ657S' 
         ,'EU_GDP': 'NAEXKP01EUQ657S'
         ,'JP_GDP': 'NAEXKP01JPQ657S' 
         ,'UK_GDP': 'NAEXKP01GBQ657S' 
         ,'US_GDP': 'NAEXKP01USQ657S' 

         
         ,'AU_CPI': 'CPALTT01AUQ659N' #Growth Rate Same Period Previous Year, 
         ,'CA_CPI': 'CPALTT01CAM659N' #Not Seasonally Adjusted, Monthly
         ,'CH_CPI': 'CPALTT01CHM659N'
         ,'EU_CPI': 'CPHPTT01EZM659N'
         ,'JP_CPI': 'CPALTT01JPM659N'
         ,'UK_CPI': 'CPALTT01GBM659N'
         ,'US_CPI': 'CPALTT01USM659N'
         
         ,'AU_UR'    :'LRUNTTTTAUQ156N' #Unemployment Rate: Aged 15 and Over: All Persons   
         ,'CA_UR'    :'LRUNTTTTCAQ156N'
         ,'EU_UR'    :'LRHUTTTTEZM156N'
         ,'CH_UR'    :'LMUNRRTTCHQ156S'          
         ,'JP_UR'    :'LRUN64TTJPM156S'
         ,'UK_UR'    :'LMUNRRTTGBM156S'  
         ,'US_UR'    :'UNRATE'    
         
         ,'AU_DEBT'  :'DEBTTLAUA188A' #Gov debt as a % of GDP, Not Seasonally Adjusted
         ,'CA_DEBT'  :'DEBTTLCAA188A' 
         ,'CH_DEBT'  :'DEBTTLCHA188A' 
         ,'JP_DEBT'  :'GGGDTAJPA188N'
         ,'EU_DEBT'  :'GCDODTOTLGDZSEMU' 
         ,'UK_DEBT'  :'DEBTTLGBA188A'
         ,'US_DEBT'  :'DEBTTLUSA188A'
         
         ,'AU_POP'   : 'SPPOPGROWAUS'
         ,'CA_POP'   : 'SPPOPGROWCAN'
         ,'CH_POP'   : 'SPPOPGROWCHE'
         ,'EU_POP'   : 'SPPOPGROWEMU'
         ,'JP_POP'   : 'SPPOPGROWJPN'
         ,'UK_POP'   : 'SPPOPGROWGBR'         
         ,'US_POP'   : 'SPPOPGROWUSA' #Population growth year on year % change
         

         
         ,'US2_DEFICIT'             : 'FGLBFAQ027S' #(Quarterly), Millions of Dollars, Seasonally Adjusted Annual Rate
         ,'US2_Trade_Weighted_Index': 'DTWEXM' #Trade Weighted U.S. Dollar Index: Major Currencies (DTWEXM)
         ,'US2_HOUSING_DEFAULTS'    : 'DRSFRMACBS' 
         ,'US2_CARD_DEFAULTS'       : 'DRCCLACBS'  
         ,'CA_LOANS_DEFAULT'        : 'DDSI02CAA156NWDB' #annual
         
         ,'GAS_SPOT'                : 'MHHNGSP'     #monthly from 2000-01-01, not seasonaly adjusted
         ,'US2_GAS_USE'             : 'NATURALGAS'  
         ,'EU_GAS_SPOT'             : 'PNGASEUUSDM' # U.S. Dollars per Million Metric British Thermal Unit, Not Seasonally Adjusted
         ,'JP_BANK_Intervention'    : 'JPINTDUSDJPY'         
         ,'AU_COAL'                 : 'PCOALAUUSDM' # USD, monthluy, global price of coal australia
       } 



eia_ids = {
         'OIL_FUT_1M' : 'PET.RCLC1.D'
        ,'OIL_FUT_2M' : 'PET.RCLC2.D'
        ,'OIL_FUT_3M' : 'PET.RCLC2.D'
        ,'OIL_FUT_4M' : 'PET.RCLC4.D'
        #,'US2_POWER'  : 'ELEC.GEN.ALL-US-99.M' #montly should divide by number of days in the month
        }

quandl_ids = {
         'GOLD_FUT'    : ['CHRIS/CME_GC1'   ,'Settle']
        ,'OIL_CA_PROD' : ['BP/OIL_PROD_CAN' ,'Value']
        #,'CA_INT_INTERBANK' : ['BOC/V121785',1]
        ,'CA_FX_FUT_1M'   : ['SCF/CME_CD1_FW','Settle'] 
        ,'CA_FX_FUT_2M'   : ['SCF/CME_CD2_FN','Settle']
        
        #,'US_OILvsGAS'     : ['BP/GAS_PRICES','Value']
        ,'GAS_FUT_1M'   : ['CHRIS/CME_NG1', 'Settle']
        
        }


manual_files = {
         #'CA_HOUSING_DEFAULT': 'CA_HOUSING_DEFAULT' #https://cba.ca/mortgages-in-arrears
         #,'JP_GDP_WORLD_BANK' : 'JP_GDP_WORLD_BANK'  #world bank 
        }
#price of a big mac in local CCY paired with FXconversion column
bigmac_ccy = { 'US_BMP': ['United States', 'US_BMP'] # data available from > 2000
             ,'AU_BMP':  ['Australia'    , 'AU_FX'] 
             ,'CA_BMP':  ['Canada'       , 'CA_FX']
             ,'UK_BMP':  ['Britain'      , 'UK_FX']
             ,'CH_BMP':  ['Switzerland'  , 'CH_FX']
             ,'JP_BMP':  ['Japan'        , 'JP_FX']
             #,'DE_BMP':  ['Germany'      , 'EU_FX'] # data available from > 2011
             #,'FR_BMP':  ['France'       , 'EU_FX']
             #,'IR_BMP':  ['Ireland'      , 'EU_FX']
            }



#-------DOWNLOAD Data and Write to files ----------------------

def get_api_key(file_name):
    with open(file_name) as f:
        api_key = f.read()
        f.closed 
    return api_key;    
    

#Federal Reserve Bank of St. Louis (FRED)
# - get api key and initalize api
fred_api_key = get_api_key('./fred_api.key')    
fred = Fred(api_key=fred_api_key) 

#FRED download
if (DO_DOWNLOAD):
    for key, code in codes.items():
       print (key, code)
       data = fred.get_series(code)
       data.to_csv('./data/' + key + '.csv')



#US Energy Information Administration (EIA) 
# - get api key
eia_api_key = get_api_key('./eia_api.key')         
    
### Retrieve Data By Series ID ###
if (DO_DOWNLOAD):
    for key, code in eia_ids.items():
       print (key, code)
       data_pointer = eiagov.EIAgov(token=eia_api_key, series=[code]) 
       data = data_pointer.GetData()       
       data.to_csv('./data/' + key + '.csv', header=False, index=False)
      


#Quandl API connection
quandl_api_key = get_api_key('./quandl_api.key')  
quandl.ApiConfig.api_key = quandl_api_key

if (DO_DOWNLOAD):
    for key, code_field in quandl_ids.items():
        data = quandl.get(code_field[0])    
        data = data[[code_field[1]]] 
        data.to_csv('./data/' + key + '.csv', header=False, index=True)



# Purchasing Power Polarity data (aka the big mac index)
# get the histoprical prices of big macs by country in native currency
if (DO_DOWNLOAD):
    file_url = "http://infographics.economist.com/2017/databank/BMFile2000toJul2017.xls"
    xl_file = wget.download(file_url)  

    #All sheets as a dictionary of DataFrames: collections.OrderedDict
    sheets_dic = pd.read_excel(xl_file, sheet_name = None, usecols=[0,1], index_col = 0)
    for key, country in bigmac_ccy.items():
        country_name = str(country[0])
        local_price = None
        ls_date = []
        ls_price = []
        for sh_name, df in sheets_dic.items():
            #extract date from sheet name which is in format MmmYYYY
            sh_date = datetime.strptime(sh_name, '%b%Y').date()
            if country_name in df.index:
                local_price  = float(df.loc[country_name].values[0]) 
                ls_date.append(sh_date)
                ls_price.append(local_price)
            
            data = pd.DataFrame({'date_key': ls_date , 'local_price': ls_price})    
            data.to_csv('./data/' + key + '.csv', header=False, index=False)



#-------MERGE downloaded data file into a SINGLE FILE----------

#Create date sequence
date_current = date.today()
date_start  =  date(1999, 1, 1) #launch date of the Euro 4 jan 1999
periods = date_current - date_start
periods = periods.days
date_key = pd.date_range(date_start, periods=periods, freq='D')
date_index = pd.DatetimeIndex(date_key)

data = pd.DataFrame({   'date_key': date_key 
                      , 'date_qtr': date_index.quarter
                      , 'date_month': date_index.month
                      , 'date_dayofyear': date_index.dayofyear                       
                     }
                    )

#mark workdays vs weekend and public holiday
is_work_day = lambda day, cal : ((day.weekday() < 6) and (not day in cal)) * 1
data['AU_IS_WORK_DAY'] = data['date_key'].apply(is_work_day, args=(holidays.Australia(),))
data['US_IS_WORK_DAY'] = data['date_key'].apply(is_work_day, args=(holidays.UnitedStates(),))
data['CA_IS_WORK_DAY'] = data['date_key'].apply(is_work_day, args=(holidays.Canada(),))
data['UK_IS_WORK_DAY'] = data['date_key'].apply(is_work_day, args=(holidays.UnitedKingdom(),))

#Flag dates after 1 jan 1999 when ERO was introduced
data['IS_EURO'] =  (data['date_key'] >= pd.Timestamp(1999, 1, 1)) * 1


    
#append source columns
date_start_2 = pd.Timestamp(1999, 1, 1)
for key, code in {**codes, **eia_ids, **quandl_ids, **bigmac_ccy}.items(): 
#for key, code in {**quandl_ids}.items():     
    src_file =  './data/' + key + '.csv'
    src_df = pd.read_csv(src_file, header=None, names = ['date_key', key], parse_dates=['date_key'])
    src_df = src_df[src_df['date_key'] >= date_start_2]
    
    src_df[key] = src_df[key].interpolate(method = 'linear', limit=None)
    data = pd.merge(left = data, right = src_df, how ='left', left_on = 'date_key', right_on = 'date_key' ) 
    data[key] = data[key].interpolate(method = 'linear', limit=None)   
    print(src_df['date_key'].min(skipna=True), ',', key)
    #if key == 'GOLD_FUT' :
    #    print (src_df.head(10))
    #    print (data[['date_key', key]].head(370))


#take the inverse of USD/CAD to get CAD/USD
data.CA_FX = 1/data.CA_FX
data.JP_FX = 1/data.JP_FX



#Australia floated its currency on 12 December 1983. It was fixed before that date


def get_start_row_index(data, col_names):
   return(max([data[col].isnull().idxmin() for col in col_names]))


#adds a delta column data.new_col =  col1 - col2
def add_delta(data, new_col, col1, col2):
    data[new_col] = 0    
    row = get_start_row_index(data, [col1,col2]) 
    data.loc[row:,new_col] = data[col1].loc[row:] - data[col2].loc[row:]
    return data;
   
#Calculate delta between Spot and Futures prices
data = add_delta(data, new_col='oil_delta', col1='OIL_FUT_1M', col2='OIL_US')
data = add_delta(data, new_col='gold_delta', col1='GOLD_FUT', col2='GOLD')
data = add_delta(data, new_col='ca_fx_delta', col1='CA_FX_FUT_2M', col2='CA_FX')
#data = add_delta(data, new_col='US2_CA_HOUSING_DEFAULT_DIFF', col1='US2_HOUSING_DEFAULTS', col2='CA_HOUSING_DEFAULT')
data = add_delta(data, new_col='gas_delta', col1='GAS_FUT_1M', col2='GAS_SPOT')


def moving_avg(data, source_col, windows=[2,7,14,30,60,90,180,365]):
    source_col_val = data[source_col]    
    for window in windows :
        new_col_name       = source_col + '_MA_' + str(window).zfill(3)

        new_col_values     = source_col_val.rolling(window=window,center=False).mean()
        data[new_col_name] = new_col_values
    return data;    

data = moving_avg(data, 'AU_FX')
data = moving_avg(data, 'CA_FX')
data = moving_avg(data, 'CH_FX')
data = moving_avg(data, 'EU_FX')
data = moving_avg(data, 'JP_FX')
data = moving_avg(data, 'UK_FX')


#----add scaled daily temperature cycle (northern hemisphere)--------
#load 1 year of celcius for example town in North Eastern US
src_file =  './data/temperature.csv'
src_df = pd.read_csv(src_file, header=None, names = ['date_key', 'temp'], parse_dates=[0])

#fit a spline to the original celcius data
days = np.array(range(1,366))
temperature_annual = src_df.temp.values.reshape(-1, 1)
spl = UnivariateSpline(days,temperature_annual, k=3)
temperature_annual = spl(temperature_annual)

#scale between -1 and 1
min_max_scaler = MinMaxScaler(feature_range=(-1, 1), copy=True)
temperature_annual = min_max_scaler.fit_transform(temperature_annual)

temperature = pd.DataFrame({  'date_dayofyear': days
                             ,'temperature'   : temperature_annual.flatten('F')
                           })
#Join to main dataset
data = pd.merge(left = data, right = temperature, how ='left', left_on = 'date_dayofyear', right_on = 'date_dayofyear' ) 

#fill 1 day for leap years
data.temperature =  data.temperature.interpolate()

#----finish temp--------



#big mac ratio = (local_price * fx_rate) / us_price
def add_bigmac_ratio(data, new_col, col_loc, col_fx, col_us = 'US_BMP'):
    data[new_col] = 0    
    row = get_start_row_index(data, [col_loc,col_fx, col_us]) 
    data.loc[row:,new_col] = data[col_loc].loc[row:] * data[col_fx].loc[row:] / data[col_us].loc[row:]
    
    #drop the local_price column
    data = data.drop(columns = col_loc)
    
    return data;

# convert Big mac prices from local ccy to ratio against US Price
for local_price_col, fx_rate_src in bigmac_ccy.items():
    
    #back fill for first quarter fo 2000    
    data[local_price_col] =  data[local_price_col].fillna(method='bfill')
    
    if (local_price_col != 'US_BMP'):
        data = add_bigmac_ratio(  data
                                , new_col = local_price_col + '_Ratio'
                                , col_loc = local_price_col
                                , col_fx  = fx_rate_src[1]
                                , col_us  = 'US_BMP')




#--------- Export final combined dataset

date_start_2 = pd.Timestamp(2000, 1, 3)
data = data[data['date_key'] >= date_start_2]
data = data.reset_index(drop = True)
data['time_index'] = data.index.values
data.to_csv('./source_data.csv', index = False)  




    



#NOTES

#difference between 3M futures contracts and today's spot price 
#data['oil_delta'] = 0    
#row = get_start_row_index(data, ['OIL_FUT_1M','OIL_US']) 
#data.loc[row:,'oil_delta'] = data[row:].OIL_FUT_1M - data[row:].OIL_US



#https://pypi.python.org/pypi/ckan-api-client/0.1-beta5
#pip install ckan-api-client
#from ckan_api_client.high_level import CkanHighlevelClient
#from ckan_api_client.objects import CkanDataset
#client = CkanHighlevelClient('http://127.0.0.1:5000', api_key='e70c15cc-2f07-4845-8c6e-3607df88e905')
#client.get_dataset('dfe41b34-5114-47be-8d94-759f942938fc')


#openex_api_key = 'f935b5c0658349008d1186b1701f0469'
#from openexchangerates import OpenExchangeRatesClient
#client = OpenExchangeRatesClient(openex_api_key)
#client.latest()
#client.time_series(app_id= openex_api_key, start=, end = yyyy-mm-dd, symbols='CAD,AUD')


#pip install openexchangerates



#Intividual CAD futhers contracts
#https://www.quandl.com/collections/futures/cme-canadian-dollar-futures
#https://www.barchart.com/futures/quotes/D6*0/all-futures?timeFrame=daily
#code to merge individual contracts into a Continuous stream
#https://www.quantstart.com/articles/Continuous-Futures-Contracts-for-Backtesting-Purposes 


#Suicide attack database:
#http://cpostdata.uchicago.edu/search_new.php


#src_df[key] = src_df[key].fillna(method = 'pad')


#plt.plot(months, spl(temperature_annual));




########### Python 3.2 #############
#Climate Data
#import http.client, urllib.request, urllib.parse, urllib.error, base64
#
#headers = {
#    # Request headers
#    'Ocp-Apim-Subscription-Key': '{subscription key}',
#}
#
#params = urllib.parse.urlencode({
#    # Request parameters
#    'locationtype': '{string}',
#    'location': '{string}',
#    'cultureInfo': '{string}',
#})
#
#try:
#    conn = http.client.HTTPSConnection('earthnetworks.azure-api.net')
#    conn.request("GET", "/getLocations/data/locations/v2/location?searchString={searchString}&%s" % params, "{body}", headers)
#    response = conn.getresponse()
#    data = response.read()
#    print(data)
#    conn.close()
#except Exception as e:
#    print("[Errno {0}] {1}".format(e.errno, e.strerror))
####################################

#cut_date = pd.Timestamp(1994,1,1)
#data['JP_MERGE'] = pd.concat([ data[data.date_key >= cut_date].JP_GDP
#                              ,data[data.date_key < cut_date].JP_GDP_WORLD_BANK
#                             ])
