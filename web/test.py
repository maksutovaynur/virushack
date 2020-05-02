import streamlit as st
import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

w_complaints = st.text_input(
    label="Please describe your symptops here:",
    value="I have a headache, fewer and influenza", key="symptoms", type="default")


@st.cache
def get_symptoms(input_text):
    return [j for j in [i.strip().lower() for i in input_text.split()] if len(j) > 4]


symtoms = get_symptoms(w_complaints)

w_symtoms = st.multiselect(
    label='Select symptoms to find drug against',
    options=symtoms,
    default=symtoms)


@st.cache
def find_farmacies(symtoms_list):
    return [f"{randomword(random.randint(9, 18)).capitalize()} <some drug against '{s}'>" for s in symtoms_list*2]


farmacies = find_farmacies(w_symtoms)

w_farmacies = st.multiselect(
    label='Select drugs to buy',
    options=farmacies,
    default=farmacies)

w_button = st.button(
    label="Find a drugstore..."
)

if w_button:
    st.text("Вот тебе и список аптек")


