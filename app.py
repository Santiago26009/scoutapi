from flask import Flask, request, Response, jsonify
from flask_httpauth import HTTPBasicAuth
import json
from selenium.webdriver.opera.options import Options 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException 
from selenium import webdriver 
import time
from time import sleep 

def getDriverEdge():
    try:  
        # Driver Code
        # create object
        driver = webdriver.Edge(r'C:\Users\Santi\Downloads\ScoutGirls\ScoutAPI\msedgedriver.exe')
        driver.get ("https://digitalcookie.girlscouts.org/scout/ava892356")
        resultado = Selenium(driver)
        
    except Exception as browser_Error:
        print('The automation cannot find website, error:  ', browser_Error)
        resultado = ["2","0","0"]

    finally:
        print (resultado)
        if (resultado[0] == '1'):
            mess = "Website ok"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '2'):
            mess = "Website down"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '3'):
            mess = "Cannot find some element in in cookie selection"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '4'):
            mess = "Cannot find some element in checkout process"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front

# Open website in Chrome
def getDriverChrome():
    try:  
        # Driver Code
        # create object
        driver = webdriver.Chrome(r'C:\Users\Santi\Downloads\ScoutGirls\ScoutAPI\chromedriver.exe')
        driver.get ("https://digitalcookie.girlscouts.org/scout/ava892356")
        resultado = Selenium(driver)
             
    except Exception as browser_Error:
        print('The automation cannot find website, error:  ', browser_Error)
        resultado = ["2","0","0"]

    finally:
        print (resultado)
        if (resultado[0] == '1'):
            mess = "Website ok"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '2'):
            mess = "Website down"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '3'):
            mess = "Cannot find some element in in cookie selection"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front
        if (resultado[0] == '4'):
            mess = "Cannot find some element in checkout process"
            back = resultado[1]
            front = resultado[2]
            return mess, back, front

# Steps for Selenium
def Selenium(driver):
    
        for entry in driver.get_log('browser'):
                print(entry)

        navigationStart = driver.execute_script("return window.performance.timeOrigin")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")

        backendPerformance = int(responseStart) - int(navigationStart)
        frontendPerformance = int(domComplete) - int(responseStart)
        print ("Main Page")
        print ("Back End: %s ms" % backendPerformance)
        print ("Front End: %s ms" % frontendPerformance)
        
        try:
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie2Input\"]")
            element.send_keys(2)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie3Input\"]")
            element.send_keys(3)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie4Input\"]")
            element.send_keys(4)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie5Input\"]")
            element.send_keys(5)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie6Input\"]")
            element.send_keys(6)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie7Input\"]")
            element.send_keys(7)
            element=driver.find_element(By.XPATH,"//*[@id=\"cookie9Input\"]")
            element.send_keys(9)
            element=driver.find_element(By.XPATH,"//*[@id=\"donateInput\"]")
            element.send_keys(9)
            time.sleep(5)
            element=driver.find_element(By.XPATH,"//*[@id=\"delivery-method-in-person\"]/div/div[3]/label")
            element.click()            
            time.sleep(5)
            element=driver.find_element(By.XPATH,"//*[@id=\"landingform\"]/div/div[2]/div[3]/div[5]/button")
            element.click()
            time.sleep(5) 
            try:
              
                time.sleep(5) 
                element=driver.find_element(By.XPATH,"//*[@id=\"phone\"]")
                element.send_keys(555555555)
                time.sleep(8) 
                element=driver.find_element(By.XPATH,"//*[@id=\"firstName\"]")  
                element.send_keys("Monitor")
                time.sleep(8)
                element=driver.find_element(By.XPATH,"//*[@id=\"deliveryAddressForm\"]/div/div/div[10]/div/button") 
                element.click()
                time.sleep(8)
                return ["1", backendPerformance,frontendPerformance]
        
            except Exception as findElementCheckProcess_Error:
                print('The automation cannot find some element, error:  ', findElementCheckProcess_Error)
                return ("4", backendPerformance,frontendPerformance)
            
        except Exception as findElementCookieSelection_Error:
            print('The automation cannot find some element, error:  ', findElementCookieSelection_Error)
            return ("3", backendPerformance,frontendPerformance)              

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if (username == "scoutgirl01" and password == "MyP4$sw0rD"):
        return True
    return False

@app.route("/api/scoutgirls/validations/", methods=['POST'])
@auth.login_required
def main():
    data = request.json
    nav = data["nav"]
    mess="Incorrect browser"
    if (nav == "edge"):
        mess, back, front = getDriverEdge()
    if (nav == "chrome"):
        mess, back, front = getDriverChrome()
    if (mess=="Website down"):
        result = {'Status Code': 200, 'Message': 'This website cannot be accessed', 'Response Time (sec)': -1}
        result_json = json.dumps(result)
        return result_json
    if (mess=="Website ok"):
        totaltime = back + front
        if (totaltime>10000):
            result = {'Status Code': 200, 'Message': 'Response time greater than 10 seconds', 'Response Time (sec)': totaltime/1000}
            result_json = json.dumps(result)
            return result_json
        else:
            result = {'Status Code': 200, 'Message': 'Warning', 'Response Time (sec)': totaltime/1000}
            result_json = json.dumps(result)
            return result_json
    if (mess=="Cannot find some element in cookie selection"):
        totaltime = back + front
        result = {'Status Code': 200, 'Message': mess, 'Response Time (sec)': totaltime/1000}
        result_json = json.dumps(result)
        return result_json
    if (mess=="Cannot find some element in checkout process"):
        result = {'Status Code': 200, 'Message': mess, 'Response Time (sec)': totaltime/1000}
        result_json = json.dumps(result)
        return result_json
    result = {'Status Code': 200, 'Message': mess, 'Response Time (sec)': -1}
    result_json = json.dumps(result)
    return result_json

app.run(port=3001, host="0.0.0.0", debug=True)
