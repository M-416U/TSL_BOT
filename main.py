import threading, time
import tkinter as tk
import customtkinter as CTK
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

CTK.set_appearance_mode("dark")

# Sets the color of the widgets
# Supported themes: green, dark-blue, blue
CTK.set_default_color_theme("blue")

app = CTK.CTk()
app.geometry("775x520")
app.title("TLS_Bot")

states = [
    'Agadir', 'Casablanca', 'Fes', 'Marrakech', 'Oujda', 'Rabat', 'Tanger'
]

states_nk = {
    "Agadir": "AGA",
    "Casablanca": "CAS",
    "Fes": "FEZ",
    "Marrakech": "RAK",
    "Oujda": "OUD",
    "Rabat": "RBA",
    "Tanger": "TNG"
}


def toggle_password():
  if password_entry.cget('show') == '':
    password_entry.configure(show='*')
    toggle_pass.configure(text='show')
  else:
    password_entry.configure(show='')
    toggle_pass.configure(text='hide')

def generet_link():
  st = ''
  if to.get() == 'france':
    st = 'fr'
  else:
    st = 'de'

  list_box.configure(state='normal')
  link = f"https://visas-{st}.tlscontact.com/appointment/ma/ma{states_nk[state.get()]}2{st}/{id_entry.get() or 1344474}"
  list_box.insert(tk.END, '\nAutomation started....:\n')
  list_box.insert(tk.END, '\n----------------------------------------\n')
  list_box.insert(tk.END,link)
  list_box.insert(tk.END, '\n----------------------------------------\n')
  list_box.configure(state='disabled')
  return link



frame = CTK.CTkFrame(master=app, border_width=1)
frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.S)

title = CTK.CTkLabel(text='TLS_Bot',
                     master=frame,
                     font=('tahoma', 25),
                     pady=20)
title.grid(row=0, column=0, columnspan=2)

email_label = CTK.CTkLabel(text="Email:", master=frame, padx=10, pady=15)
email_label.grid(row=1, column=0)

email_entry = CTK.CTkEntry(master=frame, width=600)
email_entry.grid(row=1, column=1)

password_label = CTK.CTkLabel(text="Password:", master=frame, padx=10, pady=15)
password_label.grid(row=2, column=0)

password_entry = CTK.CTkEntry(master=frame, width=600, show='*')
password_entry.grid(row=2, column=1)

id_label = CTK.CTkLabel(text="Group ID:", master=frame, padx=10, pady=15)
id_label.grid(row=3, column=0)

id_entry = CTK.CTkEntry(master=frame, width=600)
id_entry.grid(row=3, column=1)

toggle_pass = CTK.CTkButton(master=frame,
                            text='show',
                            width=100,
                            command=toggle_password)
toggle_pass.grid(row=2, column=2)

state = CTK.CTkComboBox(master=frame, values=states, width=350)
state.grid(row=5, column=1, columnspan=2)

to = CTK.CTkComboBox(master=frame, values=['france', 'germany'], width=350)
to.grid(row=4, column=1, columnspan=2)

t_frame = CTK.CTkFrame(master=frame)
t_frame.grid(row=6, column=0, columnspan=2)

min = CTK.CTkEntry(master=t_frame,width=150)
min.grid(row=0,column=0)

sec = CTK.CTkEntry(master=t_frame,width=150)
sec.grid(row=1,column=1)

min_value = min.get()
sec_value = sec.get()
total_time = 30
if min_value and sec_value:  # Check if both fields are non-empty
    total_time_sleep = (int(min_value) * 60) + int(sec_value)
def login_bot():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_extension('proxy.crx')
    driver = uc.Chrome(options=options)
    driver.get(generet_link())
    driver.implicitly_wait(2.5)
    e = driver.find_element(by=By.ID, value='username')
    e.send_keys(email_entry.get())

    driver.implicitly_wait(2)
    p = driver.find_element(by=By.ID, value='password')
    p.send_keys(password_entry.get())
    driver.implicitly_wait(2)
    log_btn = driver.find_element(by=By.ID, value='kc-login')
    log_btn.click()
    max_attempts = 3
    current_attempt = 1
    while current_attempt <= max_attempts:
        try:
            # Find and click the button
            wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
            reg = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[3]/button')))
            driver.execute_script("arguments[0].scrollIntoView();", reg)
            # Click the element
            reg.click()

            # If the click is successful, break out of the loop
            print("Successfully clicked the button.")
            break
        except EC.NoSuchElementException:
            print(f"Button not found. Attempt {current_attempt}/{max_attempts}")
            current_attempt += 1
            if current_attempt <= max_attempts:
                # Sleep and refresh the page for the next attempt
                time.sleep(int(total_time))  # Sleep for 5 seconds (adjust as needed)
                driver.refresh()
            else:
                print("Max retry attempts reached. Exiting loop.")
                break
    #

selenium_Thread = threading.Thread(target=login_bot)
def main():
        selenium_Thread.start()
        if selenium_Thread.is_alive():
            list_box.insert(tk.END, 'Automation started')
#run the script
run_btn = CTK.CTkButton(master=frame,
                        text='R U N',
                        width=600,
                        command=main,
                        state='normal')
run_btn.grid(row=7, column=0, columnspan=2)

list_box = CTK.CTkTextbox(master=frame,
                          width=550,
                          height=250,
                          state='disabled',
                          border_spacing=0)
list_box.grid(row=8, column=0, columnspan=2)

app.mainloop()