import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#funtion to get weather information from Openweather API
def get_weather(city):
    API_key="fbae904aa47c42507b829cb6b45e32eb" 
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res= requests.get(url)  
    
    if res.status_code== 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    #Parse the response JSON to get weather information
    weather = res.json()
    icon_id= weather['weather'][0]['icon']
    temp= weather['main']['temp']- 273.15
    desc= weather['weather'][0]['description']
    city=weather['name']
    country= weather['sys']['country']
    
    
    #get the icon URL and return all the weather info 
    icon_url=f" https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return(icon_url, temp, desc, city, country)
    


#Funtion to search weather for a city
def search():
    city= city_entry.get()
    result= get_weather(city)
    if result is None:
        return 
    
    #if the city is found, unpack the weather info
    icon_url, temp, desc, city, country= result
    location_label.configure(text=f"{city}, {country}")
    
    
    #Get the weather icon image from the URL and update icon label
    image= Image.open(requests.get(icon_url, stream=True).raw)
    icon= ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image= icon


#update the temperature and description labels
    temp_label.configure(text=f"Temperature: {temp:.2f}°C") 
    desc_label.configure(text=f"Description: {desc}")   
    


canvas= ttkbootstrap.Window(themename="morph")
canvas.title("Weather App")
canvas.geometry("600x600")



#Entry Widget -> to enter the cityname
city_entry= ttkbootstrap.Entry(canvas, font="Helvetica, 18")
city_entry.pack(pady=10)

#button widget -> to search for the weather info
search_button= ttkbootstrap.Button(canvas, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

#label widget -> to show the city/countryname
location_label = tk.Label(canvas, font="Helvetica 25")
location_label.pack(pady=20)
#location_label.place(x= 205,y=300)


#label widget -> to show the weather icon
icon_label =tk.Label(canvas)
icon_label.pack()

#label widget -> to show the temperature
temp_label= tk.Label(canvas, font="Helvetica, 20")
temp_label.pack()

#label widget -> to show the weather description
desc_label= tk.Label(canvas, font="Helvetica, 20")
desc_label.pack()

canvas.mainloop()

