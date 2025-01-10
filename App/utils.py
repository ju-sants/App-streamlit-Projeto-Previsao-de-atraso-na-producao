import pandas as pd

itens = ['ITEM UNIFICADO: I811412 | Desc Item: MODULO TOMADA 20A 250V~ SLIM MON',
        'ITEM UNIFICADO: I811412 | Desc Item: MODULO TOMADA 20A 250V~ SLIM MON',  
        'ITEM UNIFICADO: I811422 | Desc Item: MODULO TOMADA 20A 250V~ VERM SLIM MON',  
        'ITEM UNIFICADO: I811402 | Desc Item: MODULO TOMADA 10A 250V~ SLIM MON',
        'ITEM UNIFICADO: I8114142 | Desc Item: MODULO TOMADA 20A 250V~ PT SLIM MON',  
        'ITEM UNIFICADO: I751401 | Desc Item: MODULO TOMADA 10A 250V~ VIVAZ MON',
        'ITEM UNIFICADO: I751411 | Desc Item: MODULO TOMADA 20A 250V~ VIVAZ',
        'ITEM UNIFICADO: I751421 | Desc Item: MODULO TOMADA 20A 250V~ VERM VIVAZ',  
        'ITEM UNIFICADO: I8114042 | Desc Item: MODULO TOMADA 10A 250V~ PT SLIM MON',
        'ITEM UNIFICADO: I811402 | Desc Item: MODULO TOMADA 10A SLIM MON', 
        'ITEM UNIFICADO: I751401 | Desc Item: MODULO TOMADA 10A 250V~ VIVAZ ALT 1',
        'ITEM UNIFICADO: 0413131 | Desc Item: TERMINAL MONTADO P/ TOMADA 10A E 20A MODULAR',  
        'ITEM UNIFICADO: I811422 | Desc Item: MODULO TOMADA 20A 250V~ VERM SLIM MON NOVO',
        'ITEM UNIFICADO: I8114142 | Desc Item: MODULO TOMADA 20A PT SLIM MON',
        'ITEM UNIFICADO: I751401 | Desc Item: MODULO TOMADA 10A VIVAZ',
        'ITEM UNIFICADO: I811412 | Desc Item: MODULO TOMADA 20A SLIM MON',
        'ITEM UNIFICADO: I751411 | Desc Item: MODULO TOMADA 20A VIVAZ',
        'ITEM UNIFICADO: I8114042 | Desc Item: MODULO TOMADA 10A PT SLIM MON',
        'ITEM UNIFICADO: I7514041 | Desc Item: MODULO TOMADA 10A PT VIVAZ',
        'ITEM UNIFICADO: I7514141 | Desc Item: MODULO TOMADA 20A PT VIVAZ', 
        'ITEM UNIFICADO: I95140 | Desc Item: MODULO TOMADA 10A 250V~ I9 MON',
        'ITEM UNIFICADO: I95141 | Desc Item: MODULO TOMADA 20A 250V~ I9 MON',
        'ITEM UNIFICADO: I95142 | Desc Item: MODULO TOMADA 20A 250V~ VERM I9 MON',
        'ITEM UNIFICADO: I751421 | Desc Item: MODULO TOMADA 20A VERMELHA - VIVAZ',
]

def return_metrics_dfs():
    import pandas as pd
    models_names = ["SVR - tunned",
    "SVR",
    "LGBMRegressor - tunned",
    "TheilSenRegressor",
    "KNeighborsRegressor - tunned",
    "SGDRegressor - tunned",
    "Lasso",
    "LinearRegression - tunned",
    "ElasticNet",
    "ElasticNet - tunned",
    "ExtraTreesRegressor - tunned",
    "ExtraTreesRegressor",
    "DecisionTreeRegressor - tunned",
    "DecisionTreeRegressor",
    "BayesianRidge - tunned",
    "MLPRegressor",
    "AdaBoostRegressor - tunned"]

    archives = ["cv_svm.csv",
    "cv_svr_norm.csv",
    "cv_lgbm.csv",
    "cv_ts.csv",
    "cv_knn.csv",
    "cv_sgd.csv",
    "cv_ls.csv",
    "cv_lr.csv",
    "cv_en_norm.csv",
    "cv_ext.csv",
    "cv_ext_norm.csv",
    "cv_dtr_tunned.csv",
    "cv_br.csv",
    "cv_dtr.csv",
    "cv_neural.csv",
    "cv_en.csv",
    "cv_ada.csv"]



    models_metrics = {}

    for model_name, archive in zip(models_names, archives):
        models_metrics[model_name] = pd.read_csv(f'App/Data_2_app/models metrics/{archive}')
        models_metrics[model_name].columns = ['Nome do modelo: ', 'MSE: ', 'RMSE: ', 'MAE: ']
        models_metrics[model_name] = models_metrics[model_name].T.rename(columns={0: 'Resultados'})
    
    return models_metrics

