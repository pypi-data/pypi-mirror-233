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
    

    
 __   _ _______ _______ _______ _______ _______ __   _ __   _ _______  ______
 | \  | |______    |    |______ |       |_____| | \  | | \  | |______ |_____/
 |  \_| |______    |    ______| |_____  |     | |  \_| |  \_| |______ |    \_
                         


      """

    print(Fore.GREEN +logo)  

    print("Loading...")


    def get_local_ip():
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except socket.error as e:
            pass
        return []

    def scan_local_network(ip_range):
        local_ip = get_local_ip()
        if local_ip:
            try:
                arp = ARP(pdst=ip_range)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                packet = ether / arp

                result = srp(packet, timeout=3, verbose=0)[0]

                online_hosts = [recon.psrc for sent, recon in result]
                return online_hosts
            except Exception as e:
                pass
        return []

    def scan_online_hosts(online_hosts):
        nm = nmap.PortScanner()
        for host in online_hosts:
            try:
                nm.scan(hosts=host, arguments='-O -p 1-65535', timeout=300)
            except Exception as e:
                pass
        
        return nm.all_hosts(), nm.all_os_matches(), nm.all_protocols(), nm.all_tcp(), nm.all_udp()

    def runner():
        ip_range = "192.168.1.1/24"
        
        local_ip = get_local_ip()
        if local_ip:
            pass

        online_hosts = scan_local_network(ip_range)
        if not online_hosts:
            return

        all_hosts, os_info, protocols, tcp_info, udp_info = scan_online_hosts(online_hosts)

    runner()    




if __name__ == "__main__":
    main()
