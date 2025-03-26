import os
import shutil
import time
import zipfile
from io import BytesIO
from flask import Flask, send_file, render_template, Response
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from queue import Queue
import json

app = Flask(__name__)
progress_queues = {}

def send_progress(queue, message):
    if queue:
        queue.put(message)
    print(message)  # Keep console logging too

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://ideib.caib.es/visor/")
        return driver
    except Exception as e:
        print(f"Failed to initialize Chrome driver: {str(e)}")
        # Try with explicit ChromeDriverManager
        try:
            service = Service(ChromeDriverManager(cache_valid_range=1).install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get("https://ideib.caib.es/visor/")
            return driver
        except Exception as e:
            print(f"Failed to initialize Chrome driver with ChromeDriverManager: {str(e)}")
            raise

def accept_initial_modal(driver, queue=None):
    try:
        dacord = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="widgets_ideibSplash_Widget_28"]/div[2]/div[2]/div[3]/div[2]'))
        )
        dacord.click()
        send_progress(queue, "D'acord button clicked.")
    except TimeoutException:
        send_progress(queue, "D'acord button not found.")

def navigate_to_advanced_search(driver, queue=None):
    try:
        cercaimg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@class='icon' and contains(@src, '/visor/widgets/ideibLocate/images/icon.png?wab_dv=2.22')]"))
        )
        cerca = cercaimg.find_element(By.XPATH, "./..")
        cerca.click()
        send_progress(queue, 'Advanced search opened.')
    except TimeoutException:
        send_progress(queue, 'Advanced search button not found.')

def enter_cadastral_reference(driver, numero_catastro, queue=None):
    try:
        cadastre = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@label='Cadastre']"))
        )
        cadastre.click()
        send_progress(queue, 'Cadastre tab selected.')

        input_cadastre = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='RC']"))
        )
        input_cadastre.clear()
        input_cadastre.send_keys(numero_catastro)
        send_progress(queue, f'Cadastral reference {numero_catastro} entered.')
        
        cercar_cadastre = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-dojo-attach-point='btnRefCat']"))
        )
        cercar_cadastre.click()
        send_progress(queue, 'Search initiated.')
        close_advanced_search(driver, queue)
    except TimeoutException:
        send_progress(queue, 'Failed to enter cadastral reference.')

def close_advanced_search(driver, queue=None):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-dojo-attach-point='closeNode']"))
        )
        close_button.click()
        tancar_informacio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='Tanca']"))
        )
        tancar_informacio.click()
        send_progress(queue, 'Advanced search and information modal closed.')
    except TimeoutException:
        send_progress(queue, 'Failed to close advanced search and information modal.')

def close_left_column(driver, queue=None):
    try:
        left_column = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".bar.max"))
        )
        time.sleep(0.5)
        left_column.click()
        time.sleep(0.5)
        left_column.click()
        send_progress(queue, "Left column closed/minimized.")
    except TimeoutException:
        send_progress(queue, "Failed to close/minimize left column.")

def hide_ui_elements(driver, queue=None):
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
            send_progress(queue, f'Hidden: {i}')
        except TimeoutException:
            send_progress(queue, f'Failed to hide: {i}')

def zoom_in(driver, queue=None):
    actions = ActionChains(driver)
    for _ in range(3):
        actions.key_down(Keys.CONTROL).send_keys(Keys.ADD).key_up(Keys.CONTROL).perform()
    send_progress(queue, 'Zoomed in.')

def setup_screenshot_directory(numero_catastro):
    project_root = os.getcwd()
    screenshots_root = os.path.join(project_root, "screenshots")
    if not os.path.exists(screenshots_root):
        os.mkdir(screenshots_root)
    screenshot_directory = os.path.join(screenshots_root, numero_catastro)
    if os.path.exists(screenshot_directory):
        shutil.rmtree(screenshot_directory)
    os.mkdir(screenshot_directory)
    send_progress(None, f"Screenshot directory prepared: {screenshot_directory}")
    return screenshot_directory

def take_screenshot(driver, screenshot_directory, identifier, numero_catastro):
    screenshot_path = os.path.join(screenshot_directory, f"{identifier}_{numero_catastro}.png")
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
    driver.save_screenshot(screenshot_path)
    send_progress(None, f'Screenshot for {identifier} saved.')

def create_zip_file(screenshot_directory, numero_catastro):
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(screenshot_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.basename(file)
                zf.write(file_path, arcname)
    memory_file.seek(0)
    return memory_file

def capture_screenshots(numero_catastro, queue=None):
    years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]
    
    driver = initialize_driver()
    try:
        send_progress(queue, "Browser initialized and navigating to IDEIB viewer...")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        accept_initial_modal(driver, queue)
        navigate_to_advanced_search(driver, queue)
        enter_cadastral_reference(driver, numero_catastro, queue)
        hide_ui_elements(driver, queue)
        zoom_in(driver, queue)
        close_left_column(driver, queue)

        screenshot_directory = setup_screenshot_directory(numero_catastro)
        send_progress(queue, f"Screenshot directory prepared: {screenshot_directory}")
        time.sleep(5)
        take_screenshot(driver, screenshot_directory, "now", numero_catastro)
        send_progress(queue, "Current view screenshot taken.")

        year_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@alt='Fotografies històriques de totes les illes']"))
        )
        year_select.click()
        send_progress(queue, "Historical photos menu opened.")

        total_years = len(years_to_screenshot)
        for idx, year in enumerate(years_to_screenshot, 1):
            try:
                year_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//span[text()='{year}']"))
                )
                year_element.click()
                send_progress(queue, f"Processing year {year} ({idx}/{total_years})")
                time.sleep(5)
                take_screenshot(driver, screenshot_directory, str(year), numero_catastro)
                send_progress(queue, f"Screenshot for year {year} saved.")
            except TimeoutException:
                send_progress(queue, f"Failed to find or select year {year}.")

        send_progress(queue, "Creating ZIP file...")
        zip_file = create_zip_file(screenshot_directory, numero_catastro)
        send_progress(queue, "ZIP file created successfully!")
        return zip_file
    finally:
        driver.quit()
        if queue:
            queue.put(None)  # Signal that we're done

@app.route('/screenshots/<numero_catastro>')
def get_screenshots(numero_catastro):
    try:
        queue = progress_queues.get(numero_catastro)
        zip_file = capture_screenshots(numero_catastro, queue)
        return send_file(
            zip_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'screenshots_{numero_catastro}.zip'
        )
    except Exception as e:
        import traceback
        print("Error details:", str(e))
        print("Traceback:", traceback.format_exc())
        return str(e), 500

@app.route('/progress/<numero_catastro>')
def progress_stream(numero_catastro):
    def generate():
        queue = Queue()
        progress_queues[numero_catastro] = queue
        try:
            while True:
                message = queue.get()
                if message is None:  # End of processing
                    break
                yield f"data: {json.dumps({'message': message})}\n\n"
        finally:
            if numero_catastro in progress_queues:
                del progress_queues[numero_catastro]
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) 