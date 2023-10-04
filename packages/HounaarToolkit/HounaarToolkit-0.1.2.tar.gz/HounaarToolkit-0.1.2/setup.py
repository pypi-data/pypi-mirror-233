from setuptools import setup, find_packages

setup(
    name="HounaarToolkit",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "reportlab",
        "scikit-learn",
        "pyautogui",
        "colorama",
        "PyPDF2",
        "pytube",
        "requests",
        "beautifulsoup4",
        "scapy",
        "python-nmap",
    ],
    entry_points={
        "console_scripts": [
            "hounaartoolkit = hounaartoolkit.__init__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
