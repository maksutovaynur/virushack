import streamlit as st
import random, string
import numpy as np
import pandas as pd
import pydeck as pdk


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


w_complaints = st.sidebar.text_input(
    label="Please describe your symptops here:",
    value="I have a headache, fewer and influenza", key="symptoms", type="default")


@st.cache
def get_symptoms(input_text):
    return [j for j in [i.strip().lower() for i in input_text.split()] if len(j) > 4]


symtoms = get_symptoms(w_complaints)

w_symtoms = st.sidebar.multiselect(
    label='Select symptoms to find drug against',
    options=symtoms,
    default=symtoms)


@st.cache
def find_farmacies(symtoms_list):
    return [f"{randomword(random.randint(9, 18)).capitalize()} <some drug against '{s}'>" for s in symtoms_list * 2]


farmacies = find_farmacies(w_symtoms)

w_farmacies = st.sidebar.multiselect(
    label='Select drugs to buy',
    options=farmacies,
    default=farmacies)

w_button = st.sidebar.button(
    label="Find a drugstore..."
)

if w_button:
    st.text("Вот тебе и список аптек")

map_data = pd.DataFrame(
    np.random.randn(150, 2) / [12, 12] + [55.750533, 37.616892],
    columns=['lat', 'lon'])

map_data['label'] = map_data['lat'].apply(lambda x: f"Аптека '{randomword(5).capitalize()}'")

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=55.750533,
        longitude=37.616892,
        zoom=11,
        pitch=50,
    ),
    layers=[
        # pdk.Layer(
        #     'HexagonLayer',
        #     data=map_data,
        #     get_position='[lon, lat]',
        #     radius=200,
        #     elevation_scale=4,
        #     elevation_range=[0, 1000],
        #     pickable=True,
        #     extruded=True,
        # ),
        pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=150,
            pickable=True,
            elevation_scale=2,
            extruded=True,
        ),
    ],
))

# st.map(map_data)
