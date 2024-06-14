import pandas as pd
import streamlit as st
from itertools import cycle
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from PIL import Image

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
    
    dark = '''
    <style>
        .stApp {
        background-color: dark-gray;
        }
    </style>
    '''
    
    st.markdown(dark, unsafe_allow_html=True)
    #End
    
def generate_file_paths():
    persona_dir_path = f'{os.getcwd()}/data/persona_img/'
    ai_img_dir_path = f'{os.getcwd()}/data/ai_art/'

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
    
def extract_lyric_strings(strings):
    result = []
    for s in strings:
        index = s.lower().find("lyric")
        if index != -1:
            result.append(s[index+25:])  # Add 5 to skip "lyric"
    return result
    
def import_data():
    albums = pd.read_csv(f"data/MM_Albums_sentiment.csv")
    songs = pd.read_csv(f"data/MM_AllSongs_sentiment.csv")
    albums_dalle = pd.read_csv("data/MM_Albums_sentiment_with_DallE.csv")
    album_death_counter = pd.read_csv("data/album_death_counter.csv")

    albums['release_date'] = pd.to_datetime(albums['release_date'])
    songs['release_date'] = pd.to_datetime(songs['release_date'])

    albums['year'] = albums['release_date'].dt.year
    albums = albums.sort_values(by=['release_date'], ascending = True).reset_index(drop=True)

    top_3 = albums.sort_values(by='score', ascending=False).iloc[:3,:].reset_index(drop=True)
    bottom_3 = albums.sort_values(by='score', ascending=True).iloc[:3,:].reset_index(drop=True)
    
    return albums, songs, top_3, bottom_3, albums_dalle, album_death_counter

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
    col1.subheader("Albums with Most Positive Tone")
    col2.subheader("Albums with Most Negative Tone")

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

