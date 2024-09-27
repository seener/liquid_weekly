# Basic Web Scraper

How to setup the proper environment.

If you're using conda: 

```
$ conda create -n {env name} python=3.11
$ conda activate {env name}
$ pip install -r requirements.txt
```

If you're using python virtual environments on mac or unix:

```
$ python3.11 -m venv {env_name}
$ source {env_name}/bin/activate
$ pip install -r requirements.txt
```

If you're using python virtual environments on windows:

```
$ python3.11 -m venv {env_name}
$ {env_name}\Scripts\activate
$ pip install -r requirements.txt
```

How to run the script: 
1. The expected input is a CSV file. I have assumed that the URLs are in the first column in the CSV. You can specify if the CSV does or does not have a column header.
2. From your command line:
```
$ python web_page_processing.py
Provide the file path to a csv with urls: {full path to csv}
Does your csv have column headers [Y/N]: {y or n}
```
3. It will output an Excel file to the same director with the same name as your input file but with the *"- processed"* suffix