def return_models_exp():
    explications = {
    'SVR': """**SVR (Support Vector Regressor):**  
    Um modelo de regressão baseado no SVM. Ele busca encontrar um hiperplano que melhor se ajuste aos dados, permitindo um desvio controlado ((epsilon)) ao redor das previsões. Isso significa que pequenas discrepâncias não são penalizadas, mas desvios maiores são. Ideal para problemas não lineares, utilizando kernels como RBF, linear e polinomial para capturar padrões complexos.""",

    'LGBMRegressor': """**LGBMRegressor (LightGBM):**  
    Algoritmo de gradient boosting que constrói árvores de decisão de forma iterativa. É otimizado para lidar com grandes conjuntos de dados com alta dimensionalidade. Sua eficiência em velocidade e memória o torna ideal para competições de machine learning. Exemplo de uso: prever preços de imóveis com muitas variáveis.""",

    'TheilSenRegressor': """**TheilSenRegressor:**  
    Método robusto para regressão linear que minimiza o impacto de outliers. Ele calcula coeficientes baseados na mediana dos gradientes de todas as combinações possíveis de subconjuntos de dados, resultando em um modelo confiável em cenários ruidosos.""",

    'KNeighborsRegressor': """**KNeighborsRegressor:**  
    Um modelo baseado no algoritmo K-Nearest Neighbors (KNN). Ele faz previsões tomando a média dos valores dos (k) vizinhos mais próximos. É simples e eficaz para problemas onde os dados apresentam padrões locais homogêneos, mas pode ser ineficiente para conjuntos de dados grandes ou com alta dimensionalidade.""",

    'SGDRegressor': """**SGDRegressor (Stochastic Gradient Descent):**  
    Utiliza a técnica de descida de gradiente estocástica para treinar modelos de regressão linear. É eficiente para grandes conjuntos de dados, suportando regularizações Lasso ((L1)) e Ridge ((L2)). Exemplo: prever vendas futuras com milhões de registros.""",

    'Lasso': """**Lasso (Least Absolute Shrinkage and Selection Operator):**  
    Um modelo de regressão linear que aplica uma penalidade L1 para forçar alguns coeficientes a zero, resultando em seleção automática de características. Ideal para problemas onde a redução do número de variáveis é crucial.""",

    'LinearRegression': """**LinearRegression:**  
    O modelo básico de regressão linear, que assume uma relação linear entre variáveis preditoras e a variável resposta. Utiliza mínimos quadrados para encontrar os coeficientes que minimizam o erro. Exemplo: prever o impacto de preços em vendas.""",

    'ElasticNet': """**ElasticNet:**  
    Combina as penalizações L1 (Lasso) e L2 (Ridge) para criar um modelo robusto em situações onde há alta multicolinearidade entre variáveis. É especialmente útil em dados de alta dimensionalidade com muitas correlações.""",

    'ExtraTreesRegressor': """**ExtraTreesRegressor:**  
    Um modelo baseado em ensembles que constrói várias árvores de decisão, usando amostras aleatórias de dados e divisões aleatórias em cada nó. Ele é mais rápido que o Random Forest, mas pode superajustar se os hiperparâmetros não forem bem calibrados.""",

    'DecisionTreeRegressor': """**DecisionTreeRegressor:**  
    Constrói um modelo em forma de árvore que divide os dados com base em condições simples. Fácil de interpretar e não requer pré-processamento significativo. Porém, é propenso ao overfitting se não for controlado.""",

    'BayesianRidge': """**BayesianRidge:**  
    Modelo de regressão linear que utiliza inferência Bayesiana para estimar os coeficientes e adiciona regularização automática. Ideal para conjuntos de dados pequenos ou com incertezas.""",

    'MLPRegressor': """**MLPRegressor (Multi-Layer Perceptron Regressor):**  
    Uma rede neural para regressão que utiliza camadas totalmente conectadas. Adequado para capturar relações não lineares complexas. Requer mais dados e ajuste fino de hiperparâmetros como número de camadas e taxa de aprendizado.""",

    'AdaBoostRegressor': """**ADABoostRegressor:**  
    Algoritmo de ensemble que combina vários modelos simples, como árvores de decisão rasas, para criar um preditor mais robusto. Ele ajusta erros de iterações anteriores, melhorando gradativamente a precisão.""",
}

    return explications

