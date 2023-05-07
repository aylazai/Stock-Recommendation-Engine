# Stock Trend Prediction WebApp

This is a Python-based web application that predicts stock trends using a multi-layer LSTM recurrent neural network. The web app uses Streamlit to create a user-friendly graphical interface for inputting stocks and displaying prediction results.

## Installation

To install the necessary packages, please run the following command:

```
pip install -r requirements.txt
```

## Usage

To run the web app, navigate to the project directory in your terminal and run the following command:

```
streamlit run app.py
```

This will launch the web app in your browser. Input the stock you wish to predict and the web app will display the raw data in a table and provide visualizations of the predicted versus original values.

## Methodology

The predictions are made using a multi-layer LSTM recurrent neural network, which predicts the last value out of a sequence of values. The model is trained on historical stock data and uses technical indicators to predict future trends.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
