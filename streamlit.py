import streamlit as st 
import pandas as pd
import numpy as nps

 
customers_df = pd.read_csv("https://raw.githubusercontent.com/Rachryy/Dataset/main/olist_customers_dataset.csv")
products_df = pd.read_csv("https://raw.githubusercontent.com/Rachryy/Dataset/main/olist_products_dataset.csv")
orders_dataset_df = pd.read_csv("https://raw.githubusercontent.com/Rachryy/Dataset/main/olist_orders_dataset.csv")
orders_item_dataset_df = pd.read_csv("https://raw.githubusercontent.com/Rachryy/Dataset/main/olist_order_items_dataset.csv")

orders_dataset_df.dropna(axis=0, inplace=True)
products_df.dropna(axis=0, inplace=True)



columns = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
for column in columns:
  orders_dataset_df[column] = pd.to_datetime(orders_dataset_df[column])
  
orders_w_product_df = pd.merge(
    left=orders_item_dataset_df, right=products_df,
    how="outer",
    on="product_id"
    )

orders_item_df = pd.merge(
    left=orders_item_dataset_df, right=orders_dataset_df,
    how="left",
    on="order_id"
    )

customer_item_df = pd.merge(
    left=customers_df, right=orders_item_df,
    how="left",
    on="customer_id"
    )
customer_item_df.isna().sum()
  
group_param = orders_item_df['order_purchase_timestamp'].dt.to_period("Q")
quarterly_order = orders_item_df.groupby(group_param).order_id.nunique()

top_product = orders_w_product_df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).head(5)

category_by_city = customer_item_df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).reset_index()

state_name = {
"AC" : "Acre",
"AL" : "Alagoas",
"AM" : "Amazonas",
"AP" : "Amapa",
"BA" : "Bahia",
"CE" : "Ceara",
"DF" : "Distrito Federal",
"ES" : "Espirito Santo",
"GO" : "Goias",
"MA" : "Maranhao",
"MG" : "Minas Gerais",
"MS" : "Mato Grosso do Sul",
"MT" : "Mato Grosso",
"PA" : "Para",
"PB" : "Paraiba",
"PE" : "Pernambuco",
"PI" : "Piaui",
"PR" : "Parana",
"RJ" : "Rio de Janeiro",
"RN" : "Rio Grande do Norte",
"RO" : "Rondonia",
"RR" : "Roraima",
"RS" : "Rio Grande do Sul",
"SC" : "Santa Catarina",
"SE" : "Sergipe",
"SP" : "Sao Paulo",
"TO" : "Tocantins"
}
customer_item_df['customer_state'] = customer_item_df['customer_state'].map(state_name)

category_by_state = customer_item_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False).reset_index()


st.header('Dasboard')
st.bar_chart(quarterly_order)
st.bar_chart(top_product)
st.bar_chart(category_by_city['order_id'].head(15))
st.bar_chart(category_by_state['order_id'].head(15))
