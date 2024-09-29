import undetected_chromedriver as webdriver1
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException, TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import io
import requests as r
import pandas as pd
import time
import re

class Scraping_Maps:
    def __init__(self, url):
        service = Service()
        self.load_Pref(service, url)

    def load_Pref(self, service, url):
        try:
            options = webdriver1.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
        #        options.add_argument('--headless')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-notifications')
            options.add_argument('--autoplay-policy=user-gesture-required')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-save-password-bubble')
            chrome_prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", chrome_prefs)
            driver = webdriver1.Chrome(service=service, options=options)
        except:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
        #        options.add_argument('--headless')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-notifications')
            options.add_argument('--autoplay-policy=user-gesture-required')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-save-password-bubble')
            chrome_prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", chrome_prefs)
            driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        self.scraping(url, driver)
        
    
    def scraping(self, url, driver):
        lista_titulo=[]
        lista_calificacion=[]
        lista_direccion=[]
        lista_telefono=[]
        lista_valor_estimado=[]
        lista_url=[]
        lista_caracteristicas=[]
        all_elements = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        time.sleep(3)
        first_position = driver.find_element(By.CSS_SELECTOR, "div[role='feed']>div>div[jsaction]:not([arial-label])")
        time.sleep(5)
        while True:
            driver.execute_script("arguments[0].scrollBy(0, 500);", all_elements)
            try:
                finish = driver.find_element(By.XPATH, "//span[contains(text(), 'No hay más resultados.')]")
                break
            except NoSuchElementException:
                pass
            time.sleep(5)
        elements = driver.find_elements(By.CSS_SELECTOR, "div[role='feed']>div>div[jsaction]:not([aria-label])") #Excluimos un area
        driver.execute_script("return arguments[0].scrollIntoView(true);", first_position) #Acemos scroll a primer lugar
        time.sleep(4)
        for element in elements:
            element.click()
            time.sleep(5)
            #wait for the card to appear
            new_card = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main'][aria-label]")))
            try:
                titulo = new_card.find_element(By.TAG_NAME, 'h1').text
                titulo = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", titulo)
            except NoSuchElementException:
                titulo = 0
            try:
                calificacion = new_card.find_element(By.CSS_SELECTOR, "div[jslog]>span>span[aria-hidden]").text
                calificacion = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", calificacion)
            except NoSuchElementException:
                calificacion = "No indicado"
            try:
                direccion = new_card.find_element(By.CSS_SELECTOR, "button[data-item-id='address']").text
                direccion = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", direccion)
            except NoSuchElementException:
                direccion="No indicado"
            try:
                telefono = new_card.find_element(By.CSS_SELECTOR, "button[data-item-id*='phone']").text
                telefono = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", telefono)
            except NoSuchElementException:
                telefono="No indicado"
            try:
                valor_estimado = new_card.find_element(By.CSS_SELECTOR, "div[jsaction][jsname][aria-controls]>div").text
                valor_estimado = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", valor_estimado)
            except NoSuchElementException:
                valor_estimado="No indicado"
            try:
                url = new_card.find_element(By.CSS_SELECTOR, "a[jsaction][data-item-id]").get_attribute('href')
            except NoSuchElementException:
                url=0
            try:
                caracteristicas = new_card.find_element(By.CSS_SELECTOR, "div[role][aria-label]>button[jslog][jsaction]>div>div>div[jslog]").text
                caracteristicas = re.sub(r"[^a-zA-Z0-9/#':.-]", " ", caracteristicas)
            except NoSuchElementException:
                caracteristicas=0
            lista_titulo.append(titulo)
            lista_calificacion.append(calificacion)
            lista_direccion.append(direccion)
            lista_telefono.append(telefono)
            lista_valor_estimado.append(valor_estimado)
            lista_url.append(url)
            lista_caracteristicas.append(caracteristicas)
        df = pd.DataFrame({"titulo":lista_titulo, "calificacion":lista_calificacion, "direccion":lista_direccion, "telefono":lista_telefono, "valor_estimado":lista_valor_estimado, "url":lista_url, "caracteristicas":lista_caracteristicas})
        df.to_csv("maps.csv", encoding='latin-1', sep ="!")
        driver.quit()