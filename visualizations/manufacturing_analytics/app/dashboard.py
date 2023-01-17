# Info
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import numpy as np

st.set_page_config(layout="wide")


@st.cache
def load_data(path=''):
    if path:
        return pd.read_csv(path)
    else:
        return pd.read_csv('./datasets/energy_consumption.csv')


@st.cache
def load_models():
    return joblib.load('./list_models.pkl')

@st.cache()
def generate_plan():
    import random
    import datetime


    starting_date = pd.Timestamp(datetime.datetime.now()).round('H')
    dates = pd.date_range(start=starting_date, end=starting_date+pd.Timedelta('5days'),freq='1H')

    df_plan = pd.DataFrame()
    for m in df['machine_id'].unique():
        select_sample = [random.choice([True, False]) for x in dates]
        
        df_sample = df.query(f'machine_id=="{m}"').sample(len(dates))
        df_sample['date'] = dates
        df_sample = df_sample.iloc[select_sample,:]

        model = dict_models[m]['model']
        df_sample['energy_prediction'] = model.predict(df_sample[["volume","weight","speed"]])
        df_plan = pd.concat([df_plan,df_sample])
    return df_plan 

@st.cache
def generate_default_values(df):
    return df.sample(1)[info].values.tolist()[0]

df = load_data()
df = df[['machine_id','energy','speed','volume','weight']].copy()
list_machines = df['machine_id'].unique()
list_machines = list(sorted(list_machines))

dict_models = load_models()
list_models = list(dict_models.keys())


st.write(
        """
        # Sustainable Manufacturing through AI
        
        This app shows how manufacturing companies can leverage AI to become more sustainable. 
        This use-case show how operation team can predict the energy consumption of their machines based on operational features.
        """
    )

st.write("")

st.sidebar.image("./microsoft.png", use_column_width=True) 

st.sidebar.title("Select View")


genre = st.sidebar.radio(
     "Wireframe",
     ('Analytics', 'AI Service', 'Data I/O'))



if genre == "Analytics":

    st.write("")
    st.write('# Analytics Wireframe')
    st.write("")
    st.dataframe(df)

    st.markdown("""---""")

    st.write('## Some interesting plots')

    m_id = st.selectbox('select machine',list_machines)
    
    st.write(f'### Showing plots for machine {m_id}')
    
    df_machine = df.query(f'machine_id =="{m_id}"')
    
   
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.markdown('#### Histogram')
        fig_hist = px.histogram(df_machine, x='energy',title='Energy Distribution')
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.markdown('#### Scatter')
        # fig_scatter = px.scatter(df_machine, x="speed", y='energy',title='Energy consumption based on machine speed')
        fig_scatter = px.scatter_matrix(df,
            dimensions=["speed", "weight", "volume"],
            color="energy",
            title="Feature interaction",
            ) 

        fig_scatter.update_traces(diagonal_visible=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col3:
        st.markdown('#### Correlation Map')
        corr = df_machine.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        fig_heatmap = go.Figure(data=go.Heatmap(z=corr.mask(mask),x=corr.columns,y=corr.columns,zmin=-1,zmax=1))
        fig_heatmap.update_xaxes(side="top")
        fig_heatmap.update_layout(
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_zeroline=False,
            yaxis_autorange='reversed',
            template='plotly_white'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)


    with col4:
        st.markdown('#### 3D Scatter')
        fig_3dscatter = px.scatter_3d(df_machine, x='speed', y='volume', z='weight',
              color='energy', size_max=18,#size='energy', 
              opacity=0.7)
        st.plotly_chart(fig_3dscatter, use_container_width=True)  

elif genre == 'AI Service':

    st.write("")
    st.write('# AI Service Wireframe')
    st.write("Predict the hourly total energy consumption for a week")


    df_plan = generate_plan()
    
    st.dataframe(df_plan)

    st.write('')
    st.write('Show 5-day plan')
    df_agg = df_plan.groupby('date').sum().reset_index()
    df_max = df_agg.loc[df_agg['energy_prediction'].idxmax()]
    
    max_energy = df_max['energy_prediction'].round(1)
    max_date = df_max.date
    fig = px.bar(df_plan, x="date", y="energy_prediction", color="machine_id", text_auto=True)
    
    fig.update_xaxes(rangeslider_visible=True)

    fig.add_shape(
        type='line',
        x0=df_plan['date'].min(),
        y0=max_energy,
        x1=df_plan['date'].max(),
        y1=max_energy,
        line=dict(color='Red'),
        name="test"
    )

    fig.add_trace(go.Scatter(
        x=[max_date, max_date],
        y=[max_energy],
        name = f"Highest Consumption: {max_energy} kWh"
    ))

    st.plotly_chart(fig, use_container_width=True)

    if st.button('Refresh plan'):
        st.legacy_caching.clear_cache()
    st.markdown("""---""")

    st.write('## Choose operation parameters')

    info = ["volume","weight","speed"]
    
    cols = st.columns(len(info)+1)
    option = cols[0].selectbox('Select machine',list_machines)
    default_val = generate_default_values(df)
    result_input = []
    for i in range(len(info)):
        user_input = cols[i+1].slider(
            label=info[i],
            value=int(default_val[i]),
            min_value=int(df[info[i]].min()),
            max_value=int(df[info[i]].max()),
            )
        result_input.append(float(user_input))
    
    
    prediction = 0.0
    if st.button('Calculate Energy Consumption'):
        if len(result_input) == len(info):
            data_prediction = pd.DataFrame([result_input], columns = info)
            model = dict_models[option]['model']
            prediction = model.predict(data_prediction)[0]

    st.metric("Energy Consumption (kWh)", np.round(prediction,1))

else:
    st.write("")
    st.write('# Data I/O Wireframe')
    st.write("Import your own data")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.dataframe(dataframe)