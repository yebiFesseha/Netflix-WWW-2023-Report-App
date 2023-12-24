import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import os

st.markdown('### A netflix 2023 "What We Watched" Hours-Viewed Report analysis')

file_path = 'data/What_We_Watched_A_Netflix_Engagement_Report_2023Jan-Jun.xlsx'
df = pd.read_excel(file_path, header=5, usecols=['Title', 'Available Globally?', 'Release Date',
       'Hours Viewed'])
#create the title index
df.set_index('Title', inplace=True)

df['Release Year'] = df['Release Date'].dt.year
#convert floating to int, at the same time handle inf or nan to zero
df['Release Year'] = df['Release Year'].fillna(0).astype('int')

#rank them all
df['overall_ranking']=df['Hours Viewed'].rank(method='dense', ascending=False)
#create a ranking per year for Hours Viewed
df['yearly_ranking'] = df.groupby('Release Year')['Hours Viewed'].rank(method='dense', ascending=False)
df=df[['overall_ranking', 'yearly_ranking', 'Hours Viewed', 'Release Year', 'Release Date', 'Available Globally?']]

st.markdown('---')
st.sidebar.markdown('#### Release Year')
user_year_selection=st.sidebar.radio('', ['all', 2023, 2022, 2021, 2020, 2019,2018, 2017, 2016, 2015, 2014,
        2013, 2012,2011, 2010])

#overall ranking
if user_year_selection == 'all':
    st.markdown(f'##### Overall Ranking for the total of {df.shape[0]} movies/tv shows that have been released.')
    df['Release Year'] = df['Release Year'].apply(lambda x: '{:.0f}'.format(x))
    df
else:
    #to remove the int thousands comma separator i used the code below
    filt_df = df.loc[df['Release Year']==user_year_selection]
    filt_df['Release Year'] = filt_df['Release Year'].apply(lambda x: '{:.0f}'.format(x))
    #Dsiplay the table per release-year, 
    st.markdown(f"##### Ranking per Release-year: In the year {user_year_selection}, there were {df.loc[df['Release Year']==user_year_selection].shape[0]} movies/tv shows that have been released.")
    st.dataframe(filt_df)

#top10 bar chart of all time and per year
if user_year_selection == 'all':
    st.markdown(f'##### TOP-10 of the **complete** release-year list.')
    top10_df = df.loc[df['overall_ranking']<=10].sort_values(by='Hours Viewed', ascending=False)
    st.bar_chart(data=top10_df , y='Hours Viewed', color='#FFA500')
else:
    st.markdown(f'##### TOP-10 of the **{user_year_selection}** release-year')
    top10_df = df.loc[(df['yearly_ranking']<=10) & (df['Release Year']==user_year_selection)].sort_values(by='Hours Viewed', ascending=False)
    #st.markdown('---')
    st.bar_chart(data=top10_df , y='Hours Viewed', color='#FFA500')
