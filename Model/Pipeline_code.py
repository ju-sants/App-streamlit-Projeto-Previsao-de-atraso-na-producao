import pandas as pd

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin


from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.base import BaseEstimator, TransformerMixin

class pre_process(BaseEstimator, TransformerMixin):
    import pandas as pd

    def __init__(self):

        from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, MinMaxScaler
        from sklearn import set_config

        set_config(transform_output='pandas')


        self.media_por_item = {
          '0413131': 45.707045735475894, 'I751401': 12.75,
          'I7514041': 6.0, 'I751411': 21.476190476190474,
          'I7514141': 31.333333333333332, 'I751421': 8.75,
          'I811402': 24.252, 'I8114042': 12.0,
          'I811412': 25.650602409638555, 'I8114142': 24.857142857142858,
          'I811422': 16.46875, 'I95140': 31.081967213114755,
          'I95141': 22.0, 'I95142': 39.333333333333336
          }
        self.labelencoder = LabelEncoder()
        self.onehot = OneHotEncoder(sparse_output=False)
        self.scaler = MinMaxScaler()
        self.fitted_ = False

    def fit(self, X=None, y=None):

        numeric_cols = X.select_dtypes('number')
        itemOrdinal = pd.Series(self.labelencoder.fit_transform(X[['ITEM UNIFICADO']]).reshape(-1)).to_frame('ITEM UNIFICADO')
        dummies = self.onehot.fit_transform(X.drop(columns=['ITEM UNIFICADO', 'QTD']))
        df = pd.concat([itemOrdinal, numeric_cols, dummies], axis=1)

        df['Dias Atrasado_media_por_item'] = X['ITEM UNIFICADO'].apply(lambda x: self.media_por_item[x])

        if not self.fitted_:
          self.labelencoder.fit(X[['ITEM UNIFICADO']])
          self.onehot.fit(X.drop(columns=['ITEM UNIFICADO', 'QTD']))
          self.scaler.fit(df)
          self.fitted_ = True

        return self

    def transform(self, X, y=None):

        from sklearn import set_config

        set_config(transform_output='pandas')

        if not self.fitted_:
          raise Exception('You must train dataset first')
        X = X.copy()
        X = X.reset_index(drop=True)

        numeric_cols = X.select_dtypes('number')
        itemOrdinal = pd.Series(self.labelencoder.transform(X[['ITEM UNIFICADO']]).reshape(-1)).to_frame('ITEM UNIFICADO')
        dummies = self.onehot.transform(X.drop(columns=['ITEM UNIFICADO', 'QTD']))
        df = pd.concat([itemOrdinal, numeric_cols, dummies], axis=1)
        df['Dias Atrasado_media_por_item'] = X['ITEM UNIFICADO'].apply(lambda x: self.media_por_item[x])
        df = self.scaler.transform(df)

        return df


class base_preditors(BaseEstimator, TransformerMixin):
    def __init__(self):
        import pandas as pd
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
        from sklearn.tree import DecisionTreeRegressor

        from xgboost import XGBRegressor


        # Modelos baseados em vizinhos
        self.KNN_tunned = KNeighborsRegressor(leaf_size=10, weights='distance', n_neighbors=10, p=5, algorithm='brute')

        # Modelos de árvore de decisão

        self.EXT = ExtraTreesRegressor(random_state=42)

        self.GBR = GradientBoostingRegressor(random_state=42)
        self.GBR_tunned = GradientBoostingRegressor(max_depth=9, min_samples_leaf=2, min_samples_split=4, n_estimators=300, random_state=42)

        self.RFR = RandomForestRegressor()
        self.RFR_tunned = RandomForestRegressor(max_features=None, n_estimators=10, random_state=42)

        self.XGB = XGBRegressor(random_state=42)
        self.XGB_tunned = XGBRegressor(learning_rate=0.1, max_depth=10, n_estimators=70, random_state=42)

        self.DTR = DecisionTreeRegressor(random_state=42)
        self.DTR_tunned = DecisionTreeRegressor(min_samples_split=5, max_features='sqrt', random_state=42)



    def fit(self, X, y=None):

        self.KNN_tunned.fit(X, y)

        self.EXT.fit(X, y)

        self.GBR.fit(X, y)
        self.GBR_tunned.fit(X, y)

        self.RFR.fit(X, y)
        self.RFR_tunned.fit(X, y)

        self.XGB.fit(X, y)
        self.XGB_tunned.fit(X, y)

        self.DTR.fit(X, y)
        self.DTR_tunned.fit(X, y)

        return self

    def transform(self, X, y=None):
        import pandas as pd

        df_base_predictions = pd.DataFrame()

        df_base_predictions['KNN_tunned'] = self.KNN_tunned.predict(X)

        df_base_predictions['EXT'] = self.EXT.predict(X)

        df_base_predictions['GBR'] = self.GBR.predict(X)
        df_base_predictions['GBR_tunned'] = self.GBR_tunned.predict(X)

        df_base_predictions['RFR'] = self.RFR.predict(X)
        df_base_predictions['RFR_tunned'] = self.RFR_tunned.predict(X)

        df_base_predictions['XGB'] = self.XGB.predict(X)
        df_base_predictions['XGB_tunned'] = self.XGB_tunned.predict(X)

        df_base_predictions['DTR'] = self.DTR.predict(X)
        df_base_predictions['DTR_tunned'] = self.DTR_tunned.predict(X)

        return df_base_predictions

