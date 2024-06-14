from streamlit_functions import *

# On load
do_stuff_on_page_load()  
albums, songs, top_3, bottom_3, albums_dalle, album_death_counter = import_data()
persona_file_paths, ai_img_file_paths = generate_file_paths()

# Choose the artist and change the title
# option = st.selectbox(label = "", options = (['Mac Miller']), index = 0)
option = 'Mac Miller'
st.header("Mac Miller's Musical Evolution")
st.write(f"A Data-Driven Exploration of Changing Sentiment over the Discography")
st.caption("Powered by GPT-3.5 and Streamlit")
# album_banner(albums)

# Show discography within a container
with st.expander("**Discography** *(click to expand)*", expanded=False):
    show_discography(albums)

# Show the top 3 and bottom 3 in one row
show_top_and_bottom_3(top_3, bottom_3)
st.markdown("""---""")
# Show analysis
# Death mention bar chart
death_mentions(albums, songs, album_death_counter)
st.write(" ")
st.write(" ")
st.markdown("""---""")
# Show sentiment change over time
col1, col2 = st.columns([1,1])

sentiment_change_over_time(albums, col1)
# Show sentiment change over albums
sentiment_change_over_albums(albums, col2)
st.write("In the early stages of his career, there's a surge of content characterized by positivity, but this takes a downturn around 2013. Subsequently, there's a decrease in content output, accompanied by a path towards stability. When you disregard the time aspect and explore album by album, the density of output is less clear but the pattern of starting off strong, encountering a decline, and then rebounding towards positivity becomes evident. It would be interesting to further explore the relationship between density of output in an artist's career and tone/quality/etc.")
st.write(" ")
st.markdown("""---""")
#     option = st.selectbox(label = "Pick an album:",
#         options = (albums['album'].unique()), index = 0)
#     by_album_chart(songs, option)

# Show Dall-E Generations
# with st.expander("**What does AI Think?**", expanded=True):
st.subheader("AI's Thoughts")
st.write("This section is more for fun than for actual insights. I experimented with some of the features of generative AI by asking what it thought about some lyrical analysis. First, I asked it to analyze the themes and suggest the best place to listen to the album based on the emotions evoked. Then, I used DALL-E to read the lyrics of the entire album and generate an image that encapsulates the themes, emotions, and tone of the record. *As a disclaimer: I firmly believe in and support human-generated art first and foremost. It is not acceptable for AI to profit from the work of unconsenting artists. This exploration is purely for study purposes and does not intend to make any broader statement.*")
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
    - Song by song insights by album
    - Single metric for unique word count
    ''')
    st.write("")
    
st.write(" ")

linkedin = "https://www.linkedin.com/in/scout-og/"
github = "https://github.com/scoutog"
    
st.markdown("My name is Scout. Check out my [LinkedIn](https://www.linkedin.com/in/scout-og/) and my [Github](https://github.com/scoutog)")
# st.link_button("My LinkedIn", linkedin)
# st.link_button("My GitHub", github)