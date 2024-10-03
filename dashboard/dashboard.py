import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Visualization Data E-commerce")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

st.write("Most popular orders dan payment methods per region")

if uploaded_file is not None:
    # Read CSV file
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
    
    # Display first 5 rows of uploaded data
    st.write("Uploaded data:")
    st.dataframe(data.head())

    # Check if required columns exist
    required_columns = ['customer_state', 'order_id', 'payment_type']
    if not all(column in data.columns for column in required_columns):
        st.error(f"Required columns missing: {', '.join([col for col in required_columns if col not in data.columns])}")
    else:
        # Handling missing values in payment_type
        data['payment_type'] = data['payment_type'].fillna('Unknown')

        # Group by region and calculate total orders and most common payment methods
        orders_by_region = data.groupby('customer_state')['order_id'].count().sort_values(ascending=False)
        payment_methods_by_region = data.groupby('customer_state')['payment_type'].agg(lambda x: x.value_counts().index[0])

        # Create a DataFrame with the results
        result_table = pd.DataFrame({
            'Total_Orders': orders_by_region,
            'Most_Common_Payment_Method': payment_methods_by_region
        })

        # Display result table
        st.write("Table of Most popular orders dan payment methods per region:")
        st.dataframe(result_table)

        # Plot: 10 regions with the highest number of orders
        top_10_regions = orders_by_region.nlargest(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_10_regions.index, y=top_10_regions.values)
        plt.title('10 Regions with the Highest Number of Orders')
        plt.xlabel('Region')
        plt.ylabel('Total Orders')
        plt.xticks(rotation=45)
        for i, v in enumerate(top_10_regions.values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()  # Clear the figure

        # Plot: Most common payment methods in the top region
        top_region = orders_by_region.index[0]
        top_region_payment_methods = data[data['customer_state'] == top_region]['payment_type'].value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_region_payment_methods.index, y=top_region_payment_methods.values)
        plt.title(f'Payment Methods in {top_region} (Region with the Highest Orders)')
        plt.xlabel('Payment Methods')
        plt.ylabel('Number of Uses')
        plt.xticks(rotation=45)
        for i, v in enumerate(top_region_payment_methods.values):
            plt.text(i, v, str(v), ha='center', va='bottom')
        plt.tight_layout()
        st.pyplot(plt)
        plt.clf()  # Clear the figure

        # Additional analysis: Product categories with the highest reviews
        st.write("Calculates the product categories with the highest reviews")

        if 'product_id' in data.columns and 'order_id' in data.columns and 'review_score' in data.columns and 'product_category_name' in data.columns:
            # Filter positive reviews
            positive_reviews_df = data[data['review_score'] >= 4]
            positive_reviews_by_category = positive_reviews_df.groupby('product_category_name')['review_score'].count().sort_values(ascending=False)

            # Display table of most frequent categories with high reviews
            st.write("Table of Product Categories that Most Frequently Get the Highest Reviews:")
            st.dataframe(positive_reviews_by_category)

            # Plot: Top 10 product categories with the highest review values
            top_10_categories = positive_reviews_by_category.head(10)
            plt.figure(figsize=(12, 6))
            sns.barplot(x=top_10_categories.index, y=top_10_categories.values)
            plt.title('10 Product Categories with the Highest Review Values')
            plt.xlabel('Product Categories')
            plt.ylabel('Number of Reviews')
            plt.xticks(rotation=45)
            for i, v in enumerate(top_10_categories.values):
                plt.text(i, v, str(v), ha='center', va='bottom')
            plt.tight_layout()
            st.pyplot(plt)
            plt.clf()  # Clear the figure
        else:
            st.error("Data is incomplete, required columns not found.")
