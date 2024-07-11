import os
import shutil

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

numero_catastro = ("07040A007000630")
years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]

def take_screenshot(year):

    # specific year
    year_to_click = driver.find_element(By.XPATH, "//span[text()=" + str(year) + "]")
    print(year)
    year_to_click.click()
    time.sleep(3)

    # check if screenshot already exists, delete if it does
    screenshot_path = os.path.join(screenshot_directory, numero_catastro + "_" + str(year) + ".png")
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        print(f"Existing screenshot deleted: {screenshot_path}")

    # save screenshot driver.save_screenshot(screenshot_path, map_container_x, map_container_y, map_container_width, map_container_height)
    print('screenshot saved')

    time.sleep(1)



driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(2)

driver.maximize_window()

time.sleep(7)

# boton D'acord
dacord = driver.find_element(By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]')
print('dacord')
dacord.click()

time.sleep(3)

# boton Cerca avançada
cercaimg = driver.find_element(By.XPATH, "//img[@class='icon' and contains(@src, '/visor/widgets/ideibLocate/images/icon.png?wab_dv=2.22')]")
cerca = cercaimg.find_element(By.XPATH, "./..")
print('cerca')
cerca.click()

time.sleep(3)

# tab Cadastre
cadastre = driver.find_element(By.XPATH, "//div[@label='Cadastre']")
cadastre.click()

time.sleep(3)

# Input referencia cadastral
input_cadastre = driver.find_element(By.XPATH, "//input[@id='RC']")
input_cadastre.clear()
print('input cadastre')
input_cadastre.send_keys(numero_catastro)

time.sleep(3)

# Cercar cadastre
cercar_cadastre = driver.find_element(By.XPATH, "//div[@data-dojo-attach-point='btnRefCat']")
print('cercar_cadastre')
cercar_cadastre.click()

time.sleep(3)

# Tancar informacio
tancar_informacio = driver.find_element(By.XPATH, "//div[@title='Tanca']")
print('tancar_informacio')
tancar_informacio.click()

time.sleep(3)

# Tancar cerca avançada
tancar_cerca_avançada = driver.find_element(By.XPATH, "//div[@data-dojo-attach-point='closeNode']")
print('tancar_cerca_avançada')
tancar_cerca_avançada.click()

time.sleep(3)

# Zoom in
print('zoom')
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()

time.sleep(5)

# create screenshot_directory
project_root = os.getcwd()
screenshot_directory = os.path.join(project_root, "screenshots", numero_catastro)
if os.path.exists(screenshot_directory):
    shutil.rmtree(screenshot_directory)
    print(f"Existing directory deleted: {screenshot_directory}")
os.mkdir(screenshot_directory)

# screenshot now
screenshot_path = os.path.join(screenshot_directory, numero_catastro + "_now.png")
if os.path.exists(screenshot_path):
    os.remove(screenshot_path)
    print(f"Existing screenshot deleted: {screenshot_path}")
driver.save_screenshot(screenshot_path)
print('screenshot saved')

time.sleep(3)

# year_select
year_select = driver.find_element(By.XPATH, "//img[@alt='Fotografies històriques de totes les illes']")
year_select.click()

time.sleep(3)

# take screenshots for other years
for i in years_to_screenshot:
    take_screenshot(i)



time.sleep(5)

print('quit')
driver.quit()