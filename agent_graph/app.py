import streamlit as st
from agent_graph.graph import com_agent

st.title("Sarthak's Communication Assistant")

employer_name = st.sidebar.text_input("Please put your name")
employer_id = st.sidebar.text_input("Please input your email id")