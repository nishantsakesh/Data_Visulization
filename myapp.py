#importing all the librarie
import pandas as pd
import plotly
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Data Visualization ',
    page_icon='📊'
)

#title
st.title(':red[Data] Analytics Portal')
st.subheader(':grey[Explore Data With Ease]',divider='rainbow')

#creating a file uploader
file = st.file_uploader('Drop CSV or Excel file',type=['csv','xlsx'])

#we will check if the file ends with .csv name or  .xlsx
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)#if it ends with csv
    else:
        data = pd.read_excel(file)#if it ends with xlsx
    st.dataframe(data)#now we will set the dataframe 
    st.info('File is Sucessfully uploaded')#showing info that file is uploaded

    #creating subheader
    st.subheader(':rainbow[Basic Information Of the Dataset]',divider='rainbow')
    #we are creating variables so that it can show all the basic informations like rows, column, datatypes
    tab1,tab2,tab3,tab4= st.tabs(['Summary','Top and Bottom Rows', 'Data Types','Columns'])
    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
        st.subheader(':grey[Statistical Summary of the Dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':grey[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':grey[Bottom Rows]')
        bottomrows = st.slider('Number of Bottom you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':grey[Data types of Column]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column names of the Dataset')
        st.dataframe(list(data.columns))

    #now we are creating a bo where we can find the count of columns
    st.subheader(':rainbow[Column values to Count]',divider='rainbow')

    with st.expander('Value Count'):
        col1 , col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name', options=list(data.columns))
        with col2:
            toprows =st.number_input('Top Rows', min_value=1,step=1)
        count = st.button('Count')
        if (count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby : Simplify your data anylisis]', divider='rainbow')
    st.write('The Groupby lets you summarize data by specific categoeries and groups')
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('choose your column to groupby',options=list(data.columns))
        with col2:
            operation_col =st.selectbox('choose columns for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('choose operations',options=['sum','max','min','mean','median','count'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol =(operation_col,operation)
            ).reset_index()
            st.dataframe(result)

            st.subheader(':grey[Data Visualization]',divider='rainbow')
            graphs = st.selectbox('Choose your Graphs',options=['line','bar','scatter','pie','sunburst'])
            if(graphs=='line'):
                x_axis = st.selectbox('Choose X axis',options= list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options= list(result.columns))
                color = st.selectbox('Color Information',options=[None]+list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)

            elif(graphs=='bar'):
                x_axis = st.selectbox('Choose X axis',options= list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options= list(result.columns))
                color = st.selectbox('Color Information',options=[None]+list(result.columns))
                facet_col = st.selectbox('Column Information',options=[None]+list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)

            elif(graphs=='scater'):
                x_axis = st.selectbox('Choose X axis',options= list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options= list(result.columns))
                color = st.selectbox('Color Information',options=[None]+list(result.columns))
                size = st.selectbox('Size column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)

            elif(graphs=='pie'):
                values = st.selectbox('Choose Numerical values',options=list(result.columns))
                names = st.selectbox('Choose Labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)

            elif(graphs=='sunburst'):
                path =st.multiselect('Choose your path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)
