import os

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px


def transform_cyclical(value, count):
    return np.sin(2 * np.pi * value / count), np.cos(2 * np.pi * value / count)


def main():
    log_model = pickle.load(open('pages/bike/bike-model.pkl', 'rb'))
    no_log_model = pickle.load(open('pages/bike/bike-hour-model.pkl', 'rb'))
    scaler = pickle.load(open('pages/bike/bike-scaler.pkl', 'rb'))

    st.title('Bike Regressor :bike:')
    st.sidebar.title('Parameters')
    date = st.sidebar.date_input('Date')
    day = date.day
    month = date.month
    weekday = date.weekday()

    seasons_options = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season = st.sidebar.selectbox('Season', options=seasons_options.keys(), format_func=lambda x: seasons_options[x])

    weather_options = {1: 'Clear', 2: 'Mist', 3: 'Light snow/rain', 4: 'Heavy snow/rain'}
    weather = st.sidebar.selectbox('Weather', options=weather_options.keys(), format_func=lambda x: weather_options[x])

    holiday = int(st.sidebar.toggle('Holiday'))
    workingday = int(st.sidebar.toggle('Working Day'))

    temp = st.sidebar.slider('Temperature')
    atemp = st.sidebar.slider('Feels-Like Temperature')
    humidity = st.sidebar.slider('Humidity')
    windspeed = st.sidebar.slider('Windspeed')

    hours = np.arange(24)

    season_sin, season_cos = transform_cyclical(season, 4)
    day_sin, day_cos = transform_cyclical(day, 19)
    month_sin, month_cos = transform_cyclical(month, 12)
    weekday_sin, weekday_cos = transform_cyclical(weekday, 7)

    rows = []
    for hour in hours:
        hour_sin, hour_cos = transform_cyclical(hour, 24)

        row = [holiday, workingday, weather, temp, atemp, humidity, windspeed,
               season_sin, season_cos, month_sin, month_cos, day_sin, day_cos,
               hour_sin, hour_cos, weekday_sin, weekday_cos]
        rows.append(row)

    columns = ['holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity',
               'windspeed', 'season_sin', 'season_cos', 'month_sin', 'month_cos',
               'day_sin', 'day_cos', 'hour_sin', 'hour_cos', 'weekday_sin',
               'weekday_cos']

    df = pd.DataFrame(data=rows, columns=columns)

    features_to_scale = ["holiday", "workingday", "weather",
                         "temp", "atemp", "humidity", "windspeed"]
    df[features_to_scale] = scaler.transform(df[features_to_scale])

    st.subheader('Scaled Dataframe')
    st.write(df)

    st.subheader('Using Log Transformation')
    log_model_predictions = log_model.predict(df)
    log_model_predictions = np.expm1(log_model_predictions)

    fig = px.line(x=hours, y=log_model_predictions)
    fig.update_layout(
        xaxis={"dtick": 1, "title": "Hour"},
        yaxis={"title": "Count"}
    )
    st.plotly_chart(fig)

    st.subheader('Without Using Log Transformation')
    no_log_model_predictions = no_log_model.predict(df)

    fig = px.line(x=hours, y=no_log_model_predictions)
    fig.update_layout(
        xaxis={"dtick": 1, "title": "Hour"},
        yaxis={"title": "Count"}
    )
    st.plotly_chart(fig)


if __name__ == '__main__':
    st.set_page_config(
        page_title="Bike Regressor",
        page_icon=":bike:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.collegelasalle.com',
            'Report a bug': "https://www.collegelasalle.com",
            'About': "# BIKE Classifier. A Neural Network classifier on Bike dataset"
        }
    )
    main()
