import pandas as pd
import streamlit as st
from itertools import cycle
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler

def do_stuff_on_page_load():
    st.set_page_config(layout="wide", page_title="Sentimental Lyrics",
                      page_icon="🎵")
do_stuff_on_page_load()  

albums = pd.read_csv(f"data/MM_Albums_sentiment.csv")
songs = pd.read_csv(f"data/MM_AllSongs_sentiment.csv")
songs['release_date'] = pd.to_datetime(songs['release_date'])

album_info = songs[['album', 'release_date', 'art']].drop_duplicates().sort_values(by=['release_date']).reset_index(drop=True)
album_info['year'] = album_info['release_date'].dt.year
albums = albums.merge(album_info, on=['album'], how='left')
albums = albums.sort_values(by=['year'], ascending = True).reset_index(drop=True)

top_3 = albums.sort_values(by='Compound_Score', ascending=False).iloc[:3,:].reset_index(drop=True)
bottom_3 = albums.sort_values(by='Compound_Score', ascending=True).iloc[:3,:].reset_index(drop=True)

###############################
st.title("Mac Miller Sentiment Analysis")
st.divider()
###############################
idx = 0 
top_3_art = list(top_3['art'])
bottom_3_art = list(bottom_3['art'])
filler_ls = [" "]
filteredImages = top_3_art + filler_ls + bottom_3_art

top_3caption = list(top_3['album'])
bottom_3caption = list(bottom_3['album'])
caption = top_3caption + filler_ls + bottom_3caption

col1, col2 = st.columns([4,3])
col1.markdown("Top 3 Positive Albums")
col2.markdown("Top 3 Negative Albums")

cols = cycle(st.columns(7))
for idx, filteredImage in enumerate(filteredImages):
    col = next(cols)
    if idx == 3:
        pass
    elif idx > 3:
        col.image(filteredImage, caption=(f"#{idx-3} {caption[idx]}")) 
    else:
        col.image(filteredImage, caption=(f"#{idx+1} {caption[idx]}"))  
###############################
x = albums.copy()
x.set_index('year', inplace=True)
plot = x.copy()
plot.columns = plot.columns.str.replace('_', ' ')
plot = plot[['Compound Score','album']]
plot['Compound Score'] = plot['Compound Score'].astype(int)
fig = px.scatter(plot, title=None, trendline="lowess", text='album')

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
    yaxis=dict(showline=False, zeroline=False), 
    xaxis=dict(showgrid=False)  # Hide horizontal axis lines
)

st.subheader("Sentiment over Time")
st.plotly_chart(fig, theme="streamlit", use_container_width=True) 
####################################################
albums.set_index('album', inplace=True)
with st.expander("**By Album**", expanded=False):
    options = st.multiselect(
        'Pick some albums',
        albums.index.values,
        [])

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
    
####################################################
with st.expander("**Sentiment Metrics**", expanded=False):
    option = st.selectbox(
        'Pick a metric (compound is the best indicator of overall sentiment)',
        ('Compound Score', 'Positive Score', 'Negative Score',
        'Neutral Score', 'Variability'), index = 0)
    ####################################################
    plot = albums.copy()
    plot.columns = plot.columns.str.replace('_', ' ')
    plot = plot[[option]]
    fig = px.line(plot)
    
    fig.update_traces(
        showlegend=False#,
#         line=dict(color='blue')
    )

    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        yaxis=dict(showline=False, zeroline=False), 
        xaxis=dict(showgrid=False)  # Hide horizontal axis lines
    )

    # Use the Streamlit theme.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True) 

###############################
# Create a container for the content
with st.expander("**Discography**", expanded=False):
    idx = 0 
    filteredImages = list(album_info['art'])
    caption = list(album_info['year'])

    cols = cycle(st.columns(4))
    for idx, filteredImage in enumerate(filteredImages):
        next(cols).image(filteredImage, caption=caption[idx])

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
    
    