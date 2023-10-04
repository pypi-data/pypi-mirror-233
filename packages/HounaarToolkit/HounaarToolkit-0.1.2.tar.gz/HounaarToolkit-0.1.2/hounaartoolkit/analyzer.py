
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
        print("""


              WELCOME TO

########     ###    ##     ## ########  #######   #######  ##       ##    ## #### ######## 
##     ##   ## ##   ##     ##    ##    ##     ## ##     ## ##       ##   ##   ##     ##    
##     ##  ##   ##  ##     ##    ##    ##     ## ##     ## ##       ##  ##    ##     ##    
##     ## ##     ## ##     ##    ##    ##     ## ##     ## ##       #####     ##     ##    
##     ## #########  ##   ##     ##    ##     ## ##     ## ##       ##  ##    ##     ##    
##     ## ##     ##   ## ##      ##    ##     ## ##     ## ##       ##   ##   ##     ##    
########  ##     ##    ###       ##     #######   #######  ######## ##    ## ####    ##    

              
              a Data Analysis AI



       
        """)

        # Step 1: Input and Data Importation
        file_path = input("Enter the file path: ")

        try:
            print("Checking file path..")
            data = pd.read_csv(file_path)  # You may need to handle different file formats.
        except FileNotFoundError:
            print("File not found. Please check the file path.")

        # Step 2: Detect Column Data Types
        column_data_types = data.dtypes
        categorical_columns = data.select_dtypes(include=['object']).columns
        for column in categorical_columns:
            # Use Label Encoding to convert categorical values to numerical values
            label_encoder = LabelEncoder()
            data[column] = label_encoder.fit_transform(data[column])

        # Step 3: Data Analysis and Machine Learning Tasks
        chart_filenames = []

        for column_name, column_data_type in column_data_types.iteritems():
            print(f"Analyzing Column: {column_name} (Data Type: {column_data_type})")

            # Perform analysis based on column data type
            if column_data_type == 'float64':
                print("Regression Analysis:")
                regression_models = [
                    ("Linear Regression", LinearRegression()),
                    ("Ridge Regression", Ridge(alpha=0.5)),
                    ("Lasso Regression", Lasso(alpha=0.1)),
                    ("Decision Tree Regressor", DecisionTreeRegressor()),
                    ("Random Forest Regressor", RandomForestRegressor()),
                    ("Gradient Boosting Regressor", GradientBoostingRegressor()),
                    ("Support Vector Regressor", SVR())
                ]
                for model_name, model in regression_models:
                    X = data.drop(column_name, axis=1)
                    y = data[column_name]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    mse = mean_squared_error(y_test, y_pred)
                    print(f"{model_name} - Mean Squared Error: {mse}")

                sns.pairplot(data, x_vars=[column_name], y_vars=regression_models[0][0], kind='reg')
                pairplot_filename = f'{column_name}_pairplot.png'
                plt.savefig(pairplot_filename)
                chart_filenames.append(pairplot_filename)
                plt.close()

                sns.lmplot(data=data, x=column_name, y=regression_models[0][0])
                lmplot_filename = f'{column_name}_lmplot.png'
                plt.savefig(lmplot_filename)
                chart_filenames.append(lmplot_filename)
                plt.close()

                sns.jointplot(data=data, x=column_name, y=regression_models[0][0])
                jointplot_filename = f'{column_name}_jointplot.png'
                plt.savefig(jointplot_filename)
                chart_filenames.append(jointplot_filename)
                plt.close()

                sns.regplot(data=data, x=column_name, y=regression_models[0][0])
                regplot_filename = f'{column_name}_regplot.png'
                plt.savefig(regplot_filename)
                chart_filenames.append(regplot_filename)
                plt.close()

            elif column_data_type == 'int64':
                print("Classification Analysis:")
                classification_models = [
                    ("Logistic Regression", LogisticRegression()),
                    ("Decision Tree Classifier", DecisionTreeClassifier()),
                    ("Random Forest Classifier", RandomForestClassifier()),
                    ("Gradient Boosting Classifier", GradientBoostingClassifier()),
                    ("Support Vector Classifier", SVC())
                ]
                for model_name, model in classification_models:
                    X = data.drop(column_name, axis=1)
                    y = data[column_name]
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled = scaler.transform(X_test)
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    accuracy = accuracy_score(y_test, y_pred)
                    print(f"{model_name} - Accuracy: {accuracy}")

                sns.countplot(data=data, x=column_name)
                countplot_filename = f'{column_name}_countplot.png'
                plt.savefig(countplot_filename)
                chart_filenames.append(countplot_filename)
                plt.close()

                sns.barplot(data=data, x=column_name, y=data[column_name])
                barplot_filename = f'{column_name}_barplot.png'
                plt.savefig(barplot_filename)
                chart_filenames.append(barplot_filename)
                plt.close()

                sns.boxplot(data=data, x=column_name, y=data[column_name])
                boxplot_filename = f'{column_name}_boxplot.png'
                plt.savefig(boxplot_filename)
                chart_filenames.append(boxplot_filename)
                plt.close()

                sns.violinplot(data=data, x=column_name, y=data[column_name])
                violinplot_filename = f'{column_name}_violinplot.png'
                plt.savefig(violinplot_filename)
                chart_filenames.append(violinplot_filename)
                plt.close()

                sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
                heatmap_filename = f'{column_name}_heatmap.png'
                plt.savefig(heatmap_filename)
                chart_filenames.append(heatmap_filename)
                plt.close()

            else:
                print("Clustering Analysis:")
                clustering_models = [
                    ("K-Means", KMeans(n_clusters=3)),
                    ("Agglomerative Clustering", AgglomerativeClustering(n_clusters=3)),
                    ("DBSCAN", DBSCAN(eps=0.5, min_samples=5))
                ]
                for model_name, model in clustering_models:
                    features_for_clustering = data
                    model.fit(features_for_clustering)

        for column_name in data.columns:
            plt.figure()
            plt.bar(data.index, data[column_name])
            plt.title(f"Bar Chart for {column_name}")
            plt.xlabel("Index")
            plt.ylabel(column_name)
            chart_filename = f'{column_name}_bar_chart.png'
            plt.savefig(chart_filename)
            chart_filenames.append(chart_filename)
            plt.close()

        pdf_merger = PyPDF2.PdfFileMerger()

        for chart_filename in chart_filenames:
            if chart_filename.endswith('.png'):
                pdf_filename = chart_filename.replace('.png', '.pdf')
                c = canvas.Canvas(pdf_filename, pagesize=letter)
                c.drawImage(chart_filename, 100, 500, width=400, height=300)
                c.save()
                pdf_merger.append(pdf_filename)

        merged_pdf_filename = 'merged_report.pdf'
        pdf_merger.write(merged_pdf_filename)
        pdf_merger.close()

        print(f"Report generated successfully as '{merged_pdf_filename}'.")




if __name__ == "__main__":
    main()
