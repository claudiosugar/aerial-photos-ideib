from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

numero_catastro = "07040A007000630"

driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(7)

# Zoom in

mc = driver.find_element(By.CSS_SELECTOR, '.esriMapContainer')
mc1 = mc.size()


time.sleep(5)

driver.quit()