from math import sqrt
import pandas as pd
import os
from time import sleep

def metrica(solution, response, metrica):
    if metrica == 'ECM':
        ecm = ((solution - response)**2).sum()/len(response)
        return ecm
    if metrica == 'RECM':
        recm = sqrt(((solution - response)**2).sum()/len(response))
        return recm
    if metrica == 'RECALL':
        true_positive = 0
        false_negative = 0
        for i,j in zip(response[response.columns[0]],solution[solution.columns[0]]):
            if (i == j) and (j == 0):
                true_positive += 1
            elif (i != j) and (j==0):
                false_negative += 1
        recall = true_positive/(true_positive+false_negative)
        return recall

use_metric = 'RECALL'
path_res = 'G:/My Drive/Datathon_responses/responses/'
file_sol = 'G:/My Drive/Datathon_solutions/solution.csv'



solution = pd.read_csv(file_sol)
#students = pd.read_excel('Data 02 Alumnos.xlsx')


while True:
    files = os.listdir(path_res)
    responses = {}
    for file in files:
        if '.csv' not in file:
            print('Not in file')
            continue
        name = file.split(' ')
        try:
            response = pd.read_csv(path_res + file)
        except:
            print('cant read')
            continue
        try:
            recm = metrica(solution, response, use_metric)
            if name[0] in list(responses.keys()):
                   responses[name[0]+name[len(name)-1].replace('.csv','')] = recm
            else:
                responses[name[0]] = recm
        except:
            print("cant save")
            continue
    metric = pd.DataFrame(responses.values(), index = responses.keys())

    metric.columns = [use_metric]

    metric.sort_values(by = use_metric, ascending= False, axis = 0, inplace=True)

    metric.to_excel('G:/My Drive/Datathon_solutions/metrics.xlsx')
    sleep(60)