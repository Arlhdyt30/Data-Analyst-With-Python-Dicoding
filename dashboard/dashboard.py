import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Visualization Data E-commerce")


uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

st.write("Most popular orders dan payment methods per region")

if uploaded_file is not None:
    
    data = pd.read_csv(uploaded_file)
    
    
    st.write("uploaded data:")
    st.dataframe(data.head())

    
    orders_by_region = data.groupby('customer_state')['order_id'].count().sort_values(ascending=False)
    
    
    payment_methods_by_region = data.groupby('customer_state')['payment_type'].agg(lambda x: x.value_counts().index[0])

    
    result_table = pd.DataFrame({
        'Total_Orders': orders_by_region,
        'Most_Common_Payment_Method': payment_methods_by_region
    })
    
    
    st.write("Table of Most popular orders dan payment methods per region:")
    st.dataframe(result_table)

    
    top_10_regions = orders_by_region.nlargest(10)

    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_regions.index, y=top_10_regions.values)
    plt.title('10 region with the highest number of order')
    plt.xlabel('region')
    plt.ylabel('total orders')
    plt.xticks(rotation=45)
    for i, v in enumerate(top_10_regions.values):
        plt.text(i, v, str(v), ha='center', va='bottom')
    plt.tight_layout()

    
    st.pyplot(plt)

    
    top_region = orders_by_region.index[0]
    top_region_payment_methods = data[data['customer_state'] == top_region]['payment_type'].value_counts()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_region_payment_methods.index, y=top_region_payment_methods.values)
    plt.title(f'Payments methods in {top_region} (regions with the highest orders)')
    plt.xlabel('Payments Methods')
    plt.ylabel('Number or uses')
    plt.xticks(rotation=45)
    for i, v in enumerate(top_region_payment_methods.values):
        plt.text(i, v, str(v), ha='center', va='bottom')
    plt.tight_layout()

    
    st.pyplot(plt)

    
    st.write("Calculates the product categories with the highest reviews")

    
    if 'product_id' in data.columns and 'order_id' in data.columns and 'review_score' in data.columns and 'product_category_name' in data.columns:
        
        positive_reviews_df = data[data['review_score'] >= 4]
        positive_reviews_by_category = positive_reviews_df.groupby('product_category_name')['review_score'].count().sort_values(ascending=False)

        
        st.write("Table of Product Categories that Most Frequently Get the Highest Reviews:")
        st.dataframe(positive_reviews_by_category)

        
        top_10_categories = positive_reviews_by_category.head(10)

        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_10_categories.index, y=top_10_categories.values)
        plt.title('10 Product Categories with the Highest Review Values')
        plt.xlabel('Product categories')
        plt.ylabel('Number or reviews')
        plt.xticks(rotation=45)
        for i, v in enumerate(top_10_categories.values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        plt.tight_layout()

        st.pyplot(plt)
    else:
        st.error("Data is incomplete, required column not found.")
