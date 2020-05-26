"""This is a Graphic User Interface (GUI) that tells the user
   coronavirus information by zip code.
   Source Data: DataSF, 'Map of Rate of CVID-19 Cases by ZIP Code'
   """

import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
import pandas as pd
from sodapy import Socrata


HEIGHT = 700
WIDTH = 800

#store user entry temporarily
def test_function(entry):
    print("This is the ZIP Code: ", entry)


def get_covid_data(zip):
    #Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.sfgov.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.sfgov.org,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("favi-qct6", zip_code=zip, limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    #user enters invalid zipcode
    if len(results)==0:
        label['text'] = ""
        label2['text'] = ""
        label3['text'] = "No results for ZIP code " + "'" + str(zip) + "'" + " \n\nPlease enter valid San Francisco ZIP code."
        label4['text'] = ""
        label5['text'] = ""

    else:
        label['text'] = "As of " + results[0]['data_as_of']
        label2['text'] = "For ZIP Code: " + results[0]['zip_code']
        label3['text'] = "No. of Cases: " + results[0]['count']
        label4['text'] = "Population Size (2017 Census estimate): "+ results[0]['acs_population']
        label5['text'] = "Estimated Rate of Cases (per 10k): " + results[0]['rate']


#makes the frame
root = tk.Tk()
root.title('Enter San Francisco Zip Code')

#adjust widget size
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#import background image
background_image = ImageTk.PhotoImage(Image.open('background_4.png'))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

#create top frame
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.1, anchor='n')

#create entry box
entry = tk.Entry(frame, bg='white', font=('Courier', 25))
entry.place(relwidth=0.65, relheight=1)

#create button
my_Font = font.Font(weight="bold", size=25)
button = tk.Button(frame, text="Show Result", bg='#cccccc', command=lambda: get_covid_data(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1) #adjust button size and position
button['font'] = my_Font

#create lower frame
lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#create label
label = tk.Label(lower_frame, font=('Arial', 18))
label.place(relwidth=1, relheight=0.2)
label2 = tk.Label(lower_frame, font=('Arial', 18))
label2.place(rely=0.2, relwidth=1, relheight=0.2)
label3 = tk.Label(lower_frame, font=('Arial', 18))
label3.place(rely=0.4, relwidth=1, relheight=0.2)
label4 = tk.Label(lower_frame, font=('Arial', 18))
label4.place(rely=0.6, relwidth=1, relheight=0.2)
label5 = tk.Label(lower_frame, font=('Arial', 17))
label5.place(rely=0.8, relwidth=1, relheight=0.2)

root.mainloop()
