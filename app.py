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

df = pd.read_excel('ข้อมูลรายการสั่งซื้อ Testing.xlsx')

# hist
st.header('Orders Overtime by Sellers')
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

###### table
col_1, col_2 = st.columns([2,4])
with col_1:
    st.header('Top 10 Buyers & Sellers')
    df_top10_orders = df.groupby(['Supplier', 'Company']).agg({'NetAmount_THB':'sum'}).reset_index()
    df_top10_orders = df_top10_orders.sort_values('NetAmount_THB', ascending=False).reset_index(drop=True)
    df_top10_orders['NetAmount_THB'] = df_top10_orders['NetAmount_THB'].apply( lambda x: human_format(x))
    df_top10_orders = df_top10_orders[:10]
    df_top10_orders['Supplier'] = df_top10_orders['Supplier'].astype(str)
    df_top10_orders['Company'] = df_top10_orders['Company'].astype(str)
    st.dataframe(df_top10_orders)
    
with col_2:
    st.header('Top 10 Product sales')
    df_top10_orders = df.groupby(['Company', 'ItemDescription']).agg({'NetAmount_THB':'sum'}).reset_index()
    df_top10_orders = df_top10_orders.sort_values('NetAmount_THB', ascending=False).reset_index(drop=True)
    df_top10_orders['NetAmount_THB'] = df_top10_orders['NetAmount_THB'].apply( lambda x: human_format(x))
    df_top10_orders = df_top10_orders[:10]
    st.dataframe(df_top10_orders, use_container_width=True)