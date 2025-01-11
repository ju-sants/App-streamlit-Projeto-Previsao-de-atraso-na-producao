import streamlit as st
import pandas as pd
import plotly.express as px

from utils import inicialize_variables, get_first_data, set_data_for_modeling, get_predictions


# ----------------- Inicializando ambiente ----------------- #

st.set_page_config(page_title='Página de Predição', layout='wide', page_icon='App/Imgs/Home_PageIcon1.png')

inicialize_variables()


st.title('Previsão de Dias atrasados na produção.')

# ----------------- Dados de entrada do usuário ----------------- #

df_for_pred = get_first_data()

# ----------------- Setando Dados para o modelo ----------------- #

df_for_pred_auto, df_for_pred_prestador = set_data_for_modeling()

# ----------- Desserializando modelo e criando predições  ----------- #


try:

    models, prediction_auto, prediction_prest = get_predictions(df_for_pred_auto, df_for_pred_prestador)

except Exception as e:

    st.write('&nbsp;', unsafe_allow_html=True)
    st.image('App/Imgs/espera_pag_predi.png')
    st.markdown('### ***Tente adicionar itens para visualizar as previsões!***')

    if st.checkbox('Mostrar erro', key='show_error'):

        st.error(e)

# ----------------- Exibição dos resultados ----------------- #