def return_models():
    import dill
    import pandas as pd
    import streamlit as st

    with open('Model/trained_pipeline.pkl', 'rb') as file:
        pipeline = dill.load(file)

    models, _ = pipeline.transform(pd.DataFrame({'ITEM UNIFICADO': ['I811412'], 'QTD': [1], 'PROCESSO': ['REBITAR AUTOMATICO'], 'PRESTADOR OU AUTOMAÇÃO': ['AUTOMAÇÃO']}))
    return models
    

def capture_item(concatenated_item):

    splitted_item = concatenated_item.split(' ')[2]

    return splitted_item

def inicialize_variables():

    import streamlit as st
    import pandas as pd

    if not 'df_for_pred' in st.session_state:
        st.session_state.df_for_pred = pd.DataFrame(columns=['ITEM UNIFICADO', 'QTD', 'PROCESSO'])

    if not 'type_exibition' in st.session_state:
        st.session_state.type_exibition = 'Resumo'

    if not 'type_detail' in st.session_state:
        st.session_state.type_detail = 'Tabelas'

    if not 'active_button' in st.session_state:
        st.session_state.active_button = None


def get_first_data():

    import streamlit as st


    ITEM_UNIFICADO = capture_item(st.sidebar.selectbox('Selecione um Item: ', itens))

    QTD = st.sidebar.number_input('Indique a quantidade: ', min_value=1, max_value=1000000000000000, value=1)

    PROCESSO = st.sidebar.selectbox('Selecione o processo de produção: ', ['REBITAR AUTOMATICO', 'CORTAR FIO', 'EMBALAGEM PLAFON'])

    col_butt1, col_butt2 = st.sidebar.columns(2)

    if col_butt1.button('Adicionar item'):
        st.session_state.df_for_pred.loc[len(st.session_state.df_for_pred)] = {'ITEM UNIFICADO': ITEM_UNIFICADO, 'QTD': QTD, 'PROCESSO': PROCESSO}

    if col_butt2.button('Remover item'):
        if not st.session_state.df_for_pred.empty:
            st.session_state.df_for_pred = st.session_state.df_for_pred[:-1]

    return st.session_state.df_for_pred

def set_data_for_modeling():

    import streamlit as st

    df_for_pred = st.session_state.df_for_pred.copy()

    st.sidebar.write(df_for_pred)


    df_for_pred_auto = df_for_pred.copy()
    df_for_pred_auto['PRESTADOR OU AUTOMAÇÃO'] = 'AUTOMAÇÃO'

    df_for_pred_prestador = df_for_pred.copy()
    df_for_pred_prestador['PRESTADOR OU AUTOMAÇÃO'] = 'PRESTADOR'

    return df_for_pred_auto, df_for_pred_prestador


def get_predictions(df_for_pred_auto, df_for_pred_prestador):

    import streamlit as st
    import dill

    with open('Model/trained_pipeline.pkl', 'rb') as file:
        trained_pipeline = dill.load(file)


    _, prediction_auto = trained_pipeline.transform(df_for_pred_auto)
    _, prediction_prest = trained_pipeline.transform(df_for_pred_prestador)

    models, _ = trained_pipeline.transform(df_for_pred_auto)

    return models, prediction_auto, prediction_prest

def get_models_info(models):
    
    import pandas as pd

    df_models_params = pd.DataFrame()

    for model in models:
            
        df_models_params[type(model).__name__] = model.get_params()
    
    return df_models_params

