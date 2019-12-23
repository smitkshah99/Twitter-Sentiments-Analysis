import pandas as pd
import streamlit as st
import re
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
import tweepy
st.title('Twitter Sentiment Analysis')
navigation=st.sidebar.selectbox(    'Select You Option',
     ['Home','Crime Check'])




consumer_key=''
consumer_secret=''

access_token=''
access_token_secret='XAx3iFWz1PJVrdAB5JoKcHxzxf0KdufMsNj4QRZzawVYg'

auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)  

def twitter():
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret) 
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit = True)  
    return api  

if(navigation=='Home'):
    url = st.text_input('Enter Keyword')
    name = st.text_input('Enter Your UserName')


    if (url):
        count = st.selectbox(
        'Number of Counts',
         [50,40,30,20])
        'You selected: ', count
        st.write('The Entered keywork : ', url)
        api=tweepy.API(auth)
        tot=0
        i=0

        # In[18]:
        
        public_tweets=api.search(url,count=count,lang='en')

        df = pd.DataFrame([tweets.text for tweets in public_tweets], columns=['Tweets'])

    #, RT, @mentions
        def clean(x):
             x = re.sub(r"@[A-Za-z0–9]+", '', x)
             x = re.sub(r'^RT[\s]+', '', x)
             x = re.sub(r'https?:\/\/.*[\r\n]*', '', x)
             x = re.sub(r'#', '', x)
             return x
        df['Tweets'] = df['Tweets'].apply(clean)

        polarity = lambda x: TextBlob(x).sentiment.polarity
        subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
        df['polarity'] = df['Tweets'].apply(polarity)
        df['subjectivity'] = df['Tweets'].apply(subjectivity)
        pos=(df.polarity>0).sum()
        neg=(df.polarity<0).sum()
        neu=(df.polarity==0).sum()
        totalpol=df['polarity'].mean()
        if (totalpol>0):
            st.write(pos,' out of ',count,' have Positive Sentiment')
        if (totalpol==0):
            st.write(neu,' out of ',count,' have Neutral Sentiment')
        if (totalpol<0):
            st.write(neg,' out of ',count,' have Negative Sentiment')
        # if st.checkbox('Show Tweets'):


        labels='Positive','Negative','Neutral'
        sizes=[pos,neg,neu]
        fig1,ax1=plt.subplots()
        ax1.pie(sizes,explode=None,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
        ax1.axis('equal')
        st.pyplot()

        check1=st.checkbox('Positive')
        check2=st.checkbox('Neutral')
        check3=st.checkbox('Negative')
        
        
        if (check1):
            st.subheader('Positive Tweets :')
            for i in range(len(df.values)):
                if df.polarity[i]>0:
                    st.write(i,' ',df.Tweets[i])
        if (check2):
            st.subheader('Neutral Tweets :')
            for i in range(len(df.values)):
                if df.polarity[i]==0:
                    st.write(i,' ',df.Tweets[i])
        if (check3):
            st.subheader('Negative Tweets :')
            for i in range(len(df.values)):
                if df.polarity[i]<0:
                    st.write(i,' ',df.Tweets[i])
        
        #     for tweet in range(count-1):


    if (name):
        st.write('The Entered UserName : ', name)
        count2=200

        tw = twitter()
        search = tw.user_timeline(screen_name=name, count = count2, lang ="en")
        def clean(x):
             x = re.sub(r'^RT[\s]+', '', x)
             x = re.sub(r'https?:\/\/.*[\r\n]*', '', x)
             x = re.sub(r'#', '', x)
             x = re.sub(r'@[A-Za-z0–9]+', '', x) 
             return x
        df = pd.DataFrame([tweets.text for tweets in search], columns=['Tweets'])
        df['Tweets'] = df['Tweets'].apply(clean)
        polarity = lambda x: TextBlob(x).sentiment.polarity
        subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
        df['polarity'] = df['Tweets'].apply(polarity)
        df['subjectivity'] = df['Tweets'].apply(subjectivity)
        pos=(df.polarity>0).sum()
        neg=(df.polarity<0).sum()
        neu=(df.polarity==0).sum()

        totalpol=df['polarity'].mean()
        if (totalpol>0):
            st.write(pos,' out of ',count2,' have Positive Sentiment')
        if (totalpol==0):
            st.write(neu,' out of ',count2,' have Neutral Sentiment')
        if (totalpol<0):
            st.write(neg,' out of ',count2,' have Negative Sentiment')
        # if st.checkbox('Show Tweets'):


        labels='Positive','Negative','Neutral'
        sizes=[pos,neg,neu]
        fig1,ax1=plt.subplots()
        ax1.pie(sizes,explode=None,labels=labels,autopct='%1.1f%%',shadow=True,startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        fig2,ax2=plt.subplots()
        plt.rcParams['figure.figsize'] = [10, 8]
        for index, Tweets in enumerate(df.index):
         x = df.polarity.loc[Tweets]
         y = df.subjectivity.loc[Tweets]
         plt.scatter(x, y, color='Red')
        
         
        plt.title('Sentiment Analysis', fontsize = 20)
        plt.xlabel('← Negative — — — — — — Positive →', fontsize=15)
        plt.ylabel('← Facts — — — — — — — Opinions →', fontsize=15)
        st.pyplot(fig2)
        st.write('\n')
        st.write(df)

if(navigation=='Crime Check'):
    keyw = st.text_input('Enter Keyword To Search')
    loc = st.selectbox(
        'Select Location',
         ['ALL LOCATION','INDIA','USA','PAKISTAN'])

    api=tweepy.API(auth)  
    if(keyw):
        public_tweets=api.search(keyw,count=100,lang='en')
    
        df1 = pd.DataFrame([tweets.text for tweets in public_tweets], columns=['Tweets'])
        df1['Location'] = [tweets.user.location for tweets in public_tweets]
        df1['UserName'] = [tweets.user.screen_name for tweets in public_tweets]

        polarity = lambda x: TextBlob(x).sentiment.polarity
        subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
        df1['polarity'] = df1['Tweets'].apply(polarity)
        df1['subjectivity'] = df1['Tweets'].apply(subjectivity)
        st.subheader('OFFENSIVE TWEITTER ACCOUNT AND THEIR LOCATIONS ')
        if(loc=='ALL LOCATION'):
            st.write(df1[['UserName','Location']])
        if(loc=='INDIA'):
            st.write(df1[df1.Location.str.contains('India') | df1.Location.str.contains('भारत')| df1.Location.str.contains('Banglore') | df1.Location.str.contains('New Delhi') ])
        if(loc=='PAKISTAN'):
            st.write(df1[df1.Location.str.contains('Pakistan')])
        if(loc=='USA'):
            st.write(df1[df1.Location.str.contains('usa',case=False)])

            