else:

 # ----------------- Salvando predições ---------------------
    prediction_auto_to_save = prediction_auto.copy()
    prediction_prest_to_save = prediction_prest.copy()

    prediction_auto_to_save['Montadores'] = 'AUTOMAÇÃO'
    prediction_prest_to_save['Montadores'] = 'PRESTADOR'

    new_predictions = pd.concat([prediction_auto_to_save, prediction_prest_to_save])
    

    try:
        past_predictions = pd.read_csv('App/Data_2_app/Past predictions/past_predictions.csv')
        past_predictions = pd.concat([past_predictions, new_predictions])
        past_predictions.to_csv('App/Data_2_app/Past predictions/past_predictions.csv', index=False)    

    
    except:
        new_predictions.to_csv('App/Data_2_app/Past predictions/past_predictions.csv', index=False)
    


    type_exibition = st.selectbox('Selecione o tipo de exibição: ', ['Resumo', 'Detalhes'], key='type_exibition')

    for line in range(len(df_for_pred)):
     
        mean_auto = round(prediction_auto.iloc[line].T.mean(), 2)
        mean_prest = round(prediction_prest.iloc[line].T.mean())

        max_auto = prediction_auto.iloc[line].T.max()
        max_prest = prediction_prest.iloc[line].T.max()

        min_auto = prediction_auto.iloc[line].T.min()
        min_prest = prediction_prest.iloc[line].T.min()

        metricas = {
            'Média': [mean_auto, mean_prest],
            'Máximo': [max_auto, max_prest],
            'Mínimo': [min_auto, min_prest]
        }


        if st.session_state.type_exibition == 'Resumo':
            
            metrica = st.radio('Selecione a métrica: ', ['Média', 'Máximo', 'Mínimo'], key=f'metrica_{line}')

            col_resumo_auto, middle, col_resumo_prest = st.columns(3)

            col_resumo_auto.markdown('### ***AUTOMAÇÃO***: ')
            col_resumo_auto.write(f'## {metricas[metrica][0]}')
            col_resumo_auto.write(f'Obs: {metrica}')

            middle.markdown('<div style="text-align: center; font-weight: bold;">VERSUS</div>', unsafe_allow_html=True)

            col_resumo_prest.markdown('### ***PRESTADOR***: ')
            col_resumo_prest.write(f'## {metricas[metrica][1]}')
            col_resumo_prest.write(f'Obs: {metrica}')

            st.write('Para os dados:', df_for_pred.iloc[line].to_frame().T)

            st.write('&nbsp;', unsafe_allow_html=True)
            st.markdown('---')
            

        elif st.session_state.type_exibition == 'Detalhes':

            st.markdown('***Na a situação abaixo...***')
            st.write(df_for_pred.iloc[line].to_frame().T)
            st.write('**Temos:**')



            prediction_line_auto = prediction_auto.iloc[line]
            prediction_line_prest = prediction_prest.iloc[line]

            predictions_line = pd.concat([prediction_line_auto, prediction_line_prest])
            


            st.markdown(f'- **Uma média GERAL de: {round(predictions_line.mean(), 2)} dia(s) de atraso**')

            if min([mean_auto, mean_prest]) == mean_auto:
                st.markdown(f'- **Para este caso, o montador com menor chance de atraso foi AUTOMAÇÃO com: {mean_auto} dia(s)**')
            else:
                st.markdown(f'- **Para este caso, o montador com menor chance de atraso foi PRESTADOR com: {mean_prest} dia(s)**')

            st.write('&nbsp;', unsafe_allow_html=True)
            st.write('<div style="text-align: center; font-weight: bold;">Comparando as previsões...<div>', unsafe_allow_html=True)
            st.write('&nbsp;', unsafe_allow_html=True)


            col_detail_auto, middle, col_detail_prest = st.columns(3)

            col_detail_auto.markdown('Para ***AUTOMAÇÃO***: ')
            col_detail_auto.write(f'Média de atraso de: {mean_auto} dia(s)')
            col_detail_auto.write(f'Maior previsão de atraso: {max_auto} dia(s)')
            col_detail_auto.write(f'Menor previsão de atraso: {min_auto} dia(s)')

            fig_auto = px.bar(x=['Máximo', 'Média', 'Mínimo'], y=[max_auto, mean_auto, min_auto], title='Métricas de Atraso', height=300, text_auto=True).update_traces(marker_color='rgb(0,202,225)', marker_line_color='rgb(0,48,107)', marker_line_width=1.5, opacity=0.6)
            col_detail_auto.plotly_chart(fig_auto, use_container_width=True, key=f'plotly_chart_auto{line}')

            middle.markdown('<div style="text-align: center; font-weight: bold;">VERSUS</div>', unsafe_allow_html=True)

            col_detail_prest.markdown('Para ***PRESTADOR***: ')
            col_detail_prest.write(f'Média de atraso de: {mean_prest} dia(s)')
            col_detail_prest.write(f'Maior previsão de atraso: {max_prest} dia(s)')
            col_detail_prest.write(f'Menor previsão de atraso: {min_prest} dia(s)')

            fig_prest = px.bar(x=['Máximo', 'Média', 'Mínimo'], y=[max_prest, mean_prest, min_prest], title='Métricas de Atraso', height=300, text_auto=True).update_traces(marker_color='rgb(0,202,225)', marker_line_color='rgb(0,48,107)', marker_line_width=1.5, opacity=0.6)
            col_detail_prest.plotly_chart(fig_prest, use_container_width=True, key=f'plotly_chart_prest_{line}')

            


            st.write('<div style="text-align: center;  font-weight: bold;">Estatísticas descritivas das previsões: <div> &nbsp;', unsafe_allow_html=True)
            
            st.write('Para cada linha que passamos para predição, temos 20 previsões de diferentes modelos.')
            st.write('Aqui estão algumas estatísticas descritivas dessas previsões:')


            explicacoes = [
                'Total de Previsões.',
                'Média das previsões.',
                'Variação das previsões, indica quantos pontos as previsões variam de sua média.',
                'Menor previsão de atraso.',
                'Até 25% das previsões estão abaixo desse limiar. Primeiro Quartil.',
                'Até 50% das previsões estão abaixo desse limiar, ponto central. Mediana ou segundo Quartil.',
                'Até 75% das previsões estão abaixo desse limiar. Terceiro Quartil.',
                'Maior previsão de atraso.'
            ]

            stats = predictions_line.describe().to_frame('valores')
            stats['Explicações'] = explicacoes
            stats.index = ['Total', 'Média', 'Variação', 'Mínimo', '25%', '50%', '75%', 'Máximo']

            st.write(stats, use_container_width=True)




            if st.checkbox('Mostrar Tabelas com as predições de todos os modelos', key=f'checkbox_tables_{line}'):
                
                st.write('#### ***Obs: Cada coluna representa um modelo preditivo!***')

                st.subheader('Previsões de atraso para AUTOMAÇÃO: ')
                st.write(prediction_auto.iloc[line].to_frame().T.iloc[:, :8])
                st.write(prediction_auto.iloc[line].to_frame().T.iloc[:, 8:])
                

                st.subheader('Previsões de atraso para PRESTADOR: ')
                st.write(prediction_prest.iloc[line].to_frame().T.iloc[:, :8])
                st.write(prediction_prest.iloc[line].to_frame().T.iloc[:, 8:])


            if st.checkbox('Informações adicionais', key=f'checkbox_additional_informations_{line}'):

                st.write('Pensando nisto...')
            else:
                st.markdown('---')