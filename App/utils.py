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

def return_models():
    import cloudpickle
    import pandas as pd

    with open('Model/trained_pipeline.pkl', 'rb') as file:
        pipeline = cloudpickle.load(file)

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
    import cloudpickle

    with open('Model/trained_pipeline.pkl', 'rb') as file:
        trained_pipeline = cloudpickle.load(file)


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

