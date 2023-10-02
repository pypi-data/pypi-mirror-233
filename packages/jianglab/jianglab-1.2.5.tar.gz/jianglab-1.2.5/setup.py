from setuptools import setup, find_packages

setup(
    name='jianglab',
    version='1.2.5',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "treelib==1.6.4",
        "McsPyDataTools",
        "tqdm",
        "scipy",
        "gspread",
        "oauth2client",
        "xmltodict",
        "opencv-python",
        "ipython",
        "seaborn",
        "optuna",
        "xgboost",
        "scikit-learn",
        "umap-learn",
        "missingno",

    ],
    author = "Jiang Zheng",
    author_email = "zjiang314@gmail.com",
    description = "A package for Jiang lab",
    url = "https://github.com/jiang-lab-retina/jianglab.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

