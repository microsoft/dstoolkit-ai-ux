from random import randint
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

pd.options.display.max_columns = 50
CHOSEN_DATASET = 'FD001'

def apply_RUL(df):
    df['RUL'] = df['time_in_cycles'].max() - df['time_in_cycles']
    return df
    

def load_data(data_directory):

    data_dictionnary = {}
    # columns name from readme
    # define metadata and feature
    operational_settings = ['op_setting_{}'.format(i + 1) for i in range (3)]
    sensor_columns = ['sensor_{}'.format(i + 1) for i in range(27)]
    features = operational_settings + sensor_columns
    metadata = ['engine_no', 'time_in_cycles']
    list_columns = metadata + features
    list_file_train = [x for x in sorted(os.listdir(data_directory)) if 'train' in x]
    # names of the datasets
    for file_train in list_file_train:
        data_set_name = file_train.replace('train_', '').replace('.txt', '')
        file_test = 'test_' + data_set_name + '.txt'
        rul_test = 'RUL_' + data_set_name + '.txt'   
        # dictionnaries with all datasets
        data_dictionnary[data_set_name] = {
            'df_train': pd.read_csv(os.path.join(data_directory, file_train), sep=' ', header=None, names=list_columns),
            'df_test': pd.read_csv(os.path.join(data_directory, file_test), sep=' ', header=None, names=list_columns),
            'RUL_test' :pd.read_csv(os.path.join(data_directory, rul_test), header=None, names=['RUL']),
        }
    return(data_dictionnary, features, metadata)

if __name__ == "__main__":

    st.title("Timeseries UX Demo")
    data_directory = os.path.join(os.getcwd(), 'predictive-maintenance')
    print(os.listdir(data_directory))
    data_dictionnary, features, metadata = load_data(data_directory)
    for data_set in data_dictionnary:
        data_dictionnary[data_set]['df_train'] = data_dictionnary[data_set]['df_train'].groupby('engine_no').apply(apply_RUL).reset_index(drop=True)
    df = data_dictionnary[CHOSEN_DATASET]['df_train'].copy()
    df_eval = data_dictionnary[CHOSEN_DATASET]['df_test'].copy()
    print(df.head())
    st.dataframe(df)

    df_plot = df.copy()
    # Sorty by engine number, time_in_cycles
    df_plot = df_plot.sort_values(metadata)
    #graph = sns.PairGrid(data=df_plot, x_vars="RUL", y_vars=features, hue="engine_no", height=4, aspect=6,)
    #graph = graph.map(plt.plot, alpha=0.5)
    #graph = graph.set(xlim=(df_plot['RUL'].max(),df_plot['RUL'].min()))
    #st.pyplot(graph)

    

    c = alt.Chart(df_plot).mark_line().encode(
        x='RUL',        
        y = alt.Y('sensor_14', 
        scale= alt.Scale(domain=(df_plot['sensor_14'].min(), df_plot['sensor_14'].max()))
        )
    )
    st.altair_chart(c, use_container_width=True)
