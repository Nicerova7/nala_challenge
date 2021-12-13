from fastapi import FastAPI, File, UploadFile
from datetime import datetime
import pickle
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler

app = FastAPI()
# load the model from disk
model_loaded = pickle.load(open('modelo_final.sav', 'rb'))
df_ref = pd.read_csv('DS Challenge.csv', sep=';', encoding='utf8')

def split_dispositivo_column(row):
    dispositivo = row['dispositivo'].replace(';', ',').replace('\'','\"')
    model = json.loads(dispositivo).get('model')
    score = json.loads(dispositivo).get('device_score')
    os = json.loads(dispositivo).get('os')
    os = 'unknown_category_1' if os == ',' else ('unknown_category_2' if os == '%%' else os)
    return pd.Series([model, score, os])

def process_df(df):
    df['cashback'] = df['cashback'].str.replace(',', '.').astype(float)
    df['monto'] = df['monto'].str.replace(',', '.').astype(float)
    df['dcto'] = df['dcto'].str.replace(',', '.').astype(float)

    # https://www.utf8-chartable.de/unicode-utf8-table.pl?start=128&number=128&utf8=string-literal&unicodeinhtml=hex
    df['tipo_tc'] = df['tipo_tc'].str.replace('\xc3\xad','í').astype(str) 

    df['date'] = df.apply(lambda row: datetime.strptime(str(row['fecha']) + ' ' + str(row['hora']) + ':00:00', '%d/%m/%Y %H:%M:%S').timestamp(), axis=1)
    df['date'] = df['date'].astype('int64')

    df['genero'] = df['genero'].replace('--', np.NaN)

    df[['dispositivo_model', 'dispositivo_puntaje', 'dispositivo_os']] = df.apply(split_dispositivo_column, axis = 1)

    df = df.drop(['ID_USER', 'fecha', 'hora', 'dispositivo', 'dispositivo_model'], axis=1)

    df['is_prime'] = df['is_prime'].astype(int)
    df['fraude'] = df['fraude'].astype(int)

    std_scaler = StandardScaler() # no outliers para monto y date
    rob_scaler = RobustScaler() # robusto cuando hay outliers : como dcto y cashback (como vimos en EDA.ipynb)


    df['monto'] = std_scaler.fit_transform(df['monto'].values.reshape(-1,1))
    df['date'] = std_scaler.fit_transform(df['date'].values.reshape(-1,1))

    df['dcto'] = rob_scaler.fit_transform(df['dcto'].values.reshape(-1,1))
    df['cashback'] = rob_scaler.fit_transform(df['cashback'].values.reshape(-1,1))

    cat_vars=['genero', 'establecimiento','ciudad','tipo_tc','linea_tc','interes_tc','status_txn', 'dispositivo_puntaje', 'dispositivo_os']
    for var in cat_vars:
        cat_list='var'+'_'+var
        cat_list = pd.get_dummies(df[var], prefix=var)
        data_temp=df.join(cat_list)
        df=data_temp

    data_vars=df.columns.values.tolist()
    to_keep=[i for i in data_vars if i not in cat_vars]

    df_final=df[to_keep]
    X = df_final.drop('fraude', axis=1)
    return X.values

@app.post("/files/")
async def create_file(file: UploadFile = File(...)):
    global df_ref
    df = pd.read_csv(file.file, sep=';', encoding='utf8')
    #TODO: evitar usar el df_referencial porque demora en cargar
    # Esto se uso simplemente por el tiempo limite del challenge
    x = process_df(df_ref.append(df,  ignore_index = True))
    y_pred = model_loaded.predict(x)
    return {"¿ Fraude ? ": 'Si' if y_pred[-1] else 'No'}
