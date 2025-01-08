import pandas as pd

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler
from sklearn.base import BaseEstimator, TransformerMixin


class pre_process(BaseEstimator, TransformerMixin):
    
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

        df['Dias Atrasado_media_por_item'] = X['ITEM UNIFICADO'].apply(lambda x: self.media_por_item.get(x, 0))

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
        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.svm import SVR
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.ensemble import RandomForestRegressor

        self.DTR = DecisionTreeRegressor(random_state=42)
        self.DTR_tunned = DecisionTreeRegressor(min_samples_split=7)
        self.LR = LinearRegression()
        self.KNN = KNeighborsRegressor()
        self.KNN_tunned = KNeighborsRegressor(weights='distance', leaf_size=5, n_neighbors=11, p=4)
        self.SVR = SVR()
        self.GBR = GradientBoostingRegressor(random_state=42)
        self.GBR_tunned = GradientBoostingRegressor(max_depth=11, max_features='sqrt', min_samples_split=6, n_estimators=40)

    def fit(self, X, y=None):

        self.DTR.fit(X, y)
        self.DTR_tunned.fit(X, y)
        self.LR.fit(X, y)
        self.KNN.fit(X, y)
        self.KNN_tunned.fit(X, y)
        self.SVR.fit(X, y)
        self.GBR.fit(X, y)
        self.GBR_tunned.fit(X, y)
        return self

    def transform(self, X, y=None):
        
        df_base_predictions = pd.DataFrame()

        df_base_predictions['DTR'] = self.DTR.predict(X)
        df_base_predictions['DTR_tunned'] = self.DTR_tunned.predict(X)
        df_base_predictions['LR'] = self.LR.predict(X)
        df_base_predictions['KNN'] = self.KNN.predict(X)
        df_base_predictions['KNN_tunned'] = self.KNN_tunned.predict(X)
        df_base_predictions['SVR'] = self.SVR.predict(X)
        df_base_predictions['GBR'] = self.GBR.predict(X)
        df_base_predictions['GBR_tunned'] = self.GBR_tunned.predict(X)

        return df_base_predictions

class meta_preditors(BaseEstimator, TransformerMixin):
    def __init__(self):
        import pandas as pd
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import RandomForestRegressor

        self.META_KNN = KNeighborsRegressor()
        self.META_KNN_tunned = KNeighborsRegressor(algorithm='ball_tree', leaf_size=20, n_neighbors=7, p=1)
        self.META_LR_tunned = LinearRegression(n_jobs=-1, positive=True)
        self.META_LR = LinearRegression()
        self.META_GBR = GradientBoostingRegressor(random_state=42)
        self.META_GBR_tunned = GradientBoostingRegressor(max_features='sqrt', min_samples_split=10, min_samples_leaf=4, n_estimators=50)
        self.META_DTR = DecisionTreeRegressor()
        self.META_DTR_tunned = DecisionTreeRegressor(min_samples_split=5)
        self.META_RFR = RandomForestRegressor()
        self.META_RFR_tunned = RandomForestRegressor(max_features='sqrt', n_estimators=20, max_depth=5, min_samples_leaf=2, min_samples_split=5)

        self.models = [self.META_KNN, self.META_KNN_tunned, self.META_LR_tunned, self.META_LR, self.META_GBR, self.META_GBR_tunned, self.META_DTR, self.META_DTR_tunned, self.META_RFR, self.META_RFR_tunned]


    def fit(self, X=None, y=None):

        self.META_KNN.fit(X, y)
        self.META_KNN_tunned.fit(X, y)
        self.META_LR_tunned.fit(X, y)
        self.META_LR.fit(X, y)
        self.META_GBR.fit(X, y)
        self.META_GBR_tunned.fit(X, y)
        self.META_DTR.fit(X, y)
        self.META_DTR_tunned.fit(X, y)
        self.META_RFR.fit(X, y)
        self.META_RFR_tunned.fit(X, y)
        return self


    def transform(self, X, y=None):

        df_meta_predictions = pd.DataFrame()
        df_meta_predictions['KNN'] = self.META_KNN.predict(X)
        df_meta_predictions['KNN_tunned'] = self.META_KNN_tunned.predict(X)
        df_meta_predictions['LR_tunned'] = self.META_LR_tunned.predict(X)
        df_meta_predictions['LR'] = self.META_LR.predict(X)
        df_meta_predictions['GBR'] = self.META_GBR.predict(X)
        df_meta_predictions['GBR_tunned'] = self.META_GBR_tunned.predict(X)
        df_meta_predictions['DTR'] = self.META_DTR.predict(X)
        df_meta_predictions['DTR_tunned'] = self.META_DTR_tunned.predict(X)
        df_meta_predictions['RFR'] = self.META_RFR.predict(X)
        df_meta_predictions['RFR_tunned'] = self.META_RFR_tunned.predict(X)

        df_meta_predictions = df_meta_predictions.apply(lambda row: row.apply(lambda col: round(col)), axis=1)

        return models, df_meta_predictions


# class final_preditors(BaseEstimator, TransformerMixin):


def create_pipe():
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    import pandas as pd
    import cloudpickle

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
        cloudpickle.dump(pipe, file)
    
    return pipe

if __name__ == '__main__':
    create_pipe()
    print('Pipeline criado com sucesso!')