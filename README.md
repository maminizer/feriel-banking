# Bank Account Transaction Analysis

This project is a Streamlit application for analyzing bank account transactions. It visualizes the distribution of transaction amounts and other relevant data using Plotly.

## Features

- Filter transactions by account ID or operation type.
- Visualize the distribution of transaction amounts with histograms.
- Display the top 10 account IDs with the highest total amounts for each operation type.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/bank-account-analysis.git
    cd bank-account-analysis
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

1. Start the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the app.

## Usage

1. Select an account ID or an operation type from the sidebar.
2. View the resulting plots and analysis on the main page.

## Data

Ensure that your `df_bank` DataFrame contains the following columns:

- `account_id`: The ID of the account.
- `date`: The date of the transaction.
- `operation`: The type of operation (e.g., "CASH WITHDRAWAL", "REMITTANCE TO ANOTHER BANK").
- `amount`: The transaction amount.

## Dependencies

- pandas
- streamlit
- plotly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
