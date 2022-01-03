# Stock-Recommendation-Engine
A larger scale stock recommendation system with Python. I use the three indices; NIFTY50, BOVESPA,  &amp; RTSI in this program as an example. 
## How it Works
First, the program requests online stock price data and stores this data into the MySQL database and I keep this scalable so that you can adjust for any number of indices.
Then we apply the following technical indicators: MACD, Golden Cross, RSI & Long Term SMA. The program then screens all the stocks and prints it's reccommendations.
Last, I automize the system by first updating the MySQL database and sending an email to the user containing the signals with the smtp library. 
