import pandas as pd # pip install pandas
import streamlit as st
import template as t
import webbrowser
import os

# Configur page
st.set_page_config(page_title = "App",
page_icon = "📺",
layout = "wide")

# Create session
if 'index' not in st.session_state:
  st.session_state['index'] = 100

# load data
df = pd.read_csv("./recommendations/df.csv", sep = ",")
df_show = df[df['index'] == st.session_state['index']].iloc[0]

# ---- SIDEBAR ----
st.sidebar.image("npologo.png", use_column_width = True)
st.sidebar.header("Control diversity here:")
diversity_weight = st.sidebar.select_slider("Choose level of diversity", options=["Low diversity", "medium", "High diversity"])

# define fractions so that the diversity of data changes per sample group
if diversity_weight == "Low diversity":
    frac = 0.1
if diversity_weight == "medium":
    frac = 0.5
else:
    frac = 0.8

grouped = df.groupby('k_means')
df_sample = grouped.apply(lambda x: x.sample(frac=frac))

# ---- MAINPAGE ----
st.title("Recommender system")
# Show image with title and description
col1, col2 = st.columns(2)

image = df_show['image']
url = df_show['url']

with col1: 
  st.image(image)

with col2:
  st.header(df_show['title'])
  st.write(df_show['description'])
  if st.button("Watch now!"):
      webbrowser.open_new_tab(url)

# First recommendation
st.subheader('Recommendations based on ' + df_show['title'])
df_recommendations1 = df_sample[df_sample['k_means'] == df_show['k_means']].head(10)
t.recommendations(df_recommendations1)

st.markdown("##")

st.markdown("---")