import pandas as pd
import streamlit as st
import datetime as dt
from itertools import cycle
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

def do_stuff_on_page_load():
    st.set_page_config(layout="wide")
do_stuff_on_page_load()    

albums = pd.read_csv(f"data/MM_Albums_sentiment.csv")
songs = pd.read_csv(f"data/MM_AllSongs_sentiment.csv")
songs['release_date'] = pd.to_datetime(songs['release_date'])

album_info = songs[['album', 'release_date', 'art']].drop_duplicates().sort_values(by=['release_date']).reset_index(drop=True)
album_info['year'] = album_info['release_date'].dt.year
albums = albums.merge(album_info, on=['album'], how='left')
albums = albums.sort_values(by=['year'], ascending = True).reset_index(drop=True)

####################################################

# st.title(":red[Mac] :orange[Miller] :green[Sentiment] :blue[Analysis]")
st.title("Mac Miller Sentiment Analysis")
st.write("")

# Create a container for the content
with st.expander("**Discography**", expanded=True):
    idx = 0 
    filteredImages = list(album_info['art'])
    caption = list(album_info['year'])

    cols = cycle(st.columns(4))
    for idx, filteredImage in enumerate(filteredImages):
        next(cols).image(filteredImage, caption=caption[idx])#width=150

st.markdown(
    """
    <style>
    img {
        cursor: pointer;
        transition: all .2s ease-in-out;
    }
    img:hover {
        transform: scale(1.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
####################################################
with st.expander("**Sentiment Metrics**", expanded=False):
    option = st.selectbox(
        'Pick a metric (compound is the best indicator of overall sentiment)',
        ('Compound Score', 'Positive Score', 'Negative Score',
        'Neutral Score', 'Variability'), index = 0)
    ####################################################
    albums.set_index('album', inplace=True)
    plot = albums.copy()
    plot.columns = plot.columns.str.replace('_', ' ')
    plot = plot[[option]]
    fig = px.line(plot, title=option)
    fig.update_layout(yaxis_title=option)
    fig.update_layout(xaxis_title=None)

    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
####################################################
with st.expander("**By Album**", expanded=False):
    options = st.multiselect(
        'Pick some albums',
        albums.index.values,
        ['Faces'])
    ####################################################
    # Line plot using plotly express
    plot = albums.reset_index()
    plot = plot.drop(columns = ['release_date', 'art', 'year', 'Variability'])

    # Select only the quantitative columns for scaling
    columns_to_scale = ['Positive_Score', 'Negative_Score', 'Neutral_Score', 'Compound_Score']
    scaler = MinMaxScaler()

    # Fit and transform the selected columns
    plot[columns_to_scale] = scaler.fit_transform(plot[columns_to_scale])

    # Reshape DataFrame for plotly express
    df_long = pd.melt(plot, id_vars=['album'], var_name='Score Type', value_name='Score')

    if not options:
        pass
    else:
        df_long = df_long[df_long['album'].isin(options)]

    # Line plot using plotly express
    fig = px.line(df_long, x='Score Type', y='Score', color='album',
                  title='Normalized Sentiment Analysis Metrics for Albums',
                  labels={'Score Type': 'Sentiment Type', 'Score': 'Normalized Score'},
                  line_shape='linear')


    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 

