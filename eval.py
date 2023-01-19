import os
base_path = r"C:\Users\viejo\Anaconda3"
path = os.pathsep.join([os.path.join(base_path, i) for i in [r"", r"bin", r"Scripts", r"Library\mingw-w64\bin", r"Library\bin"]])
os.environ["PATH"]+=os.pathsep+path
from math import sqrt
from pickletools import read_decimalnl_long
import pandas as pd
from time import sleep
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import gspread_dataframe as gd
import gspread as gs
from df2gspread import df2gspread as d2g
import gspread
from df2gspread import df2gspread as d2g

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credential.json', scope)
gc = gspread.authorize(credentials)

'''
gauth = GoogleAuth()

gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
drive = GoogleDrive(gauth)
query = "'{}' in parents and trashed=false"
query=query.format(folder_id)
file_list = drive.ListFile({'q': query}).GetList()
'''



def metrica(solution, response, metrica):
    if metrica == 'ECM':
        ecm = ((solution - response)**2).sum()/len(response)
        return ecm
    if metrica == 'RECM':
        recm = sqrt(((solution - response)**2).sum()/len(response))
        return recm
    if metrica in ['RECALL','ACCURACY']:
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        for i,j in zip(response[response.columns[0]],solution[solution.columns[0]]):
            if (i == j) and (j == 1):
                true_positive += 1
            elif (i==j) and (j == 0):
                true_negative += 1
            elif (i != j) and (j==0):
                false_negative += 1
            elif (i != j) and (j==1):
                false_positive += 1
        recall = true_positive/(true_positive+false_negative)
        accuracy= (true_positive + true_negative)/(true_positive + false_negative + true_negative + false_positive)
        if metrica == 'RECALL':
            return recall
        elif metrica == 'ACCURACY':
            return accuracy

use_metric = ['RECALL', 'ACCURACY']
path_res = "G:/.shortcut-targets-by-id/1L5as_lChFoOSJ5jGRPmbNyBx8OEVaa8ULNbodWk2VX9wJL7ibf0KZKre0sib84zLZuJmxg81/Datathon  (File responses)/Predicciones (File responses)/"
file_sol = 'G:\Mi unidad\Datathon\solution\solution.csv'


solution = pd.read_csv(file_sol)
#students = pd.read_excel('Data 02 Alumnos.xlsx')

files = os.listdir(path_res)
responses = {}
spreadsheet_key = '1732AeZw4d720B5tcm7bxn3YIgVITE6SbBfWiGzD9jB0'

while True:
    for file in files:
        if '.csv' in file:
            name = file.split(' ')
            try:
                response = pd.read_csv(path_res + file)
            except:
                print('cant read')
                continue
            try:
                recm = metrica(solution, response, use_metric[0])
                accuracy = metrica(solution, response, use_metric[1])
                if name[0] in list(responses.keys()):
                        responses[name[0]+name[len(name)-1].replace('.csv','')] = [recm,accuracy]
                else:
                    responses[name[0]] = [recm,accuracy]
            except:
                print("cant save")
                continue
    metric = pd.DataFrame(responses.values(), index = responses.keys())

    metric.columns = use_metric

    metric.sort_values(by = use_metric, ascending= False, axis = 0, inplace=True)
    #metricsdirectory = "G:/.shortcut-targets-by-id/1L5as_lChFoOSJ5jGRPmbNyBx8OEVaa8ULNbodWk2VX9wJL7ibf0KZKre0sib84zLZuJmxg81/Datathon  (File responses)/metricas.gsheet"
    #metric.to_excel(metricsdirectory)
    #metric.to_csv('G:/.shortcut-targets-by-id/1L5as_lChFoOSJ5jGRPmbNyBx8OEVaa8ULNbodWk2VX9wJL7ibf0KZKre0sib84zLZuJmxg81/Datathon  (File responses)/metricas.csv')
    d2g.upload(metric, spreadsheet_key, credentials=credentials, wks_name='Sheet1')
    sleep(90)