import os
import shutil

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

print('input numero de catastro:\n')
numero_catastro = input()
if numero_catastro == '':
    numero_catastro = '07040A007000630'
posibles_catastros = ['1583813EE7218S', '07040A007000630', '07008A00900111', '07008A01300014']
years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]

def take_screenshot(year):

    # specific year
    year_to_click = driver.find_element(By.XPATH, "//span[text()=" + str(year) + "]")
    print(str(year) + ' init')
    year_to_click.click()
    time.sleep(5)

    # check if screenshot already exists, delete if it does
    screenshot_path = os.path.join(screenshot_directory, str(year) + "_" + numero_catastro + ".png")
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
        print(f"Existing screenshot deleted: {screenshot_path}")

    # save screenshot
    driver.save_screenshot(screenshot_path)
    print(str(year) + ' screenshot saved')

    time.sleep(1)



driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(2)

driver.fullscreen_window()

time.sleep(7)

# boton D'acord
try:
    dacord = driver.find_element(By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]')
    dacord.click()
    print('dacord')
except NoSuchElementException:
    print('dacord not found')

time.sleep(2)

# boton Cerca avançada
cercaimg = driver.find_element(By.XPATH, "//img[@class='icon' and contains(@src, '/visor/widgets/ideibLocate/images/icon.png?wab_dv=2.22')]")
cerca = cercaimg.find_element(By.XPATH, "./..")
print('cerca')
cerca.click()

time.sleep(2)

# tab Cadastre
cadastre = driver.find_element(By.XPATH, "//div[@label='Cadastre']")
cadastre.click()

time.sleep(2)

# Input referencia cadastral
input_cadastre = driver.find_element(By.XPATH, "//input[@id='RC']")
input_cadastre.clear()
print('input cadastre')
input_cadastre.send_keys(numero_catastro)

time.sleep(2)

# Cercar cadastre
cercar_cadastre = driver.find_element(By.XPATH, "//div[@data-dojo-attach-point='btnRefCat']")
print('cercar_cadastre')
cercar_cadastre.click()

time.sleep(2)

"""
# Tancar informacio - no parece necesario ya que se cierra con tancar cerca avançada
tancar_informacio = driver.find_element(By.XPATH, "//div[@title='Tanca']")
print('tancar_informacio')
tancar_informacio.click()

time.sleep(2)"""

# Tancar cerca avançada
tancar_cerca_avançada = driver.find_element(By.XPATH, "//div[@data-dojo-attach-point='closeNode']")
print('tancar_cerca_avançada')
tancar_cerca_avançada.click()

time.sleep(2)

# Zoom in
print('zoom')
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()

time.sleep(5)

# hide stuff
stuff_ids = [
    'themes_IDEIBTheme_widgets_AnchorBarController_Widget_20',
    'widgets_ideibSearch_Widget_22',
    'themes_IDEIBTheme_widgets_Header_Widget_21',
    'widgets_ZoomSlider_Widget_24',
    'widgets_ideibStreetView',
    'widgets_MyLocation_Widget_26',
    'widgets_ideibHomeButton_Widget_25',
    'widgets_ideibZoomExtent',
    'widgets_ZoomSlider_Widget_24',
    'dijit__WidgetBase_2',
    'esri_dijit_OverviewMap_1'
         ]

for i in stuff_ids:
    stuff_to_hide = driver.find_element(By.ID, i)
    driver.execute_script("arguments[0].style.display = 'none';", stuff_to_hide)
    print('hide ' + i)

# hide left column
print('hide left column')
left_column = driver.find_element(By.CSS_SELECTOR, ".bar.max")
left_column.click()
left_column.click()

# create screenshot directory
project_root = os.getcwd()
screenshots_root = os.path.join(project_root, "screenshots")
if not os.path.exists(screenshots_root):
    os.mkdir(screenshots_root)
screenshot_directory = os.path.join(screenshots_root, numero_catastro)
if os.path.exists(screenshot_directory):
    shutil.rmtree(screenshot_directory)
    print(f"Existing directory deleted: {screenshot_directory}")
os.mkdir(screenshot_directory)

# screenshot now
screenshot_path = os.path.join(screenshot_directory, "now_" + numero_catastro + ".png")
if os.path.exists(screenshot_path):
    os.remove(screenshot_path)
    print(f"Existing screenshot deleted: {screenshot_path}")
driver.save_screenshot(screenshot_path)
print('screenshot saved')

time.sleep(5)

# year_select
year_select = driver.find_element(By.XPATH, "//img[@alt='Fotografies històriques de totes les illes']")
year_select.click()

time.sleep(4)

# take screenshots for other years
for i in years_to_screenshot:
    take_screenshot(i)



time.sleep(5)

print('quit')
driver.quit()