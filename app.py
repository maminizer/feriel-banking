import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

# Title of the app
st.title("Banking Transactions & Amount Time Series Analysis")


st.subheader('CSV File Upload')
# File uploader placeholder
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Sidebar for user input
st.sidebar.title('Select Account ID')
selected_account_id = st.sidebar.number_input('Enter Account ID' , value=5740)

# Define operation types
operation_types = [
    "CASH WITHDRAWAL",
    "REMITTANCE TO ANOTHER BANK",
    "CREDIT IN CASH",
    "COLLECTION FROM ANOTHER BANK",
    "CREDIT CARD WITHDRAWAL"
]

# Sidebar for user input
st.sidebar.title('Select Operation Type')
selected_operation = st.sidebar.selectbox('Choose Operation Type', operation_types)


if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    df = df.drop(['Unnamed: 0'], axis=1)

    col1, col2, col3 = st.columns([3, 1, 1])
    # Display the dataframe
    col1.write("Dataframe:")
    col1.dataframe(df, width=1000, height=300)

    # Check for missing values
    missing_values = df.isnull().sum()
    col2.write("Missing Values:")
    col2.dataframe(missing_values, width=300)

    # Get summary statistics for 'amount' and 'balance'
    summary_statistics = df[['amount', 'balance']].describe()
    col3.write("Summary Statistics:")
    col3.dataframe(summary_statistics)

    # Check for missing values and display summary statistics if relevant columns exist
    if 'amount' in df.columns and 'balance' in df.columns:

        st.subheader('Data Distribution Analysis')
        col3, col4 = st.columns(2)

        # Histogram for amount
        fig_amount = px.histogram(
            df, x='amount', nbins=30, title='Distribution of Transaction Amounts')
        col3.plotly_chart(fig_amount)

        # Histogram for balance
        fig_balance = px.histogram(
            df, x='balance', nbins=30, title='Distribution of Account Balances')
        col4.plotly_chart(fig_balance)

        # Calculate outliers
        total_observations = len(df)
        Q1 = df[['amount', 'balance']].quantile(0.25)
        Q3 = df[['amount', 'balance']].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers_amount = ((df['amount'] < lower_bound['amount']) | (
            df['amount'] > upper_bound['amount'])).sum()
        outliers_balance = ((df['balance'] < lower_bound['balance']) | (
            df['balance'] > upper_bound['balance'])).sum()

        # Calculate percentage of outliers
        outliers_amount_percentage = (
            outliers_amount / total_observations) * 100
        outliers_balance_percentage = (
            outliers_balance / total_observations) * 100

        st.subheader('Outline Percentage in Target Features')
        col5, col6 = st.columns(2)

        # Display outliers in cards
        col5.metric(label="Outliers Percentage in Amount",
                    value=f"{outliers_amount_percentage:.2f}%")
        col6.metric(label="Outliers Percentage in Balance",
                    value=f"{outliers_balance_percentage:.2f}%")

        # Convert date to string and split it into year, month, and day
        df['date'] = df['date'].astype(str)
        df['year'] = df['date'].str[:2]
        df['month'] = df['date'].str[2:4]
        df['day'] = df['date'].str[4:]

        # Convert year to the correct format
        # Assuming all years are in 20th century
        df['year'] = '19' + df['year']

        # Convert year, month, and day to datetime format
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        # Set 'date' as index
        df.set_index('date', inplace=True)
        
        st.subheader('Amount Distribution By Month/Year')
        col7, col8 = st.columns(2)
        
        # Group by year and sum the 'amount'
        total_amount_yearly = df.groupby('year')['amount'].sum()
        
        bar_amount_year = px.bar(total_amount_yearly)
        col7.plotly_chart(bar_amount_year, x='Year', y='Total Amount', title='Total Amount Distribution by Year')
        
        # Group by month and sum the 'amount'
        total_amount_monthly = df.groupby('month')['amount'].sum() 
        
        bar_amount_month = px.bar(total_amount_monthly)
        col8.plotly_chart(bar_amount_month, x='Month', y='Total Amount', title='Total Amount Distribution by Month')
        
        # Group by day and sum the 'amount'
        total_amount_daily = df.groupby('day')['amount'].sum()
        st.subheader('Transaction Distribution By Month/Year')
        col9, col10 = st.columns(2)
        
        # Total transactions by month
        total_transactions_yearly = df.groupby('year').size()
        bar_transaction_yearly = px.bar(total_transactions_yearly)
        col9.plotly_chart(bar_transaction_yearly, x='Year',use_container_width=True, y='Total Amount', title='Total Transacation Distribution by Year')
        
        # Total transactions by month
        total_transactions_monthly = df.groupby('month').size()
        bar_transaction_month = px.bar(total_transactions_monthly)
        col10.plotly_chart(bar_transaction_month, x='Month',use_container_width=True, y='Total Amount', title='Total Transacation Distribution by Month')
        
        # Filter DataFrame based on selected account ID
        account_data = df[df['account_id'] == int(selected_account_id)]
        # Plotting function using Plotly
        def plot_time_series(account_data):
            fig = go.Figure()
            
            # Positive balances in blue
            fig.add_trace(go.Scatter(x=account_data.index, y=account_data['balance'], mode='lines+markers', name='Positive Balances', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=account_data.index[account_data['balance'] < 0], y=account_data['balance'][account_data['balance'] < 0], mode='markers', name='Negative Balances', marker=dict(color='red', size=10)))
            
            fig.update_layout(title=f'Time Series of Balance for Account {int(selected_account_id)}',
                            xaxis_title='Date',
                            yaxis_title='Balance',
                            showlegend=True,
                            hovermode='x unified')
            
            st.plotly_chart(fig, use_container_width=True)
        
        
        st.subheader('Balance Evolution of Given Client')
        # Ensure there's data for the selected account ID
        if not account_data.empty:
            plot_time_series(account_data)
        else:
            st.warning(f'No data found for Account ID {selected_account_id}')
        
        
        st.subheader('Amount Distribution By Operation Type')
        # Filter DataFrame based on selected operation type
        operation_df = df[df['operation'] == selected_operation]
        if not operation_df.empty:
            
            # fig_operation = px.histogram(operation_df, x='amount')
            fig_operation = px.histogram(operation_df, x='amount', nbins=30, title=f'Distribution of Amounts - {selected_operation}', marginal='violin', color_discrete_sequence=['skyblue'])

            # Display the plotly chart in Streamlit
            st.plotly_chart(fig_operation,  use_container_width=True)
        else:
            st.warning(f'No Operation is selected')
else:
    st.write("The dataframe does not contain 'amount' and 'balance' columns.")





