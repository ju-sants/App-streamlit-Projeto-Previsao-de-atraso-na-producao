import streamlit as st
import pandas as pd
import cloudpickle

from utils import itens, capture_item


if not 'df_for_pred' in st.session_state:
    st.session_state.df_for_pred = pd.DataFrame(columns=['ITEM UNIFICADO', 'QTD', 'PROCESSO'])

if not 'type_exibition' in st.session_state:
    st.session_state.type_exibition = 'Resumo'

if not 'type_detail' in st.session_state:
    st.session_state.type_detail = 'Tabelas'


st.title('Previsão de Dias atrasados na produção.')



# ----------------- Dados de entrada ----------------- #

dict2df = {
        'ITEM UNIFICADO': [],
        'QTD': [],
        'PROCESSO': [],
    }


ITEM_UNIFICADO = capture_item(st.sidebar.selectbox('Selecione um Item: ', itens))

QTD = st.sidebar.number_input('Indique a quantidade: ', min_value=1, max_value=1000000000000000, value=1)

PROCESSO = st.sidebar.selectbox('Selecione o processo de produção: ', ['REBITAR AUTOMATICO', 'CORTAR FIO', 'EMBALAGEM PLAFON'])

col_butt1, col_butt2 = st.sidebar.columns(2)

if col_butt1.button('Adicionar item'):
    st.session_state.df_for_pred.loc[len(st.session_state.df_for_pred)] = {'ITEM UNIFICADO': ITEM_UNIFICADO, 'QTD': QTD, 'PROCESSO': PROCESSO}

if col_butt2.button('Remover item'):
    if not st.session_state.df_for_pred.empty:
        st.session_state.df_for_pred = st.session_state.df_for_pred[:-1]


df_for_pred = st.session_state.df_for_pred.copy()


# ----------------- Visualizando predições ----------------- #

st.sidebar.write(df_for_pred)


df_for_pred_auto = df_for_pred.copy()
df_for_pred_auto['PRESTADOR OU AUTOMAÇÃO'] = 'AUTOMAÇÃO'

df_for_pred_prestador = df_for_pred.copy()
df_for_pred_prestador['PRESTADOR OU AUTOMAÇÃO'] = 'PRESTADOR'

with open('Model/trained_pipeline.pkl', 'rb') as file:
    trained_pipeline = cloudpickle.load(file)

try:

    prediction_auto = trained_pipeline.transform(df_for_pred_auto)
    prediction_prest = trained_pipeline.transform(df_for_pred_prestador)

except:

    pass

else:

    type_exibition = st.selectbox('Selecione o tipo de exibição: ', ['Resumo', 'Detalhes'], key='type_exibition')

    if st.session_state.type_exibition == 'Resumo':

        st.write('Trabalhando...')

    elif st.session_state.type_exibition == 'Detalhes':
        
        type_detail = st.selectbox('Selecione o tipo de disposição dos dados: ', ['Tabelas', 'Informações', 'Não quero ver nada'], key='type_detail')

        if type_detail == 'Tabelas':

            st.subheader('Previsão de atraso para AUTOMAÇÃO: ')
            st.write(prediction_auto)

            st.subheader('Previsão de atraso para PRESTADOR: ')
            st.write(prediction_prest)

        elif type_detail == 'Informações':


            col__results_auto, col__results_prest = st.columns(2)

            col__results_auto.write('Previsão de atraso para AUTOMAÇÃO: ')
            for column, lines in prediction_auto.items():
                values = ', '.join(map(str, lines.values))
                col__results_auto.write(f'Para o modelo {column} entre: {values} dia(s) atrasado')

            col__results_prest.write('Previsão de atraso para PRESTADOR: ')
            for column, lines in prediction_prest.items():
                values = ', '.join(map(str, lines.values))
                col__results_prest.write(f'Para o modelo {column} entre: {values} dia(s) atrasado')

        else:
            st.write('Nada por aqui...')