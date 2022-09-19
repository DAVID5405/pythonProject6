import json

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from pydantic import BaseModel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


app = FastAPI()
templates = Jinja2Templates(directory="templates/")

def weather(city):
    city = city.replace(" ", "+")
    res = requests.get(
        f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',
        headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    time = soup.select('#wob_dts')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather = soup.select('#wob_tm')[0].getText().strip()
    print(location)
    print(time)
    print(info)
    print(weather + "°C")
    val = (location, time, info, weather)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234567890",
        database="test"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO  data(location, locationTime, info, weather) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

async def get_body(request: Request):
    return await request.body()

@app.get("/data")
def output_request(body=Depends(get_body)):
    print("New request arrived.")
    #time.sleep(5)
    print(body)
    return dict(myexample={'request': str(body, 'utf-8')})

@app.post("/data")
def input_request(body=Depends(get_body)):
    print("New request arrived.")
    print(str(body))
    #time.sleep(5)
    return dict(myexample={'request': str(body, 'utf-8')})

@app.get("/form")
def get_post(request: Request):
    return templates.TemplateResponse('form.html', context={'request': request})

@app.post("/form")
def form_post(request: Request, num: str = Form(...)):
    # result = spell_number(num)
    # num = num + " weather"

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234567890",
        database="test"
    )
    # weather(num)
    mycursor = mydb.cursor()
    sql_query = "SELECT weather FROM test.data WHERE location = %(location)s ORDER BY id DESC LIMIT 1"
    data_tuple = {"location": num}
    mycursor.execute(sql_query, data_tuple)


    myresult = mycursor.fetchone()[0]

    print("Have a Nice Day:)")

    # for x in myresult:
    #     x = str(x)
    # Visulizing Data using Matplotlib
    # creating the dataset
    data = {num: int(myresult)}
    courses = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(3, 4))

    # creating the bar plot
    plt.bar(courses, values, color='maroon',
            width=0.01)

    plt.xlabel("Courses offered")
    plt.ylabel(num)
    plt.title("Weather")
    plt.show()
    return templates.TemplateResponse('form.html', context={'request': request, 'result': myresult})
