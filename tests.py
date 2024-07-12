from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

numero_catastro = "07040A007000630"

driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(7)

# Zoom in

# boton D'acord
try:
    dacord = driver.find_element(By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]')
    dacord.click()
    print('dacord')
except NoSuchElementException:
    print('dacord not found')

time.sleep(2)

# hide left column
print('hide left column')
left_column = driver.find_element(By.CSS_SELECTOR, ".bar.max")
print(left_column.get_attribute('outerHTML'))
left_column.click()

time.sleep(5)

driver.quit()
