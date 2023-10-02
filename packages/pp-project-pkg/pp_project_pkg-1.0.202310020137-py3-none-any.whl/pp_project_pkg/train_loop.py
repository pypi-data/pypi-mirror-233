"""
Module for training linear model
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import wml.visionml as wv

__all__ = ['linear_train','train_model','train_randomforest','plot_res','outliers','get_model']


class get_model():
    def __init__(self,start_date='2023-08-01',end_date='2023-08-30',test_start_date='2023-09-01',test_end_date='2023-09-07'):
        self.sd = start_date
        self.ed = end_date
        self.test_sd = test_start_date
        self.test_end = test_end_date
        self.data = wv.read_sql('select * from pp_tables.waldorf_waste_data')
        
    def remove_zeros(self,data):
        data = (data[data['actual_consumption']!=0].dropna()).reset_index()
        return data    
    
    def train_data(self):
        train_data = (self.data[(self.data['date']<=self.ed) & (self.data['date']>=self.sd)]).reset_index()
        print('Length of train_data before removing zero values : {}'.format(str(len(train_data))))
        train_data = self.remove_zeros(train_data)
        print('Length of train_data after removing zero values : {}'.format(str(len(train_data))))
        self.train_data = train_data
        return train_data
    
    def get_test_data(self):
        test_data = (self.data[(self.data['date']<=self.test_end) & (self.data['date']>=self.test_sd)]).reset_index()
        print('Length of test_data before removing zero values : {}'.format(str(len(test_data))))
        test_data = self.remove_zeros(test_data)
        print('Length of test_data after removing zero values : {}'.format(str(len(test_data))))
        self.test_data = test_data
        return test_data
    
    def actual_num(self,list_covers):
        return sum(list_covers)/len(list_covers)
    
    def get_unqiue_taxcodes(self,data):
        unique_taxcode= list(pd.unique(data['taxonomy_code']))
        self.unique_taxcode = unique_taxcode
        return unique_taxcode
        
    def get_final_weight(self,data,taxcode='xyz'):
        data_temp = data[data['taxonomy_code']==taxcode]
        weight_res = sum(data_temp['consumption_per_cover'])/len(data_temp)
        weight_res = weight_res/1000.0
        weight_res = '%.5f'%(weight_res)
        return weight_res
    
    def get_res_dict(self):
        self.get_unqiue_taxcodes(self.train_data)
        self.dict_final = {self.unique_taxcode[i]:self.get_final_weight(self.train_data,taxcode=self.unique_taxcode[i]) for i in range(len(self.unique_taxcode))}
        return self.dict_final
    
    def final_test_check(self):
        self.final_test_val = {}
        self.final_res_val ={}
        self.get_res_dict()
        for i in range(len(self.test_data)):
            test_val = (sum(self.test_data[self.test_data['taxonomy_code']==self.test_data['taxonomy_code'][i]]['consumption_per_cover'])
                        /(len(self.test_data[self.test_data['taxonomy_code']==self.test_data['taxonomy_code'][i]])))
            self.final_test_val[self.test_data['taxonomy_code'][i]]=test_val
            self.final_res_val[self.test_data['taxonomy_code'][i]] = abs(test_val-self.dict_final[self.test_data['taxonomy_code'][i]])
        self.total_res_total = sum(self.final_res_val.values())
        self.total_res = sum(self.final_res_val.values())/len(self.final_res_val)
        
    def get_weight_with_conditions(self,min_value = 15,mean_multiplier=2):
        self.final_weight ={}
        for i in range(len(self.test_data)):
            all_val = self.test_data[self.test_data['taxonomy_code']==self.test_data['taxonomy_code'][i]]
            test_len = len(all_val)
            if test_len<min_value:
                print(f"number of events for {self.test_data['taxonomy_code'][i]} less than {min_value}")
                self.final_weight[self.test_data['taxonomy_code'][i]]=None
            else:    
                all_val.loc[all_val['consumption_per_cover'] >= (all_val.mean() * mean_multiplier), 'consumption_per_cover'] = 0 
                test_final_sum = sum(all_val['consumption_per_cover'])/len(test_len)
                self.final_weight[self.test_data['taxonomy_code'][i]]=test_final_sum       

def linear_train(data,input_cols=['actual_covers'],output_cols=['actual_consumption'],test_case=[130],logger=None):
    """
    Linear train a model on the data with input_cols and output_cols
    Args:
        data : pd.DataFrame
        input_cols : list of input columns
        output_cols : list of output columns
    Returns:
        model : sklearn model object
    """
    from sklearn.linear_model import LinearRegression

    # create the input and output variables for the model
    
    if logger:
        logger.info("Training linear model")
        logger.info("Input columns : {}".format(input_cols))
        logger.info("Output columns : {}".format(output_cols))
    X = data[input_cols]
    y = data[output_cols]

    if logger:
        logger.info("training on events : {}".format(len(X)))

    ##remove zeros from the data
    X = X[X!=0].dropna()    
    y= y[y.index.isin(X.index)]

    if logger:
        logger.info("training on events after removing zeros: {}".format(len(X)))
    
    if len(X) <= 3:
        return None
    
    # convert the lists to numpy arrays
    dp1 = np.array(X)
    dp1 = np.reshape(dp1,[len(X),1])

    dp2 = np.array(y)
    dp2 = np.reshape(dp2,[len(y),1])

    # Splitting data into training and test sets (keeping the latest 10% for evaluation)
    train_size = int(0.9 * len(dp1))
    X_train, X_test = dp1[:train_size], dp1[train_size:]
    y_train, y_test = dp2[:train_size], dp2[train_size:]


    # create a linear regression model and fit it to the data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicting and evaluating
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred) 
    r2 = r2_score(y_test, y_pred)

    if logger:
        logger.info('Mean squared error: {}'.format(mse))
        logger.info('Mean absolute error: {}'.format(mae))
        logger.info('R2 score: {}'.format(r2))   

    # perform inference to predict actual_production based on no_of_covers
    if test_case:
        input_data = [test_case]
        predicted_output = model.predict(input_data)
        if logger:
            logger.info("Predicted output for a test case: {}".format(predicted_output))
    return model



def train_model(data,logger=None):
    """
    Trains a linear model on the data and upload the model to the cloud with parameters
    
    Args:
        data: pd.DataFrame
        logger: logger object
    Returns:
        None
    """
    # Reading data
    data = pd.read_csv('data.csv')

    # Selecting relevant input features
    X = data[['actual_covers', 'food_item_consumed', 'nationalities', 'day_of_the_week']]
    y = data[['predicted_covers', 'food_item_waste']]

    # Encoding categorical features (nationalities, sex, day_of_the_week)
    categorical_features = ['nationalities', 'day_of_the_week']
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', one_hot_encoder, categorical_features)
        ],
        remainder='passthrough'
    )

    # Creating a Linear Regression model
    model = LinearRegression()

    # Creating a pipeline with the preprocessor and the model
    pipeline_linear = Pipeline(steps=[('preprocessor', preprocessor),
                               ('model', model)])

    # Splitting data into training and test sets (keeping the latest 10% for evaluation)
    train_size = int(0.9 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Training the model
    pipeline_linear.fit(X_train, y_train)

    # Predicting and evaluating
    y_pred = pipeline_linear.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred) 
    r2 = r2_score(y_test, y_pred)

    if logger:
        logger.info('Mean squared error: {}'.format(mse))
        logger.info('Mean absolute error: {}'.format(mae))
        logger.info('R2 score: {}'.format(r2))   

    # Check feature importances
    importances = model.feature_importances_ 
    feature_df = pd.DataFrame({'Feature': list(X), 'Importance': importances})
    feature_df = feature_df.sort_values('Importance', ascending=False)


def train_randomforest(data,logger=None):
    """
    Train a random forest model on the data and upload the model to the cloud with parameters

    Args:
        data: pd.DataFrame
        logger: logger object
    Returns:
        None
    """
    data = pd.read_csv('data.csv')

    # Selecting relevant input features
    X = data[['actual_covers', 'food_item_consumed', 'nationalities', 'sex', 'day_of_the_week']]
    y = data[['predicted_covers', 'food_item_waste']]

    # Encoding categorical features (nationalities, sex, day_of_the_week)
    categorical_features = ['nationalities', 'sex', 'day_of_the_week']
    one_hot_encoder = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', one_hot_encoder, categorical_features)
        ],
        remainder='passthrough'
    )

    # Splitting data into training and test sets (keeping the latest 10% for evaluation)
    train_size = int(0.9 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    rf_model = RandomForestRegressor(n_estimators=100) 
    pipeline_randomforest = Pipeline(steps=[('preprocessor', preprocessor), 
                               ('model', rf_model)])
    pipeline_randomforest.fit(X_train, y_train) 
    y_pred = pipeline_randomforest.predict(X_test)
 
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred) 
    r2 = r2_score(y_test, y_pred)    

    if logger:
        logger.info('Mean squared error: {}'.format(mse))
        logger.info('Mean absolute error: {}'.format(mae))
        logger.info('R2 score: {}'.format(r2))   
            
    # Check feature importances
    importances = rf_model.feature_importances_ 
    feature_df = pd.DataFrame({'Feature': list(X), 'Importance': importances})
    feature_df = feature_df.sort_values('Importance', ascending=False)



def plot_res(y_test, y_pred):
    """
    Plots the results of the model
    
    Args:
        y_test: pd.DataFrame
        y_pred: pd.DataFrame
    Returns:
        None
    """
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()], [y_pred.min(), y_pred.max()], '--r')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.show()

    
def outliers(data,threshold_val=2.0):
    """
    Detect outliers in the file
    
    Args:
        data: pd.DataFrame
        threshold_val: float
    Returns:
        pd.DataFrame
    """
    
    avg_events = data['events'].mean()
    
    # Calculate the range of events
    range_events = data['events'].max() - data['events'].min()

    # Define a threshold value for outliers
    threshold = threshold_val * range_events

    # Identify the outliers based on the threshold value
    outliers = data[data['events'] > avg_events + threshold]

    return outliers