def sentiment_change_over_time(albums, col1):
    caption = '''Early in his career, there's a burst of content released marked by positivity, but it takes a nosedive towards the 2013. This is then followed by less decreased content output and a journey back to stability.'''

    x = albums.copy()
    x.set_index('year', inplace=True)
    plot = x.copy()
    plot = plot[['score','album']]
    plot['score'] = round(plot['score'].astype(float),1)
    fig = px.scatter(plot, title=None, text='album') # trendline="lowess", 

    fig.update_traces(
        textposition='bottom center',
        showlegend=False,
#         line=dict(color='green'),  #dict(color='rgba(255, 0, 0, 0.5)'
        marker=dict(color='cyan'),  # Set the color of scatter points
        hovertemplate='<b>%{text}</b><br>Score: %{y}<extra></extra>'  # Customize hover text
    )

    fig.update_layout(
        yaxis_title='Positivity Score',
        xaxis_title=None,
        title = "Sentiment Change over Time",
        yaxis=dict(showline=False, zeroline=False), 
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # st.markdown("<h3 style='text-align: center; '>Sentiment over Time</h3>", unsafe_allow_html=True)
    col1.plotly_chart(fig, theme="streamlit", use_container_width=True) 
#     col1.write(caption)
#     col1.markdown(f'<div style="text-align: justify;">{caption}</div>', unsafe_allow_html=True)
    #End

def sentiment_change_over_albums(albums, col2):
    caption = '''If you strip away the time factor and focus solely on each album, the pattern of starting strong, experiencing a decline, and then bouncing back towards positive vibes becomes even more evident.'''

    plot = albums.copy()
    plot = plot.sort_values(by=['release_date']).reset_index(drop=True)
    plot = plot.set_index('album')
    plot = plot[['score']]
    plot['score'] = round(plot['score'].astype(float),1)
    fig = px.line(plot, title=None)

    fig.update_traces(
        showlegend=False,
        line=dict(color='cyan')
    )

    fig.update_layout(
        yaxis_title='Sentiment',
        xaxis_title=None,
        title = 'Sentiment Change by Album',
        yaxis=dict(showline=False, zeroline=False), 
        yaxis_visible=False, #xaxis_showticklabels=False,
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # Use the Streamlit theme.
    col2.plotly_chart(fig, theme="streamlit", use_container_width=True) 
#     col2.write(caption)
#     col2.markdown(f'<div style="text-align: justify;">{caption}</div>', unsafe_allow_html=True)
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
#         plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    #End

def albums_and_Dalle(albums, albums_dalle, persona_file_paths, ai_img_file_paths):
    
    ai_img_file_paths = extract_lyric_strings(ai_img_file_paths)
    
#     cwd = os.getcwd()
#     ai_img_file_paths = [os.path.join(cwd, s) for s in ai_img_file_paths]
    
    column_sizing = [4,1,4,1,4,1,4]
    col0,col01, col1, col2, col3, col4, col5 = st.columns(column_sizing)
    
    col1.markdown(f'**<u><div style="text-align: center;">Dall-E Generation (based on Themes)</div></u>**', unsafe_allow_html=True)
    col0.markdown(f'**<u><div style="text-align: center;">Album Art</div></u>**', unsafe_allow_html=True)
    col3.markdown(f'**<u><div style="text-align: center;">Common Themes</div></u>**', unsafe_allow_html=True)
    col5.markdown(f'**<u><div style="text-align: center;">Ideal Listening Location</div></u>**', unsafe_allow_html=True)
#     col7.markdown(f'**<u><div style="text-align: center;">Where to Listen</div></u>**', unsafe_allow_html=True)

    for album in albums['album'].unique():
        col0,col01, col1, col2, col3, col4, col5 = st.columns(column_sizing)

        theme = albums_dalle[albums_dalle['album']==album]['album_theme'].item()
        theme = theme.replace(".","")
#         theme = theme.replace(",","\n")
        
        col3.write("")
        col3.write("")
        col3.write("")
        col3.write("")
        col3.write("")
        col3.write("")
        col3.markdown(f'<div style="text-align: center;">{theme}</div>', unsafe_allow_html=True)
        
        col0.image(albums[albums['album']==album]['art'].item(), caption = album)

        if album == 'GO:OD AM ':
            matching = [ai_img_file_paths[5]]
        else:
            matching = [s for s in ai_img_file_paths if album in s]

        if len(matching) != 1:
            matching = [matching[1]]
            
        matching = matching[0]

        image = Image.open(matching)
        col1.image(image, caption = album)

        listening_place = albums_dalle[albums_dalle['album']==album]['album_summary'].item()
        listening_place = listening_place.replace("The ideal place to listen to this record would be: ","")
        listening_place = listening_place.replace(".","")

        col5.write("")
        col5.write("")
        col5.write("")
        col5.write("")
        col5.write("")
        col5.write("")
        col5.markdown(f'<div style="text-align: center;">{listening_place}</div>', unsafe_allow_html=True)
        
def by_album_chart(songs, option):
#     option = 'K.I.D.S.'
    x = songs[songs['album'] == option].reset_index(drop=True)
    x.set_index('track_no', inplace=True)
    plot = x.copy()
    plot = plot[['score','title']]
    plot['score'] = round(plot['score'].astype(float),1)
    fig = px.scatter(plot, x=plot['title'], y=plot['score'], title=None) # trendline="lowess",

    fig.update_traces(
        textposition='bottom center',
        showlegend=False,
        line=dict(color='green'),  #dict(color='rgba(255, 0, 0, 0.5)'
        marker=dict(color='orange'),  # Set the color of scatter points
        hovertemplate='<b>%{text}</b><br>Score: %{y}<extra></extra>'  # Customize hover text
    )

    fig.update_layout(
        yaxis_title='Sentiment',
        xaxis_title=None,
        title = "Sentiment Change over Time",
        yaxis=dict(showline=False, zeroline=False), 
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # st.markdown("<h3 style='text-align: center; '>Sentiment over Time</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
    
####
def death_mentions(albums, songs, album_death_counter):
    caption = '''The evolution seen here is what sparked my interest in this analysis. Mac Miller initially entered the music scene with a cheerful, carefree demeanor and a love for life. However, as he matured, he openly grappled with existential challenges, including substance abuse, depression, and the search for meaning. We'll observe a notable shift in the tone of his music over time, particularly concerning discussions of mortality. Initially scarce, references to death gradually became a central theme. Yet, as we progress, you'll notice this trend wane, giving way to a resurgence of positivity in his work up until his death.'''
    
    num_songs = songs.groupby(['album']).agg(num_songs = ("track_no","max")).reset_index()
    death_adj = album_death_counter.merge(num_songs)
    death_adj['death_counter'] = death_adj['death_counter'] / death_adj['num_songs']
    album_death_counter = death_adj[['album','death_counter']].reset_index(drop=True)
    album_death_counter['death_counter'] = round(album_death_counter['death_counter'],1)
    
    
    x = album_death_counter.merge(albums[['album', 'release_date', 'score']], 
                                  on=['album']).sort_values(by= ['release_date']).reset_index(drop=True)
    
    x.set_index('album', inplace=True)
    plot = x.copy()
    fig = px.bar(plot, x=plot.index, y='death_counter', title="Average Death Mentions by Album", text=plot.index, 
                 hover_data=[plot.index, 'death_counter'], color='death_counter', color_continuous_scale=["green", "blue", "red"]) 

    fig.update_traces(
        textposition='outside',
        showlegend=False,
        hovertemplate='<b>%{text}</b><br>Death Mentions: %{y}<extra></extra>'  # Customize hover text
    )

    fig.update_layout(
        yaxis_title='Times Mentioned',
        yaxis_visible=False, xaxis_showticklabels=False,
        xaxis_title = None
#         title = "Sentiment Change over Time",
    )
    fig.update_coloraxes(showscale=False)

    # st.markdown("<h3 style='text-align: center; '>Sentiment over Time</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
    st.markdown(f'<div style="text-align: justify;">{caption}</div>', unsafe_allow_html=True)