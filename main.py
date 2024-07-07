from selenium import webdriver
from selenium.webdriver.common.by import By
import time

numero_catastro = "07040A007000630"

driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(5)

driver.maximize_window()

time.sleep(3)

# boton D'acord
dacord = driver.find_element(By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]')
dacord.click()

time.sleep(3)

# boton Cerca avançada
cercaimg = driver.find_element(By.XPATH, "//img[@class='icon' and contains(@src, '/visor/widgets/ideibLocate/images/icon.png?wab_dv=2.22')]")
cerca = cercaimg.find_element(By.XPATH, "./..")
cerca.click()

time.sleep(3)

# tab Cadastre
cadastre = driver.find_element(By.XPATH, "//div[@label='Cadastre']")
cadastre.click()

time.sleep(3)

# Input referencia cadastral
input_cadastre = driver.find_element(By.XPATH, "//input[@id='RC']")
input_cadastre.clear()
input_cadastre.send_keys(numero_catastro)

time.sleep(3)
# Cercar cadastre
cercar_cadastre = driver.find_element(By.XPATH, "//input[@id='RC']/..")
print(cercar_cadastre)
cercar_cadastre.click()

time.sleep(5)

driver.quit()