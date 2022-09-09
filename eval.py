from math import sqrt
import pandas as pd
import os
from time import sleep

def metrica(solution, response, metrica):
    if metrica == 'ECM':
        ecm = ((solution - response).sum()**2)/len(response)
        return ecm
    if metrica == 'RECM':
       recm = sqrt(((solution - response).sum()**2)/len(response))
       return recm

use_metric = 'RECM'
path_res = 'G:/My Drive/Datathon_responses/responses/'
file_sol = 'G:/My Drive/Datathon_solutions/solution.csv'

files = os.listdir(path_res)

solution = pd.read_csv(file_sol)
responses = {}

while True:
    for file in files:
        if '.csv' not in file:
            continue
        name = file.split(' ')
        response = pd.read_csv(path_res + file)
        responses[name[0]] = metrica(solution, response, use_metric)


    metric = pd.DataFrame(responses.values(), index = responses.keys())

    metric.columns = [use_metric]

    metric.to_csv('metrics.csv')
    sleep(60)