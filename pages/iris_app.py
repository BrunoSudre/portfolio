import streamlit as st
import pandas as pd
import pickle


def main():
    st.title('Iris Classifier')
    st.sidebar.title('Parameters')

    sepal_length = st.sidebar.slider('Sepal Legnth (cm)', min_value=4.3, max_value=7.9, step=0.1)
    sepal_width = st.sidebar.slider('Sepal Width (cm)', min_value=2.0, max_value=4.4, step=0.1)
    petal_length = st.sidebar.slider('Petal Legnth (cm)', min_value=1.0, max_value=6.9, step=0.1)
    petal_width = st.sidebar.slider('Petal Width (cm)', min_value=0.1, max_value=2.5, step=0.1)

    columns = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    data = [[sepal_length, sepal_width, petal_length, petal_width]]
    df = pd.DataFrame(data=data, columns=columns)

    st.subheader('Original Data')
    st.write(df)

    st.subheader('Scaled Data')
    scaler = pickle.load(open('pages/iris/iris-scaler.pkl', 'rb'))
    df[columns] = scaler.transform(df)
    st.write(df)

    st.subheader('Classification')
    model = pickle.load(open('pages/iris/iris-model.pkl', 'rb'))
    predictions = model.predict(df)
    st.write(f":blue[**{predictions[0]}**]")
    st.image(f'pages/iris/{predictions[0]}.jpeg')


if __name__ == '__main__':
    st.set_page_config(
        page_title="Iris Classifier",
        page_icon="💐",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.collegelasalle.com',
            'Report a bug': "https://www.collegelasalle.com",
            'About': "# IRIS Classifier. A Neural Network classifier on IRIS dataset"
        }
    )
    main()
