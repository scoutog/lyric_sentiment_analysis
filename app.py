from streamlit_functions import *

# On load
do_stuff_on_page_load()  
albums, songs, top_3, bottom_3, albums_dalle, album_death_counter = import_data()
persona_file_paths, ai_img_file_paths = generate_file_paths()

# Choose the artist and change the title
# option = st.selectbox(label = "", options = (['Mac Miller']), index = 0)
option = 'Mac Miller'
st.title(f"{option} Sentiment Analysis")
# album_banner(albums)

# Show discography within a container
with st.expander("**Discography**", expanded=False):
    show_discography(albums)

# Show the top 3 and bottom 3 in one row
show_top_and_bottom_3(top_3, bottom_3)

# Show analysis
# Death mention bar chart
death_mentions(albums, songs, album_death_counter)

# Show sentiment change over time
sentiment_change_over_time(albums)

# Show sentiment change over albums
sentiment_change_over_albums(albums)

#     option = st.selectbox(label = "Pick an album:",
#         options = (albums['album'].unique()), index = 0)
#     by_album_chart(songs, option)

# Show Dall-E Generations
with st.expander("**What does AI Think?**", expanded=True):
    albums_and_Dalle(albums, albums_dalle, persona_file_paths, ai_img_file_paths)

# Generate wordclouds
# with st.expander("**WordClouds**", expanded=True):
#     option = st.selectbox(label = "Pick an album:",
#         options = (albums['album'].unique()), index = 7)
#     generate_wordcloud(albums, option)

# List enhancements
with st.expander("**Things I Want to Add**", expanded=False):
    st.markdown('''

    - Generalize to allow input of artist
    - Track the number of words per album
    - Single metric for unique word count
    ''')
    st.write("")