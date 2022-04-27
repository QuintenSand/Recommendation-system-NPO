import streamlit as st
from random import random
import pandas as pd

# Functions
def select_show(show_id):  
  st.session_state['index'] = show_id
  
def tile_item(column, item):
  with column:
    st.button('📺', key=random(), on_click=select_show, args=(item['index'], ))
    st.image(item['image'], use_column_width='always')
    st.caption(item['title'])

def recommendations(df):

  # check the number of items
  nbr_items = df.shape[0]

  if nbr_items != 0:    

    # create columns with the corresponding number of items
    columns = st.columns(nbr_items)

    # convert df rows to dict lists
    items = df.to_dict(orient='records')

    # apply tile_item to each column-item tuple (created with python 'zip')
    any(tile_item(x[0], x[1]) for x in zip(columns, items))

def diversity(df, categories):
    # select random number of categories of df
    randomlist = random.sample(range(0, 15), categories)

    # filter based on random numbers
    df = df[df['k_means'].isin(randomlist)]

    # calculate samples per categorie (variety)
    v = df.groupby(['k_means']).size()

    # total content (actually amount of rows)
    N = len(df)

    # calculate diversity
    diversity_index = (1 - sum(v*(v-1))/(N*(N-1)))

    # return diversity
    return diversity_index