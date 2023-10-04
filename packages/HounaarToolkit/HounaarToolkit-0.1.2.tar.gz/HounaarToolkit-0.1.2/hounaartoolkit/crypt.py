import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import LabelEncoder
import pyautogui
import time
import platform
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from colorama import Back, Fore, Style
import PyPDF2
import json
import os
from pytube import YouTube
import requests
from bs4 import BeautifulSoup
import re , time
import subprocess
import socket
import os
from scapy.all import ARP, Ether, srp, conf
import nmap


def main():
      
      logo ="""
      .o88b. d8888b. db    db d8888b. d888888b  .d88b.  
      d8P  Y8 88  `8D `8b  d8' 88  `8D `~~88~~' .8P  Y8. 
      8P      88oobY'  `8bd8'  88oodD'    88    88    88 
      8b      88`8b      88    88~~~      88    88    88 
      Y8b  d8 88 `88.    88    88         88    `8b  d8' 
      `Y88P' 88   YD    YP    88         YP     `Y88P' 

      d8888b. d8888b. d888888b  .o88b. d88888b 
      88  `8D 88  `8D   `88'   d8P  Y8 88'     
      88oodD' 88oobY'    88    8P      88ooooo 
      88~~~   88`8b      88    8b      88~~~~~ 
      88      88 `88.   .88.   Y8b  d8 88.     
      88      88   YD Y888888P  `Y88P' Y88888P 
                                             


      """

      print(Fore.GREEN +logo)  
      crypto = input("Enter your cryptocurrency in ALL CAPITAL Letters:")
      key = "https://api.binance.com/api/v3/ticker/price?symbol="+crypto
      while True:
         data = requests.get(key)  
         data = data.json()
         print(f"{data['symbol']} price is {data['price']}")




if __name__ == "__main__":
    main()

