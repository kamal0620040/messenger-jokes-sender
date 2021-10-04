from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests

# Getting Facebook email and password form .env
try:
    config = dotenv_values(".env")
except:
    print("Make sure you have .env file in the same directory where this program is present")
    quit()
    
# Checking weather .env file contains required environment variable fields or not
if not 'FACEBOOK_EMAIL' in config.keys() or not 'FACEBOOK_PASSWORD' in config.keys():
    print("Your .env file doesnot contains the required parameter.")
    quit()

# Getting required Information form user
groupId = input("Enter Messenger group/chat ID::")
noOfJokes = int(input("Enter The number of jokes to send::"))

# Start the local session for firefox
try:
    driver = webdriver.Firefox()
except:
    print("Make sure you have correctly configured Firefox gecodriver.")
    quit()

# Log In into facebook
try:
    driver.get("https://www.facebook.com/")
    time.sleep(5)
    email = driver.find_element_by_xpath("//div/input[@id='email']")
    email.send_keys(config['FACEBOOK_EMAIL'])
    email.send_keys(Keys.TAB)
    time.sleep(3)
    password = driver.find_element_by_xpath("//div/input[@id='pass']")
    password.send_keys(config['FACEBOOK_PASSWORD'])
    password.send_keys(Keys.RETURN)
    time.sleep(10)
except:
    print("Something went wrong while logging into facebook.")
    driver.quit()
    quit()

# Opens messenger group/chat
try:
    driver.get("https://www.messenger.com/t/"+groupId)
    time.sleep(5)
    driver.find_element_by_xpath("//div/button[@type='submit']").click()
    time.sleep(15)
    # Select the messenger Input Field
    message = driver.find_element_by_xpath("//div[@class='_1mf _1mj']")
    message.click()
except:
    print("Something went wrong while opening messenger. Please check your credential and Check weather the group/chat ID is correct or not.")
    driver.quit()
    quit()

# sends Jokes until it comes out of while loop
print("On Progress...")
number = 1
while number <= noOfJokes:
    try:
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
    except:
        print("Error with jokeAPI")
        driver.quit()
        quit()

    if 'setup' in response.json():
        x = driver.switch_to.active_element
        time.sleep(1)
        x.send_keys("Number ",number)
        x.send_keys(Keys.RETURN)
        time.sleep(1)
        x.send_keys(response.json()['setup'])
        x.send_keys(Keys.RETURN)
        time.sleep(1)
        x.send_keys(response.json()['delivery'])
        x.send_keys(Keys.RETURN)
        number = number+1
        time.sleep(15)
    else:
        # print(response.json()['joke'])
        x = driver.switch_to.active_element
        time.sleep(1)
        x.send_keys("Number ",number)
        x.send_keys(Keys.RETURN)
        time.sleep(1)
        x.send_keys(response.json()['joke'])
        x.send_keys(Keys.RETURN)
        number = number+1
        time.sleep(15)


# Displaying end message
print('Sent ',noOfJokes,' joke successfully!!')
driver.quit()