# Expiry Alert

Expiry Alert is a Streamlit web application designed to streamline invoice management and provide timely expiry notifications for products listed on invoices. The application integrates with the Gemini API for invoice processing and offers an intuitive interface for users to input invoice details and manage expiry dates.

## Features

- **Gemini API Integration**: Seamlessly send invoice images to the Gemini API and receive a list of items for efficient invoice processing.
- **Expiry Date Management**: Users can enter expiry dates for each product listed on invoices, facilitating better inventory management.
- **Alert System**: Receive timely email alerts when product expiry dates are approaching, helping users stay informed and proactive.

## Usage

1. **Installation**: Clone this repository and install the required dependencies using `pip install -r requirements.txt`.
2. **Run the App**: Start the Streamlit app by running `streamlit run app.py` in your terminal.
3. **Upload Invoice**: Upload the image of the invoice to the app interface.
4. **Enter Expiry Dates**: Once the list of items is generated, enter the expiry dates for each product.
5. **Receive Alerts**: Receive email alerts 10 days before the expiry date of any product listed on the invoice.

## Dependencies

- Python 3.x
- Streamlit
- Gemini API (API Key required)
- Pandas
- SMTP (for email alerts)

## Configuration

Ensure you have the necessary API keys for Gemini API integration. Additionally, configure the email settings (SMTP server, sender email, etc.) for sending expiry alerts.


## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request to suggest improvements or new features.

## Authors

- [PEELA SAHITH](https://github.com/sahith1s)

## Acknowledgments

Special thanks to the Streamlit community for their valuable contributions and support.
