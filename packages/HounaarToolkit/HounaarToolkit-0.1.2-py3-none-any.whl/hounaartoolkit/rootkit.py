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
        

        
 ____             _   _    _ _    ____ _                            
|  _ \ ___   ___ | |_| | _(_) |_ / ___| | ___  __ _ _ __   ___ _ __ 
| |_) / _ \ / _ \| __| |/ / | __| |   | |/ _ \/ _` | '_ \ / _ \ '__|
|  _ < (_) | (_) | |_|   <| | |_| |___| |  __/ (_| | | | |  __/ |   
|_| \_\___/ \___/ \__|_|\_\_|\__|\____|_|\___|\__,_|_| |_|\___|_|   
                                                                    



        """

    print(Fore.GREEN +logo)  


    def run_rkhunter_scan():
        try:
            subprocess.run(["sudo", "rkhunter", "--check"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running rkhunter: {e}")
        else:
            print("rkhunter scan completed successfully.")


    if platform.system() == "Linux":
        run_rkhunter_scan()
    else:
        print("You are using Windows, so you should consider using dedicated Windows antivirus and anti-malware software, such as "
              f"{Fore.RED}Windows Defender{Style.RESET_ALL}, {Fore.GREEN}Malwarebytes{Style.RESET_ALL}, or other reputable security products that are compatible with Windows. "
              "These tools are specifically designed for Windows and can provide effective protection against various types of malware, including rootkits.")


if __name__ == "__main__":
    main()