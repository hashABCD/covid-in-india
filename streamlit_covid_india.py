# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:06:29 2020

@author: ABCD
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Read DataFrame
df=pd.read_csv("Covid_in_India.csv")

#Edit df
df.Date=pd.to_datetime(df.Date, format="%d-%m-%Y")
df=df.sort_values(by=["Date"])
df["Conf"]=df.ConfFor+df.ConfInd

#DEFINE FUNCTIONS

# Latest data statewise
def status_now():
    """
    Displays the latest statewise confirmed cases bar graph
    """
    
    df_state=df[df.Date==df.Date.max()]
    df_state=df_state.sort_values(by=["Conf"], ascending=False)

    last=df.Date.max()
    d=str(last.day)
    m=str(last.month)
    y=str(last.year)
    date_t=d+"-"+m+"-"+y

    st.markdown(f"Total Confirmed : {df_state.Conf.sum()}")
    st.markdown(f"   Indian Nationals: {df_state.ConfInd.sum()}")
    st.markdown(f"   Foreign Nationals: {df_state.ConfFor.sum()}")
    st.markdown(f"Recovered : {df_state.Rec.sum()}")
    st.markdown(f"Deaths : {df_state.Death.sum()}")
    st.markdown(f"Mortality Rate:{round(df_state.Death.sum()*100/df_state.ConfInd.sum(),2)}")
    
    
    plt.figure(figsize=(10,8))
    sns.set(style="darkgrid")
    st.title(f"Total confirmed Cases: {date_t}")
    #plt.title(f"Total confirmed cases as on {date_t}", fontsize=16)
    sns.barplot(x="State", y="Conf", data=df_state)
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot()
    
#Time Series Maker    
def ts_maker(region="All"):
    """
    Takes in State Name 
    Returns time series dataframe
    """
    if region=="All":
        df_temp=df
    else:
        df_temp=df[df.State==region]
    dates=df_temp.Date.unique()
    ConfTot=[]
    DeathTot=[]
    RecTot=[]
    MortRate=[]
    for date in dates:
        ConfTot.append(df_temp.Conf[df_temp.Date==date].sum())
        DeathTot.append(df_temp.Death[df_temp.Date==date].sum())
        RecTot.append(df_temp.Rec[df_temp.Date==date].sum())
        MortRate.append(round(df_temp.Death[df_temp.Date==date].sum()*100/df_temp.Conf[df_temp.Date==date].sum(),2))
    ts_dict={"Date":dates,"ConfTot":ConfTot,"DeathTot":DeathTot,"RecTot":RecTot,"MortRate":MortRate}
    ts=pd.DataFrame(ts_dict)
    return(ts)

#Time Series Plotter
def ts_plotter(region="All"):
    """
    Takes in Region Name
    Plots status
    """
    ts=ts_maker(region)
    
    plt.figure(figsize=(10,6))
    sns.set(style="darkgrid")
    #st.markdown(f"State: {region}")
    plt.plot(ts.Date, ts.ConfTot, marker='s', c='k', label="Confirmed")
    plt.plot(ts.Date, ts.DeathTot, marker='s', c='r', label="Death")
    plt.plot(ts.Date, ts.RecTot, marker='s', c='g',label="Recovered")
    plt.legend()
    st.pyplot()

    plt.figure(figsize=(10,6))
    st.markdown(f"Morality Rate:")
    plt.plot(ts.Date, ts.MortRate, marker='s', c='k', label="Mortality Rate")
    plt.legend()
    st.pyplot()


st.title("COVID IN INDIA")    
#Function Call
status_now()

st.title("Time Series")
#selectbox
r_name=["All"]
r_name=r_name+(list(df.State.unique()))
re_sel_name=st.selectbox("Select Region", (r_name))
ts_plotter(re_sel_name)    