class meta_preditors(BaseEstimator, TransformerMixin):
    def __init__(self):
        import pandas as pd
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.linear_model import LinearRegression, ElasticNet, Lasso, BayesianRidge, TheilSenRegressor, SGDRegressor
        from sklearn.svm import SVR
        from sklearn.ensemble import AdaBoostRegressor, ExtraTreesRegressor
        from sklearn.tree import DecisionTreeRegressor

        from lightgbm import LGBMRegressor

        # from catboost import CatBoostRegressor

        from sklearn.neural_network import MLPRegressor


        # Modelos baseado em vizinhos
        self.META_KNN_tunned = KNeighborsRegressor(n_neighbors=10, p=1)
        self.META_RN_tunned = RadiusNeighborsRegressor(leaf_size=15, p=5, weights='distance')

        # Modelos Lineares

        self.META_LR_tunned = LinearRegression(n_jobs=-1, fit_intercept=False, positive=True)

        self.META_EN = ElasticNet()
        self.META_EN_tunned = ElasticNet(fit_intercept=False, l1_ratio=0.9, positive=True, precompute=True, selection='random', random_state=42)

        self.META_LS = Lasso()

        self.META_BR_tunned = BayesianRidge(compute_score=True, max_iter=200, tol=0.0001)

        self.META_TS = TheilSenRegressor()

        self.META_SGD_tunned = SGDRegressor(alpha=0.007, loss='huber', max_iter=2000, penalty='l1', tol=0.01, random_state=42)



        # Support Vector Machines

        self.META_SVR = SVR()
        self.SVR_tunned = SVR(C=4, coef0=0.6, degree=7, kernel='poly')

        # Modelos de Árvore
        self.META_ADA_tunned = AdaBoostRegressor(learning_rate=0.01, random_state=42)

        self.META_EXT = ExtraTreesRegressor()
        self.META_EXT_tunned = ExtraTreesRegressor(max_depth=5, max_features='sqrt', min_samples_leaf=4, n_estimators=200)

        self.META_DTR = DecisionTreeRegressor()
        self.META_DTR_tunned = DecisionTreeRegressor(min_samples_split=5, max_features='sqrt', random_state=42)

        self.META_LGBM_tunned = LGBMRegressor(max_depth=5, objective='mae', random_state=42, verbose=-1)


        # Redes Neurais
        self.neural = MLPRegressor()


        # Lista com todos os modelos

        self.models = [self.META_KNN_tunned, self.META_LR_tunned, self.META_EN, self.META_EN_tunned,
                       self.META_LS, self.META_BR_tunned, self.META_TS, self.META_SGD_tunned, self.META_SVR,
                       self.SVR_tunned, self.META_ADA_tunned, self.META_EXT, self.META_EXT_tunned, self.META_DTR,
                       self.META_DTR_tunned, self.META_LGBM_tunned, self.neural
                       ]




    def fit(self, X=None, y=None):


        self.META_KNN_tunned.fit(X, y)

        self.META_LR_tunned.fit(X, y)

        self.META_EN.fit(X, y)
        self.META_EN_tunned.fit(X, y)

        self.META_LS.fit(X, y)

        self.META_BR_tunned.fit(X, y)

        self.META_TS.fit(X, y)

        self.META_SGD_tunned.fit(X, y)

        self.META_SVR.fit(X, y)

        self.META_ADA_tunned.fit(X, y)

        self.META_EXT.fit(X, y)
        self.META_EXT_tunned.fit(X, y)

        self.META_DTR.fit(X, y)
        self.META_DTR_tunned.fit(X, y)

        self.META_LGBM_tunned.fit(X, y)

        self.neural.fit(X, y)

        return self


    def transform(self, X, y=None):
        import pandas as pd

        df_meta_predictions = pd.DataFrame()

        df_meta_predictions['KNN_tunned'] = self.META_KNN_tunned.predict(X)

        df_meta_predictions['LR_tunned'] = self.META_LR_tunned.predict(X)

        df_meta_predictions['EN'] = self.META_EN.predict(X)
        df_meta_predictions['EN_tunned'] = self.META_EN_tunned.predict(X)

        df_meta_predictions['LS'] = self.META_LS.predict(X)

        df_meta_predictions['BR_tunned'] = self.META_BR_tunned.predict(X)

        df_meta_predictions['TS'] = self.META_TS.predict(X)

        df_meta_predictions['SGD_tunned'] = self.META_SGD_tunned.predict(X)

        df_meta_predictions['SVR'] = self.META_SVR.predict(X)

        df_meta_predictions['ADA_tunned'] = self.META_ADA_tunned.predict(X)

        df_meta_predictions['EXT'] = self.META_EXT.predict(X)
        df_meta_predictions['EXT_tunned'] = self.META_EXT_tunned.predict(X)

        df_meta_predictions['DTR'] = self.META_DTR.predict(X)
        df_meta_predictions['DTR_tunned'] = self.META_DTR_tunned.predict(X)

        df_meta_predictions['LGBM_tunned'] = self.META_LGBM_tunned.predict(X)

        df_meta_predictions['neural'] = self.neural.predict(X)

        df_meta_predictions = df_meta_predictions.apply(lambda row: row.apply(lambda col: round(col)), axis=1)

        return self.models, df_meta_predictions

# class final_preditors(BaseEstimator, TransformerMixin):


def create_pipe():
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import dill

    df_scaled = pd.read_excel('Data/processed/df_scaled.xlsx')
    df_prepared = pd.read_excel('Data/midprocess/df_prepared_fase1.xlsx')

    X = df_scaled
    y = df_prepared['Dias Atrasado']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline([('preprocess', pre_process()),
                    ('base_preditors', base_preditors()),
                    ('meta_preditors', meta_preditors())])
    
    pipe.fit(x_train, y_train)

    with open('Model/trained_pipeline.pkl', 'wb') as file:
        dill.dump(pipe, file)
    
    return pipe

if __name__ == '__main__':
    create_pipe()
    print('Pipeline criado com sucesso!')