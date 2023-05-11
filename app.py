import streamlit as st
import pandas as pd
import plotly.express as px
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

st.set_page_config(
        page_title="dashboard",
        layout="wide", 
        initial_sidebar_state="auto", 
        menu_items=None
        )
# hide streamlit banner
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
df = pd.read_excel('ข้อมูลรายการสั่งซื้อ Testing.xlsx')


a = df['Company'].nunique()
b = df['Supplier'].nunique()
c = df['NetAmount_THB'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Unique Buyers", a, )
col2.metric("Unique Sellers", b, )
col3.metric("Total Volumes", human_format(c) )

col_1, col_2 = st.columns([3,1])

with col_1:
    # hist
    st.header("Sellers' Orders for Overtime")
    df_plot = df[['POCreateDate', 'NetAmount_THB', 'Company']]
    df_plot['POCreateDate'] = pd.to_datetime(df_plot['POCreateDate']).dt.date + pd.offsets.MonthBegin(0)
    df_plot = df_plot.groupby(['POCreateDate', 'Company']).sum().reset_index()


    fig = px.bar(df_plot, x='POCreateDate', y='NetAmount_THB', color="Company", barmode='group')
    fig.update_layout(legend=dict(
        title=None,
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="left",
        x=0
    ))
    st.plotly_chart(fig, theme=None, use_container_width=True)
with col_2:
    
    st.header('Product Proportion')
    df_pie = df.groupby(['MatGroup'])[['NetAmount_THB']].sum().reset_index()
    df_pie['NetAmount_THB'] = (df_pie['NetAmount_THB'] / df_pie['NetAmount_THB'].sum())*100

    fig = px.pie(df_pie, values='NetAmount_THB', names='MatGroup')
    fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
    fig.update(layout_showlegend=False)
    st.plotly_chart(fig, theme=None, use_container_width=True)
    
###### table
col_1, col_2 = st.columns([2,5])
with col_1:
    
    st.header('Top 10 Buyers & Sellers')
    df_top10_orders = df.groupby(['Supplier', 'Company']).agg({'NetAmount_THB':'sum'}).reset_index()
    df_top10_orders = df_top10_orders.sort_values('NetAmount_THB', ascending=False).reset_index(drop=True)
    df_top10_orders['NetAmount_THB'] = df_top10_orders['NetAmount_THB'].apply( lambda x: human_format(x))
    df_top10_orders = df_top10_orders[:10]
    df_top10_orders['Supplier'] = df_top10_orders['Supplier'].astype(str)
    df_top10_orders['Company'] = df_top10_orders['Company'].astype(str)
    st.dataframe(df_top10_orders.set_index('Company'))
    
with col_2:
    st.header('Top 10 Product sales')
    df_top10_orders = df.groupby(['Company', 'ItemDescription']).agg({'NetAmount_THB':'sum'}).reset_index()
    df_top10_orders = df_top10_orders.sort_values('NetAmount_THB', ascending=False).reset_index(drop=True)
    df_top10_orders['NetAmount_THB'] = df_top10_orders['NetAmount_THB'].apply( lambda x: human_format(x))
    df_top10_orders = df_top10_orders[:10]
    st.dataframe(df_top10_orders.set_index('Company'), use_container_width=True)

# line
st.header("Buyers' Orders for Overtime")
df_plot = df[['POCreateDate', 'NetAmount_THB', 'Supplier']]
df_plot['POCreateDate'] = pd.to_datetime(df_plot['POCreateDate']).dt.date + pd.offsets.MonthBegin(0)
df_plot = df_plot.groupby(['POCreateDate', 'Supplier']).sum().reset_index()
df_plot['Supplier'] = df_plot['Supplier'].astype(str)
df_plot = df_plot[df_plot['Supplier'].isin(['40', '541', '545'])]


fig = px.line(df_plot, x='POCreateDate', y='NetAmount_THB', color="Supplier")
fig.update_layout(legend=dict(
    title=None,
    orientation="h",
    yanchor="bottom",
    y=1.05,
    xanchor="left",
    x=0
))
st.plotly_chart(fig, theme=None, use_container_width=True)