import streamlit as st
import pandas as pd
import plotly.express as px
from utils import return_models, inicialize_variables, return_metrics_dfs, return_models_exp

st.set_page_config(page_title="Informações", page_icon=r"App/Imgs/Home_PageIcon1.png", layout="wide")

inicialize_variables()

st.title('Informações, dados e estatísticas')

exibition = st.selectbox('Selecione uma exibição: ', ['Informações técnicas dos modelos', 'Sobre os Dados'], key='exibition_pag_info')

if exibition == 'Informações técnicas dos modelos':

    st.subheader('Informações sobre dos modelos utilizados')

    # ----------------- Checkboxes com os nomes dos modelos

    models_names_n_todos = [type(model).__name__ for model in return_models()]

    models_names_n_todos = list(set(models_names_n_todos))

    models_names_n_todos.insert(0, 'Todos')

    options = {}

    col_options_models_info1, col_options_models_info2 = st.columns(2)

    for idx, option in enumerate(models_names_n_todos):

        if idx % 2 == 0:
            if option == 'Todos':
                options[option] = col_options_models_info1.checkbox(option, value=True) # Deixando a opção todos selecionada previamente
            
            else:
                options[option] = col_options_models_info1.checkbox(option)

        else:
            options[option] = col_options_models_info2.checkbox(option)


    # -------------- Páginas de informações ----------------------

    tab_inst_hiper_metr, tab_saiba_mais, tab_ranking_otm = st.tabs(['Instaciamento, HiperParâmetros e Métricas', 'Saiba mais sobre os algoritmos', 'Ranking e Otimismo'])

    st.markdown('---')

    # ---------------- armazenando opçoes escolhidas ----------------

    options_selected = []

    for option, state in  options.items():

        if state:
            options_selected.append(option)


    # --------------------- Tratamento de inconsistências -----------------------

    if 'Todos' in options_selected and len(options_selected) > 1:
        st.error('Você só pode selecionar "Todos" se for a única opção selecionada.')


    # ---------------- Inserindo informações nas páginas ---------------------
    else:
        with tab_inst_hiper_metr:
            st.success("""
                - A MAE (Mean Absolute Error) calcula a média dos erros absolutos entre as previsões (𝑦^y^) e os valores reais (𝑦 y) sendo fácil de interpretar, pois está na mesma escala dos dados e trata todos os erros de forma uniforme.
                - A MSE (Mean Squared Error) usa o quadrado dos erros, penalizando mais os erros grandes, o que é útil quando discrepâncias maiores têm maior impacto no problema. No entanto, como os valores ficam em unidades quadradas, pode ser menos intuitivo.
                - A RMSE (Root Mean Squared Error) é a raiz quadrada da MSE, trazendo os erros de volta à escala original dos dados, mas mantendo a penalização maior para erros grandes. A escolha entre elas depende do quanto você quer penalizar erros maiores e da necessidade de interpretar os valores diretamente na escala dos dados.
                """)
            st.markdown('---')

        if options_selected == ['Todos']:
            st.write("Você selecionou todos os modelos.")
            with tab_inst_hiper_metr:
                for model in return_models():
                    parametros = f'{model}'.split('(')[1]
                    parametros = parametros.split(')')[0]

                    if parametros == '' or parametros == 'random_state=42':
                        st.write(f"Modelo: {type(model).__name__}")
                        st.markdown(f"`{model}`")

                        st.markdown('&nbsp;', unsafe_allow_html=True)
                        st.markdown('***Métricas do modelo***')

                        st.write(return_metrics_dfs()[type(model).__name__])

                    else:
                        st.write(f"Modelo: {type(model).__name__} - Com Otimização de HiperParâmetros")
                        st.markdown(f"`{model}`")

                        st.markdown('&nbsp;', unsafe_allow_html=True)
                        st.markdown('***Métricas do modelo***')

                        st.write(return_metrics_dfs()[f'{type(model).__name__} - tunned'])

                    st.markdown("---")

            with tab_saiba_mais:
                models_names = []
                for model in return_models():
                    models_names.append(type(model).__name__)
                
                for unique_model_name in set(models_names):
                    st.success(return_models_exp()[unique_model_name])

            with tab_ranking_otm:
                
                ranking_tab, otimismo_tab = st.tabs(['Ranking', 'Otimismo dos modelos'])
                

                with ranking_tab:
                    st.subheader('Ranking')
                    metrics_dfs_formateded = []

                    for key, metric_df in return_metrics_dfs().items():
                        metrics_dfs_formateded.append(metric_df.drop('Nome do modelo: ').rename(columns={'Resultados': key}))

                    metrics_dfs_all = pd.concat(metrics_dfs_formateded, axis=1).T.abs()

                    min_mae = metrics_dfs_all.T.loc['MAE: '].min()
                    melhor_mae = metrics_dfs_all[metrics_dfs_all[metrics_dfs_all == min_mae].any(axis=1)].index.tolist()[0]

                    min_mse = metrics_dfs_all.T.loc['MSE: '].min()
                    melhor_mse = metrics_dfs_all[metrics_dfs_all[metrics_dfs_all == min_mse].any(axis=1)].index.tolist()[0]

                    min_rmse = metrics_dfs_all.T.loc['MAE: '].min()
                    melhor_rmse = metrics_dfs_all[metrics_dfs_all[metrics_dfs_all == min_rmse].any(axis=1)].index.tolist()[0]

                    st.write('- TOP 1º Melhor modelo em MAE: ', melhor_mae, ', com uma avaliação de: ', min_mae)
                    st.write('- TOP 1º Melhor modelo em MSE: ', melhor_mse, ', com uma avaliação de: ', min_mse)
                    st.write('- TOP 1º Melhor modelo em RMSE: ', melhor_rmse, ', com uma avaliação de: ', min_rmse)

                    st.write('&nbsp;', unsafe_allow_html=True)
                    st.write('<div style="text-align: center; font-weight: bold;">Gráficos<div>', unsafe_allow_html=True)
                    fig_mae = px.bar(data_frame=metrics_dfs_all, x=metrics_dfs_all.index, y=metrics_dfs_all['MAE: '], labels={"MAE: ": 'Métrica', 'index': 'Modelos'})
                    fig_mse = px.bar(data_frame=metrics_dfs_all, x=metrics_dfs_all.index, y=metrics_dfs_all['MSE: '], labels={"MSE: ": 'Métrica', 'index': 'Modelos'})
                    fig_rmse = px.bar(data_frame=metrics_dfs_all, x=metrics_dfs_all.index, y=metrics_dfs_all['RMSE: '], labels={"RMSE: ": 'Métrica', 'index': 'Modelos'})

                    col_fig_rmse, col_fig_mse = st.columns(2)

                    col_fig_rmse.plotly_chart(fig_rmse)
                    col_fig_mse.plotly_chart(fig_mse)
                    st.plotly_chart(fig_mae)

                # ------------------------ Otimismo ----------------------
                with otimismo_tab:

                    st.subheader('Otimismo dos modelos')

                    st.success("""
                        - Modelos Otimistas são aqueles que geralmente preveem resultados abaixo do limiar central das previsões (que poderia ser a média ou mediana).
                        - Modelos pessimistas preveem resultados maiores que o limiar central
                        - Modelos Neutros preveem resultados alinhados a média ou mediana
                        """)

                    limiar_central = st.radio('Com base em que limiar?: ', ['Média', 'Mediana'])

                    try:
                        all_predictions = pd.read_csv('App/Data_2_app/Past predictions/past_predictions.csv')
                    
                    except Exception:
                        st.error('Faça Predições primeiro.')

                    else:
                        col_otimistas, col_neutros, col_pessimistas = st.columns(3)

                        col_pessimistas.subheader('Modelos pessimistas')
                        col_pessimistas.markdown('---')

                        col_otimistas.subheader('Modelos otimistas')
                        col_otimistas.markdown('---')

                        col_neutros.subheader('Modelos neutros')
                        col_neutros.markdown('---')


                        for column in all_predictions.drop(columns='Montadores').columns:

                            if limiar_central == 'Mediana':
                                if all_predictions[column].mean() > all_predictions.drop(columns='Montadores').mean().T.quantile(0.5):
                                    col_pessimistas.write(f'`{column}`')

                                elif all_predictions[column].mean() < all_predictions.drop(columns='Montadores').mean().T.quantile(0.5):
                                    col_otimistas.write(f'`{column}`')
                                    
                                else: 
                                    col_neutros.write(f'`{column}`')
                            
                            else:
                                if all_predictions[column].mean() > all_predictions.drop(columns='Montadores').mean().T.mean():
                                    col_pessimistas.write(f'`{column}`')

                                elif all_predictions[column].mean() < all_predictions.drop(columns='Montadores').mean().T.mean():
                                    col_otimistas.write(f'`{column}`')
                                    
                                else: 
                                    col_neutros.write(f'`{column}`')

        else:           
            
            with tab_inst_hiper_metr:
                for model_name in options_selected:
                    for model in return_models():
                        if type(model).__name__ == model_name:
                            parametros = f'{model}'.split('(')[1]
                            parametros = parametros.split(')')[0]

                            if parametros == '' or parametros == 'random_state=42':
                                st.write(f"Modelo: {type(model).__name__}")
                                st.markdown(f"`{model}`")

                                st.markdown('&nbsp;', unsafe_allow_html=True)
                                st.markdown('***Métricas do modelo***')


                                st.write(return_metrics_dfs()[type(model).__name__])

                                st.markdown('---')

                            else:
                                st.write(f"Modelo: {type(model).__name__} - Com Otimização de HiperParâmetros")
                                st.markdown(f"`{model}`")

                                st.markdown('&nbsp;', unsafe_allow_html=True)
                                st.markdown('***Métricas do modelo***')


                                st.write(return_metrics_dfs()[f'{type(model).__name__} - tunned'])

                                st.markdown('---')



            with tab_saiba_mais:
                models_names = []
                
                for model_name in options_selected:
                    for model in return_models():
                        if type(model).__name__ == model_name:
                            models_names.append(model_name)

                for unique_model_name in set(models_names):
                    st.success(return_models_exp()[unique_model_name])

elif exibition == 'Sobre os Dados':
    st.subheader('Tabela com as médias de atraso pelo montador: PRESTADOR')

    tabela_medias_prest = pd.read_csv('App/Data_2_app/Tabelas/tabela_medias_produto_prestador.csv')
    st.write(tabela_medias_prest)


    st.subheader('Tabela com as médias de atraso pelo montador: AUTOMAÇÃO')

    tabela_medias_auto = pd.read_csv('App/Data_2_app/Tabelas/tabela_medias_produto_automacao.csv')
    st.write(tabela_medias_auto)