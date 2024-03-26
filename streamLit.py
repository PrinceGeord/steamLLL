import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
from io import BytesIO
import requests
from wordcloud import WordCloud
from gameQueries import fetch_games, fetch_game_info
from insertGames import insert_game_details
from keyword_extract import get_keywords


df = pd.DataFrame(fetch_games(), columns=['appid', 'game_name'])

def load_game(appid):
     info = fetch_game_info(appid)
     if info[2] == None:
          insert_game_details(appid)
          info = fetch_game_info(appid)
     if info[8] == None:
          p_keywords = get_keywords(appid, True).to_dict(orient='records')
          n_keywords = get_keywords(appid, False).to_dict(orient='records')
     else:
          p_keywords = info[7]
          n_keywords = info[7]
     return {'info': info, 'p_keywords': p_keywords, 'n_keywords': n_keywords }



# page setup

st.set_page_config(page_title="DYGLLL", page_icon="❤️")
st.title("Does Your Game Live Laugh Love?")



# search feature

text_search = st.text_input("Search for games", value="")
m1 = df["game_name"].str.contains(text_search)
df_search = df[m1]
N_cards_per_row = 1

if text_search:
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i ==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")

        with cols[n_row%N_cards_per_row]:
            st.caption(f"{row['appid']} - {row['game_name'].strip()}")
            st.markdown(f"**{row['game_name'].strip()}**")
            st.button('search', key={row['appid']}, help=None, on_click=None, args=None, kwargs=None, type="secondary", disabled=False, use_container_width=False)

# wordcloud - idea. Have a postive and a negative wordcloud image shaped to an emoji (e.g. postive is heart shape, negative is a frowney face)

game_info = load_game(2357570)
raw_wcf_input = game_info['p_keywords']
wcf_input = {}


for word in raw_wcf_input:
     wcf_input.update({word['keywords']: word['score']})
response = requests.get("https://raw.githubusercontent.com/R-CoderDotCom/samples/main/wordcloud-mask.jpg")
p_mask = np.array(Image.open(BytesIO(response.content)))
wcf = WordCloud(background_color= "azure", colormap = "Reds", max_words = 50, mask = p_mask, contour_width = 1, contour_color = 'red').fit_words(wcf_input)
wcffig, ax = plt.subplots(figsize = (20,20))
ax.imshow(wcf, interpolation='bilinear')
plt.axis("off")
st.pyplot(wcffig)
# barplot

chart_data = pd.DataFrame(
     wcf_input.values(),
     index=wcf_input.keys()
)
data = pd.melt(chart_data.reset_index(), id_vars=["index"])

chart = (
     alt.Chart(data).mark_bar().encode(
          x=alt.X("value", type="quantitative", title="", axis=alt.Axis(labels=False)),
          y=alt.Y("index", type="nominal", title=""),
          color=alt.Color("variable", type="nominal", title="red", legend=None),
          order = alt.Order("variable", sort="descending"),
     )
     )

st.altair_chart(chart, use_container_width=True)