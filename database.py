from bs4 import BeautifulSoup
import requests
import mysql.connector

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


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

city = input("Enter the Name of City ->  ")
city = city + " weather"
weather(city)
print("Have a Nice Day:)")



# This code is contributed by adityatri

