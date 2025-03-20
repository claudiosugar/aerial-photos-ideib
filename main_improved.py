import os
import shutil
import time
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def initialize_driver():
    driver = webdriver.Chrome()
    driver.get("https://ideib.caib.es/visor/")
    driver.fullscreen_window()
    return driver

def accept_initial_modal(driver):
    try:
        dacord = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]'))
        )
        dacord.click()
        print("D'acord button clicked.")
    except TimeoutException:
        print("D'acord button not found.")

def navigate_to_advanced_search(driver):
    try:
        cercaimg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@class='icon' and contains(@src, '/visor/widgets/ideibLocate/images/icon.png?wab_dv=2.22')]"))
        )
        cerca = cercaimg.find_element(By.XPATH, "./..")
        cerca.click()
        print('Advanced search opened.')
    except TimeoutException:
        print('Advanced search button not found.')

def enter_cadastral_reference(driver, numero_catastro):
    try:
        cadastre = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@label='Cadastre']"))
        )
        cadastre.click()

        input_cadastre = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='RC']"))
        )
        input_cadastre.clear()
        input_cadastre.send_keys(numero_catastro)
        cercar_cadastre = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-dojo-attach-point='btnRefCat']"))
        )
        cercar_cadastre.click()
        print('Cadastral reference entered and searched.')
        close_advanced_search(driver)
    except TimeoutException:
        print('Failed to enter cadastral reference.')

def close_advanced_search(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-dojo-attach-point='closeNode']"))
        )
        close_button.click()
        tancar_informacio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Tanca']"))
        )
        tancar_informacio.click()
        print('Advanced search and information modal closed.')
    except TimeoutException:
        print('Failed to close advanced search and information modal.')

def close_left_column(driver):
    try:
        # Locate the left column by its class, which is assumed to be 'bar max' from the previous descriptions
        left_column = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".bar.max"))
        )
        # Perform two clicks to close/minimize the left column
        time.sleep(0.5)
        left_column.click()  # First click
        time.sleep(0.5)  # Wait a bit before the second click to ensure UI responsiveness
        left_column.click()  # Second click
        print("Left column closed/minimized.")
    except TimeoutException:
        print("Failed to close/minimize left column.")

def hide_ui_elements(driver):
    stuff_ids = [
        'themes_IDEIBTheme_widgets_AnchorBarController_Widget_20', 'widgets_ideibSearch_Widget_22',
        'themes_IDEIBTheme_widgets_Header_Widget_21', 'widgets_ZoomSlider_Widget_24',
        'widgets_ideibStreetView', 'widgets_MyLocation_Widget_26',
        'widgets_ideibHomeButton_Widget_25', 'widgets_ideibZoomExtent',
        'widgets_ZoomSlider_Widget_24', 'dijit__WidgetBase_2', 'esri_dijit_OverviewMap_1'
    ]
    for i in stuff_ids:
        try:
            stuff_to_hide = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, i))
            )
            driver.execute_script("arguments[0].style.display = 'none';", stuff_to_hide)
            print('Hidden:', i)
        except TimeoutException:
            print('Failed to hide:', i)

def zoom_in(driver):
    actions = ActionChains(driver)
    for _ in range(3):  # Perform zoom in three times
        actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
    print('Zoomed in.')

def setup_screenshot_directory(numero_catastro):
    project_root = os.getcwd()
    screenshots_root = os.path.join(project_root, "screenshots")
    if not os.path.exists(screenshots_root):
        os.mkdir(screenshots_root)
    screenshot_directory = os.path.join(screenshots_root, numero_catastro)
    if os.path.exists(screenshot_directory):
        shutil.rmtree(screenshot_directory)
    os.mkdir(screenshot_directory)
    print(f"Screenshot directory prepared: {screenshot_directory}")
    return screenshot_directory

def take_screenshot(driver, screenshot_directory, identifier, numero_catastro):
    screenshot_path = os.path.join(screenshot_directory, f"{identifier}_{numero_catastro}.png")
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
    driver.save_screenshot(screenshot_path)
    print(f'Screenshot for {identifier} saved.')

def start_gui():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    numero_catastro = simpledialog.askstring("Input", "Enter numero de catastro:")

    if numero_catastro:
        main(numero_catastro)

def main(numero_catastro):
    # numero_catastro = input() or '07040A007000630'
    years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]

    driver = initialize_driver()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))  # Wait for page to load
    accept_initial_modal(driver)
    navigate_to_advanced_search(driver)
    enter_cadastral_reference(driver, numero_catastro)
    hide_ui_elements(driver)
    zoom_in(driver)  # Perform zoom in operation
    close_left_column(driver)

    screenshot_directory = setup_screenshot_directory(numero_catastro)

    # Screenshot the current state
    time.sleep(5)
    take_screenshot(driver, screenshot_directory, "now", numero_catastro)

    # Prepare for historical screenshots
    year_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@alt='Fotografies històriques de totes les illes']"))
    )
    year_select.click()

    for year in years_to_screenshot:
        # Navigate to the year
        try:
            year_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{year}']"))
            )
            year_element.click()
            print(f"Year {year} selected.")
            # Wait for the image or map to load
            time.sleep(5)
            take_screenshot(driver, screenshot_directory, str(year), numero_catastro)
        except TimeoutException:
            print(f"Failed to find or select year {year}.")

    driver.quit()

if __name__ == "__main__":
    start_gui()
