import streamlit as st
import pandas as pd

from utils import inicialize_variables, get_first_data, set_data_for_modeling, get_predictions


# ----------------- Inicializando ambiente ----------------- #

st.set_page_config(page_title='Página de Predição', layout='wide', page_icon='App\Imgs\Home_PageIcon1.png')

inicialize_variables()


st.title('Previsão de Dias atrasados na produção.')

# ----------------- Dados de entrada do usuário ----------------- #

df_for_pred = get_first_data()

# ----------------- Setando Dados para o modelo ----------------- #

df_for_pred_auto, df_for_pred_prestador = set_data_for_modeling()

# ----------- Desserializando modelo e criando predições  ----------- #


try:
    prediction_auto, prediction_prest = get_predictions(df_for_pred_auto, df_for_pred_prestador)

except:

    st.write('&nbsp;', unsafe_allow_html=True)
    st.image('App\Imgs\espera_pag_predi.png')
    st.markdown('### ***Tente adicionar itens para visualizar as previsões!***')

# ----------------- Exibição dos resultados ----------------- #

else:

    type_exibition = st.selectbox('Selecione o tipo de exibição: ', ['Resumo', 'Detalhes'], key='type_exibition')

    for line in range(len(df_for_pred)):
     
        mean_auto = prediction_auto.iloc[line].T.mean()
        mean_prest = prediction_prest.iloc[line].T.mean()

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
            


            st.markdown(f'- **Uma média GERAL de: {predictions_line.mean()} dia(s) de atraso**')

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

            middle.markdown('<div style="text-align: center; font-weight: bold;">VERSUS</div>', unsafe_allow_html=True)

            col_detail_prest.markdown('Para ***PRESTADOR***: ')
            col_detail_prest.write(f'Média de atraso de: {mean_prest} dia(s)')
            col_detail_prest.write(f'Maior previsão de atraso: {max_prest} dia(s)')
            col_detail_prest.write(f'Menor previsão de atraso: {min_prest} dia(s)')


            st.markdown('---')



            if st.checkbox('Mostrar Tabelas com as predições de todos os modelos', key=f'checkbox_tables_{line}'):
                
                st.write('#### ***Obs: Cada coluna representa um modelo preditivo!***')

                st.subheader('Previsões de atraso para AUTOMAÇÃO: ')
                st.write(prediction_auto.iloc[line].to_frame().T.iloc[:, :6])
                st.write(prediction_auto.iloc[line].to_frame().T.iloc[:, 6:])
                

                st.subheader('Previsões de atraso para PRESTADOR: ')
                st.write(prediction_prest.iloc[line].to_frame().T.iloc[:, :6])
                st.write(prediction_prest.iloc[line].to_frame().T.iloc[:, 6:])


            if st.checkbox('Informações', key=f'checkbox_informations_{line}'):


                col_results_auto, col_results_prest = st.columns(2)


                col_results_auto.write('Previsões de atraso para AUTOMAÇÃO: ')
                for column, lines in prediction_auto.iloc[line].to_frame().T.items():
                    values = ', '.join(map(str, lines.values))
                    col_results_auto.write(f'Para o modelo {column} entre: {values} dia(s) atrasado')

                col_results_prest.write('Previsões de atraso para PRESTADOR: ')
                for column, lines in prediction_prest.iloc[line].to_frame().T.items():
                    values = ', '.join(map(str, lines.values))
                    col_results_prest.write(f'Para o modelo {column} entre: {values} dia(s) atrasado')

            else:
                st.markdown('---')