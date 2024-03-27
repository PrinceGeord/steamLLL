import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt
from PIL import Image
from io import BytesIO
import requests
from wordcloud import WordCloud
from gameQueries import fetch_games
from SLFunc import load_game

df = pd.DataFrame(fetch_games(), columns=['appid', 'game_name', 'thumbnail'])

# page setup

st.set_page_config(page_title="DYGLLL", page_icon="❤️")
st.title("Does Your Game Live Laugh Love?")

# search feature


def set_game(appid):
    st.session_state['game_selected'] = appid
    st.session_state.search = ''

if 'search' not in st.session_state:
    st.session_state.search = ''
if 'game_selected' not in st.session_state:
    st.session_state.game_selected = ''

def submit():
    st.session_state.search = st.session_state.searchText
    st.session_state.searchText = ''
    st.session_state.game_selected = ''

def change_feedback():
     if st.session_state.feedback_toggle == False:
          st.session_state.feedback_toggle = True
     else:
          st.session_state.feedback_toggle = False

st.text_input("Search bar",placeholder="Search for a game title", key='searchText', on_change=submit, label_visibility="hidden")

game_title_location = st.empty()
imageLocation = st.empty()


if st.session_state.search != '':
    m1 = df["game_name"].str.contains(st.session_state.search)
    df_search = df[m1]
    N_cards_per_row = 1
    default_thumbnail = np.array(Image.open(BytesIO(requests.get("https://upload.wikimedia.org/wikipedia/commons/c/c1/Steam_Logo.png").content)))
    for n_row, row in df_search.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i ==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[n_row%N_cards_per_row]:
          if row['thumbnail'] is None:
               thumbnail = default_thumbnail
          else:
               thumbnail = np.array(Image.open(BytesIO(requests.get(row['thumbnail']).content)))
          st.image(thumbnail, width=200)
          st.caption(f"steam_app_id: {row['appid']}")
          st.markdown(f"**{row['game_name'].strip()}**")
          st.button('search', key={row['appid']}, help=None, on_click=set_game, args= (row['appid'],), kwargs=None, type="secondary", disabled=False, use_container_width=False)


if 'feedback_toggle' not in st.session_state :
          st.session_state.feedback_toggle = True

if st.session_state.game_selected !='':
     selected_game = load_game(st.session_state['game_selected'])
     game_title_location.header(selected_game['info'][1], divider='rainbow')
     if selected_game['info'][7] is not None:
          imageLocation.image(np.array(Image.open(BytesIO(requests.get(selected_game['info'][7]).content))))

     if st.session_state.feedback_toggle == False:
          st.session_state['keywords'] = 'n_keywords'
          st.button("Click for Positive Feedback", on_click=change_feedback, args=None)
     if st.session_state.feedback_toggle == True:
          st.session_state['keywords'] = 'p_keywords'
          st.button("Click for Negative Feedback", on_click=change_feedback, args=None)
     if selected_game['info'][3] == 'game':
          wcf_input = selected_game[st.session_state.keywords]
          p_response = requests.get("https://raw.githubusercontent.com/R-CoderDotCom/samples/main/wordcloud-mask.jpg")
          p_mask = np.array(Image.open(BytesIO(p_response.content)))
          n_response = requests.get("https://banner2.cleanpng.com/20190419/gjs/kisspng-computer-icons-portable-network-graphics-emoticon-facing-people-icons-2138-free-vector-icons-pa-5cba908ad45c75.5210478015557305708698.jpg")
          n_mask = np.array(Image.open(BytesIO(n_response.content)))
          if st.session_state.keywords == 'p_keywords':
               wcmask = p_mask
          else:
               wcmask = n_mask

               # WordCloud
          wcf = WordCloud(background_color= "rgba(255,255,255,0)", mode='RGBA', colormap = "Reds", max_words = 50, mask = wcmask,  repeat = True, width=400, height=400).fit_words(wcf_input)
          wcffig, ax = plt.subplots(figsize = (20,20))
          ax.imshow(wcf, interpolation='bilinear')
          plt.axis("off")
          plt.tight_layout(pad=0)
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
                    y=alt.Y("index", type="nominal", title="").sort('-x'),
                    color=alt.Color("index", scale=alt.Scale(
                         domain=data.sort_values(['value'])['index'].tolist(),
                         range=['navy', 'navy', 'darkgreen', 'darkgreen', "goldenrod",'goldenrod', "darkorange",'darkorange', "firebrick",'firebrick']
                    ), type="nominal", title="red", legend=None),
                    order = alt.Order("variable", sort="descending"),
               ).transform_window(
                    rank='rank(value)',
                    sort=[alt.SortField('value', order='descending')]
               ).transform_filter(
                    alt.datum.rank < 10
               )
               )

          st.altair_chart(chart, use_container_width=True)
     else:
          st.write(f'App currently only reviews video games - this is a {selected_game["info"][3]}')