from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
import time

numero_catastro = "07040A007000630"

driver = webdriver.Chrome()

driver.get("https://ideib.caib.es/visor/")

time.sleep(7)

# Zoom in
actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()

time.sleep(5)

driver.quit()