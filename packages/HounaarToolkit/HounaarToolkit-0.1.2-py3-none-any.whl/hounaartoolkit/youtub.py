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
      logo = """

#     #                                          
 #   #   ####  #    # ##### #    # #####  ###### 
  # #   #    # #    #   #   #    # #    # #      
   #    #    # #    #   #   #    # #####  #####  
   #    #    # #    #   #   #    # #    # #      
   #    #    # #    #   #   #    # #    # #      
   #     ####   ####    #    ####  #####  ###### 



######                                                                 
#     #  ####  #    # #    # #       ####    ##   #####  ###### #####  
#     # #    # #    # ##   # #      #    #  #  #  #    # #      #    # 
#     # #    # #    # # #  # #      #    # #    # #    # #####  #    # 
#     # #    # # ## # #  # # #      #    # ###### #    # #      #####  
#     # #    # ##  ## #   ## #      #    # #    # #    # #      #   #  
######   ####  #    # #    # ######  ####  #    # #####  ###### #    # 




      """

      print(Fore.GREEN +logo)



      real = input("Enter video url:")

      print("Checking video url validation...")
      video = YouTube(real)
      print("URL set: Checked")

      print("Checking Resolutions...")
      stream = video.streams.get_highest_resolution()
      print("Highest resolution: Checked")

      print("Downloading the file...")
      downloader = stream.download()
      print("<================================>")

      print("DONE !!")


if __name__ == "__main__":
    main()