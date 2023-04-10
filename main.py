import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from io import StringIO
import pandas as pd
import mysql.connector
import plotly.express as px
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
sentiment=SentimentIntensityAnalyzer()
st.set_page_config(page_title="SENTIMENT ANALYSIS",page_icon="https://www.freecodecamp.org/news/content/images/size/w2000/2020/09/wall-5.jpeg")
st.title("SENTIMENT ANALYSIS SYSTEM")
st.sidebar.image("https://getthematic.com/assets/img/sentiment-analysis/fine-grained.png")
choice=st.sidebar.selectbox("MENU",("HOME","CSV FILE","GOOGLE SHEETS","MYSQL DATABASE"))
if(choice=="HOME"):
    st.markdown("<center><h1>WELCOME</h1></center>",unsafe_allow_html=True)
    st.image("https://imerit.net/wp-content/uploads/2021/07/what-is-sentiment-analysis.jpg")
    st.write("SENTIMENT ANALYSIS is a DATA SCIENCR PROJECT.IT HELPS TO KNOW THE OPINION OF THE PEOPLE WHETHER IT IS POSITIVE , NEGATIVE AND NEUTRAL")
elif(choice=="CSV FILE"):
    st.markdown("<center><h1>Upload your CSV FILE</h1></center>",unsafe_allow_html=True)
    file=st.file_uploader("Upload File Here")
    if file:
        b=file.getvalue()
        p=b.decode('utf-8')
        data=StringIO(p)
        df=pd.read_csv(data)
        pos=0
        neg=0
        neu=0
        for i in range(0,len(df)):
            k=df._get_value(i,'Review')
            pred=sentiment.polarity_scores(k)
            if(pred['compound']>0.5):
                pos=pos+1
            elif(pred['compound']<-0.5):
                neg=neg+1
            else:
                neu=neu+1
        positive=(pos/len(df))*100
        negative=(neg/len(df))*100
        neutral=(neu/len(df))*100
        st.write("Positive:",positive)
        st.write("Negative:",negative)
        st.write("Neutral:",neutral)
        fig=px.pie(values=[positive,negative,neutral],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)
elif(choice=="GOOGLE SHEETS"):
    id=st.text_input("Enter Sheet ID")
    r=st.text_input("Enter Range")
    btn=st.button('Analyze')
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file('google sheet.json',['https://www.googleapis.com/auth/spreadsheets'])
            st.session_state['cred']=f.run_local_server(port=0)
        service=build('Sheets','v4',credentials=st.session_state['cred']).spreadsheets().values()
        d=service.get(spreadsheetId=id,range=r).execute()
        data=d['values']
        sentiment=SentimentIntensityAnalyzer()
        pos=0
        neg=0
        neu=0
        for k in data:
            print(k[0])
            pred=sentiment.polarity_scores(k[0])
            if(pred['compound']>0.5):
                pos=pos+1
            elif(pred['compound']<-0.5):
                neg=neg+1
            else:
                neu=neu+1
        positive=(pos/len(data))*100
        negative=(neg/len(data))*100
        neutral=(neu/len(data))*100        
        st.write("Positive:",positive)
        st.write("Negative:",negative)
        st.write("Neutral:",neutral)
        fig=px.pie(values=[positive,negative,neutral],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)

elif(choice=="MYSQL DATABASE"):
    db=st.text_input("Enter database name")
    btn=st.button('Analyze')
    if btn:
        mydb=mysql.connector.connect(host='localhost',user='root',password='123456',database=db)
        c=mydb.cursor()
        c.execute('select (review) from opinion')
        l=[]
        for r in c:
            l.append(r)
        df=pd.DataFrame(data=l,columns=['review'])
        #st.dataframe(df)
        sentiment=SentimentIntensityAnalyzer()
        pos=0
        neg=0
        neu=0
        count=0
        for k in c:           
            count=count+1
            pred=sentiment.polarity_scores(k)                       
            if(pred['compound']>0.5):
                pos=pos+1
            elif(pred['compound']<-0.5):
                neg=neg+1
            else:
                neu=neu+1
        positive=(pos/count)*100
        negative=(neg/count)*100
        neutral=(neu/count)*100
        st.write("positive:",positive)
        st.write("negative:",negative)
        st.write("neutral:",neutral)
        fig=px.pie(values=[positive,negative,neutral],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)
        


    
      
  
        
        
        
