import pandas as pd
import streamlit as st
from itertools import cycle
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def do_stuff_on_page_load():
    st.set_page_config(layout="wide", page_title="Sentimental Lyrics", #centered
                      page_icon="📻")
    st.markdown(
        """
        <style>
        img {cursor: pointer; transition: all .2s ease-in-out;}
        img:hover {transform: scale(1.1);}
        </style>
        """,unsafe_allow_html=True,
    )
    #End
    
def generate_file_paths():
    persona_dir_path = f'{os.getcwd()}/data/persona_img/'
    ai_img_dir_path = f'{os.getcwd()}/data/ai_img/'

    res = []
    for path in os.listdir(persona_dir_path):
        if os.path.isfile(os.path.join(persona_dir_path, path)):
            res.append(path)
    persona_file_paths = []

    for i in res:
        persona_file_paths.append(f"{persona_dir_path}{i}")

    res = []
    for path in os.listdir(ai_img_dir_path):
        if os.path.isfile(os.path.join(ai_img_dir_path, path)):
            res.append(path)
    ai_img_file_paths = []

    for i in res:
        ai_img_file_paths.append(f"{ai_img_dir_path}{i}")
        
    return persona_file_paths, ai_img_file_paths
    #End
    
def import_data():
    albums = pd.read_csv(f"data/MM_Albums_sentiment.csv")
    songs = pd.read_csv(f"data/MM_AllSongs_sentiment.csv")
    albums_dalle = pd.read_csv("data/MM_Albums_sentiment_with_DallE.csv")

    albums['release_date'] = pd.to_datetime(albums['release_date'])
    songs['release_date'] = pd.to_datetime(songs['release_date'])

    albums['year'] = albums['release_date'].dt.year
    albums = albums.sort_values(by=['release_date'], ascending = True).reset_index(drop=True)

    top_3 = albums.sort_values(by='score', ascending=False).iloc[:3,:].reset_index(drop=True)
    bottom_3 = albums.sort_values(by='score', ascending=True).iloc[:3,:].reset_index(drop=True)
    
    return albums, songs, top_3, bottom_3, albums_dalle

def show_discography(df):
    idx = 0 
    filteredImages = list(df['art'])
    caption = list(df['year'])

    cols = cycle(st.columns(4))
    for idx, filteredImage in enumerate(filteredImages):
        next(cols).image(filteredImage, caption=caption[idx])
    #End
    
def album_banner(albums):
    cols = cycle(st.columns(13))
    for album in albums['album'].unique():
        col = next(cols)
        col.image(albums[albums['album']==album]['art'].item())
    # end

def show_top_and_bottom_3(top_3, bottom_3):
    idx = 0 
    top_3_art = list(top_3['art'])
    bottom_3_art = list(bottom_3['art'])
    filler_ls = [" "]
    filteredImages = top_3_art + filler_ls + bottom_3_art

    top_3caption = list(top_3['album'])
    bottom_3caption = list(bottom_3['album'])
    caption = top_3caption + filler_ls + bottom_3caption

    col1, col2 = st.columns([4,3])
    col1.subheader("Top 3 Positive Albums")
    col2.subheader("Top 3 Negative Albums")

    cols = cycle(st.columns(7))
    for idx, filteredImage in enumerate(filteredImages):
        col = next(cols)
        if idx == 3:
            pass
        elif idx > 3:
            col.image(filteredImage, caption=(f"#{idx-3} {caption[idx]}")) 
        else:
            col.image(filteredImage, caption=(f"#{idx+1} {caption[idx]}"))  
    #End

def sentiment_change_over_time(albums):
    caption = '''You can see the density of content released in the early part of his career that begins with positivity and happiness but ends with negative sentiment. That is followed by decreased output and a progression back toward happiness.'''

    x = albums.copy()
    x.set_index('year', inplace=True)
    plot = x.copy()
    plot = plot[['score','album']]
    plot['score'] = round(plot['score'].astype(float),1)
    fig = px.scatter(plot, title=None, text='album', trendline = 'lowess') # trendline="lowess", 

    fig.update_traces(
        textposition='bottom center',
        showlegend=False,
        line=dict(color='green'),  #dict(color='rgba(255, 0, 0, 0.5)'
        marker=dict(color='orange'),  # Set the color of scatter points
        hovertemplate='<b>%{text}</b><br>Score: %{y}<extra></extra>'  # Customize hover text
    )

    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        title = "Sentiment Change over Time",
        yaxis=dict(showline=False, zeroline=False), 
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # st.markdown("<h3 style='text-align: center; '>Sentiment over Time</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
    st.write(caption)
    #End

def sentiment_change_over_albums(albums):
    caption = '''When you remove the temporal component and just look at album over album, the trend of starting high, dropping off, and progressing back toward good is even more clear.'''

    plot = albums.copy()
    plot = plot.sort_values(by=['release_date']).reset_index(drop=True)
    plot = plot.set_index('album')
    plot = plot[['score']]
    fig = px.line(plot)

    fig.update_traces(
        showlegend=False,
        line=dict(color='orange')
    )

    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        title = 'Sentiment Change by Album',
        yaxis=dict(showline=False, zeroline=False), 
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # Use the Streamlit theme.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
    st.write(caption)
    #End
    
def generate_wordcloud(albums, option):
    df = albums[albums['album'].isin([option])].reset_index(drop=True)

    # Create some sample text
    for index, row in df.iterrows():
        text = df.iloc[index,2]
        album_name = df.iloc[index,0]
        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)

        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    #End

def albums_and_Dalle(albums, persona_file_paths, ai_img_file_paths):
    col1, col2, col3, col4, col5 = st.columns([3,1,3,1,3])
    
    col1.subheader("Original Album Art")
    for album in albums['album'].unique():
        col1.image(albums[albums['album']==album]['art'].item(), caption = album)

    col2.write()
    
    col3.subheader("AI Personification")
    for album in albums['album'].unique():
        matching = [s for s in persona_file_paths if album in s]
        if len(matching) != 1:
            matching = matching[1]
        col3.image(matching, caption = album)
        
    col4.write()
    
    col5.subheader("AI Art")
    for album in albums['album'].unique():
        matching = [s for s in ai_img_file_paths if album in s]
        if len(matching) != 1:
            matching = matching[1]
        col5.image(matching, caption = album)