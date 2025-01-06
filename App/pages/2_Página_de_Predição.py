import streamlit as st
import pandas as pd
import cloudpickle

from utils import itens, capture_item



st.title('Previsão de Dias atrasados na produção.')



ITEM_UNIFICADO = capture_item(st.selectbox('Selecione um Item: ', itens))

QTD = st.number_input('Indique a quantidade: ', min_value=1, max_value=1000000000000000, value=1)

PROCESSO = st.selectbox('Selecione o processo de produção: ', ['REBITAR AUTOMATICO', 'CORTAR FIO', 'EMBALAGEM PLAFON'])


df_for_pred = pd.DataFrame({
        'ITEM UNIFICADO': ['I811402'],
        'QTD': [1],
        'PROCESSO': ['REBITAR AUTOMATICO'],
    })


st.write(df_for_pred)


df_for_pred_auto = df_for_pred.copy()
df_for_pred_auto['PRESTADOR OU AUTOMAÇÃO'] = 'AUTOMAÇÃO'

df_for_pred_prestador = df_for_pred.copy()
df_for_pred_prestador['PRESTADOR OU AUTOMAÇÃO'] = 'PRESTADOR'

with open('App/Model/trained_pipeline.pkl', 'rb') as file:
    trained_pipeline = cloudpickle.load(file)

    
if st.button('Fazer Predição'):


    prediction_auto = trained_pipeline.transform(df_for_pred_auto)
    prediction_prestador = trained_pipeline.transform(df_for_pred_prestador)

    st.write(prediction_prestador)
