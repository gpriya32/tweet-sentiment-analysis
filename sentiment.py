import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.title("Sentiment Analysis of tweets about US Airlines")
st.sidebar.title("Sentiment Analysis of tweets about US Airlines")

st.markdown(" This app streamlit dashboard to analyze sentiments of tweets 🐦  --- by Priyanka Gupta")
st.sidebar.markdown(" This app streamlit dashboard to analyze sentiments of tweets 🐦 ")

DATA_URL = "Tweets.csv"

@st.cache(persist=True)

def load_data():
    data=pd.read_csv(DATA_URL)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data

data=load_data()

st.sidebar.subheader("Show random tweet")
random_tweet=st.sidebar.radio("Sentiment",("positive","negative","neutral"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweet by sentiment")
select=st.sidebar.selectbox("Visualization",["Histogram","Pie Chart"],key='1')

sentiment_count=data["airline_sentiment"].value_counts()
sentiment_count=pd.DataFrame({"Sentiment":sentiment_count.index,"Tweets":sentiment_count.values})


if not st.sidebar.checkbox("Hide",True):
    st.markdown("### Number of tweets by sentiment")
    if select == "Histogram":
        fig=px.bar(sentiment_count,x="Sentiment",y="Tweets",color= "Tweets",height=400)
        st.plotly_chart(fig)
    else:
        fig=px.pie(sentiment_count,values="Tweets",names="Sentiment")
        st.plotly_chart(fig)

# should have longitude and latitude without missing value_counts
# then u can use map
# st.map(data)


st.sidebar.subheader("When and where are users are tweeting from?")

hour=st.sidebar.slider("Hour of day",0,23)
modified_data=data[data["tweet_created"].dt.hour==hour]
if not st.sidebar.checkbox("Close",True,key='1'):
    st.markdown("### Tweets location based on time of day")
    st.markdown("%i Tweets between %i:00 to %i:00"%(len(modified_data),hour,(hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data",False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown airline tweets by sentiments")
choice=st.sidebar.multiselect("Pick airlines",["US Airways","United","American","Southwest","Delta","Virgin America"],key='0')

if len(choice)>0:
    choice_data = data[data.airline.isin(choice)]
    # using histogram to create count_plot
    fig_choice=px.histogram(choice_data,x="airline", y="airline_sentiment",histfunc="count",color="airline_sentiment",
    facet_col="airline_sentiment",labels={"airline_sentiment":"Tweets"},height=600,width=800)
    st.plotly_chart(fig_choice)

# word cloud
# to know the word occur mostly
st.sidebar.subheader("Word Cloud")
wors_sentiments=st.sidebar.radio("Display wordcloud for sentiment",("positive","negative","neutral"))

if not st.sidebar.checkbox("Close",True,key="2"):
    st.header("Word cloud for a particular sentiment "+ wors_sentiments)
     # to hide warning
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df =data[data["airline_sentiment"]==wors_sentiments]
    # string
    words=" ".join(df["text"])
    processed_words =" ".join([ word for word in words.split() if "http" not in word and not word.startswith("@") and word !="RT"])
    cloud=WordCloud(stopwords=STOPWORDS,background_color="white",height=640,width=800).generate(processed_words)
    # stopwords to remove commonly occuring processed_words
    # generate to make word cloud of words that are common in particular sentiments
    # using matplot to show image
    plt.imshow(cloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
   

