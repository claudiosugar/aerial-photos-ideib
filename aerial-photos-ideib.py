from playwright.sync_api import sync_playwright
import time
import logging
from flask import Flask, render_template, request, send_file, jsonify
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define years to screenshot
years_to_screenshot = [1956, 1984, 1989, 2001, 2002, 2006, 2008, 2010, 2012, 2015, 2018, 2021, 2023]

app = Flask(__name__)

# Create a directory for storing screenshots if it doesn't exist
SCREENSHOT_DIR = "screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

def maximize_window(page):
    """Maximize the browser window"""
    try:
        logger.info("Maximizing browser window...")
        page.set_viewport_size({"width": 1920, "height": 1080})
        logger.info("Browser window maximized successfully")
    except Exception as e:
        logger.error(f"Failed to maximize window: {str(e)}")

def close_initial_modal(page):
    """Close the initial modal that appears when the page loads"""
    try:
        logger.info("Closing initial modal...")
        ok_button = page.locator('div.jimu-btn.jimu-float-trailing.enable-btn[data-dojo-attach-point="okNode"]')
        ok_button.wait_for(state="visible")
        ok_button.click()
        time.sleep(1)  # Wait for modal to close
        logger.info("Initial modal closed successfully")
    except Exception as e:
        logger.error(f"Failed to close initial modal: {str(e)}")

def click_locate_icon(page):
    """Click the locate icon to open the search panel"""
    try:
        logger.info("Clicking locate icon...")
        img = page.locator('img.icon[src*="/visor/widgets/ideibLocate/images/icon.png"]')
        img.wait_for(state="visible")
        parent = img.locator('xpath=..')
        parent.click()
        time.sleep(2)  # Wait for search panel to appear
        logger.info("Locate icon clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click locate icon: {str(e)}")

def click_cadastre_tab(page):
    """Click the Cadastre tab in the search panel"""
    try:
        logger.info("Clicking Cadastre tab...")
        cadastre_tab = page.locator('div.tab.jimu-vcenter-text[label="Cadastre"]')
        cadastre_tab.wait_for(state="visible")
        cadastre_tab.click()
        time.sleep(2)  # Wait for tab to be selected
        logger.info("Cadastre tab clicked successfully")
    except Exception as e:
        logger.error(f"Failed to click Cadastre tab: {str(e)}")

def enter_cadastral_reference(page, referencia_catastral):
    """Enter the cadastral reference and click search"""
    try:
        logger.info(f"Entering cadastral reference: {referencia_catastral}")
        input_field = page.locator('input#RC[name="search"]')
        input_field.wait_for(state="visible")
        input_field.fill(referencia_catastral)
        
        logger.info("Clicking search button...")
        search_button = page.locator('div.locate-btn.btn-addressLocate[data-dojo-attach-point="btnRefCat"]')
        search_button.wait_for(state="visible")
        search_button.click()
        
        time.sleep(3)  # Wait for results to load
        logger.info("Search completed successfully")
    except Exception as e:
        logger.error(f"Failed to enter cadastral reference: {str(e)}")

def close_left_column(page):
    """Close/minimize the left column"""
    try:
        left_column = page.locator('.bar.max')
        if left_column.is_visible():
            time.sleep(0.5)
            left_column.click()  # First click
            time.sleep(0.5)
            left_column.click()  # Second click
            logger.info("Left column closed/minimized.")
    except Exception as e:
        logger.error(f"Failed to close/minimize left column: {str(e)}")

def close_cerca_avancada(page):
    """Close the cerca avançada panel"""
    try:
        logger.info("Closing cerca avançada panel...")
        close_button = page.locator('div.close-icon.jimu-float-trailing[data-dojo-attach-point="closeNode"]')
        close_button.wait_for(state="visible")
        close_button.click()
        time.sleep(1)  # Wait for panel to close
        logger.info("Cerca avançada panel closed successfully")
    except Exception as e:
        logger.error(f"Failed to close cerca avançada panel: {str(e)}")

def hide_ui_elements(page):
    """Hide various UI elements to clean up the view"""
    stuff_ids = [
        'themes_IDEIBTheme_widgets_AnchorBarController_Widget_20', 'widgets_ideibSearch_Widget_22',
        'themes_IDEIBTheme_widgets_Header_Widget_21', 'widgets_ZoomSlider_Widget_24',
        'widgets_ideibStreetView', 'widgets_MyLocation_Widget_26',
        'widgets_ideibHomeButton_Widget_25', 'widgets_ideibZoomExtent',
        'widgets_ZoomSlider_Widget_24', 'dijit__WidgetBase_2', 'esri_dijit_OverviewMap_1'
    ]
    
    for element_id in stuff_ids:
        try:
            element = page.locator(f'#{element_id}')
            if element.is_visible():
                page.evaluate(f"document.getElementById('{element_id}').style.display = 'none';")
                logger.info(f'Hidden: {element_id}')
        except Exception as e:
            logger.error(f'Failed to hide {element_id}: {str(e)}')

def zoom_in_three_times(page):
    """Zoom in three times"""
    try:
        logger.info("Zooming in three times...")
        for i in range(3):
            # Find and click the zoom in button
            zoom_in_button = page.locator('div.zoom.zoom-in.jimu-corner-top.firstFocusNode[data-dojo-attach-point="btnZoomIn"]')
            zoom_in_button.wait_for(state="visible")
            zoom_in_button.click()
            time.sleep(1)  # Wait for zoom animation
            logger.info(f"Zoomed in {i+1}/3 times")
    except Exception as e:
        logger.error(f"Failed to zoom in: {str(e)}")

def take_screenshot(page, referencia_catastral, year=None):
    """Take a screenshot of the current view"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if year:
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"foto_{referencia_catastral}_{year}_{timestamp}.png")
        else:
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"foto_{referencia_catastral}_{timestamp}.png")
        page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved as {screenshot_path}")
        return os.path.normpath(screenshot_path)  # Normalize path separators
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None

def select_historical_photos(page):
    """Click on the historical photos option"""
    try:
        logger.info("Selecting historical photos option...")
        historical_photos = page.locator('img[alt="Fotografies històriques de totes les illes"]')
        historical_photos.wait_for(state="visible")
        historical_photos.click()
        time.sleep(2)  # Wait for the options to load
        logger.info("Historical photos option selected successfully")
    except Exception as e:
        logger.error(f"Failed to select historical photos: {str(e)}")

def select_year_and_screenshot(page, year, referencia_catastral):
    """Select a specific year and take a screenshot"""
    try:
        logger.info(f"Selecting year {year}...")
        year_element = page.locator(f'span:text("{year}")')
        year_element.wait_for(state="visible")
        year_element.click()
        time.sleep(5)  # Wait for the image to load
        screenshot_path = take_screenshot(page, referencia_catastral, year)
        logger.info(f"Year {year} selected and screenshot taken successfully")
        return screenshot_path
    except Exception as e:
        logger.error(f"Failed to select year {year}: {str(e)}")
        return None

def get_aerial_photos(referencia_catastral):
    """
    Navigate to the IDEIB website and retrieve aerial photos for the given cadastral reference
    Returns a list of screenshot paths
    """
    screenshot_paths = []
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Maximize window
            maximize_window(page)
            
            # Navigate to the IDEIB website
            logger.info("Navigating to IDEIB website...")
            page.goto("https://ideib.caib.es/visor/")
            page.wait_for_load_state("networkidle")
            
            # Execute all steps in sequence
            close_initial_modal(page)
            close_left_column(page)
            click_locate_icon(page)
            click_cadastre_tab(page)
            enter_cadastral_reference(page, referencia_catastral)
            close_cerca_avancada(page)
            zoom_in_three_times(page)
            hide_ui_elements(page)
            
            # Select historical photos and take screenshots for each year
            select_historical_photos(page)
            for year in years_to_screenshot:
                screenshot_path = select_year_and_screenshot(page, year, referencia_catastral)
                if screenshot_path:
                    screenshot_paths.append(screenshot_path)
            
            browser.close()
            
    except Exception as e:
        logger.error(f"Error retrieving aerial photos: {str(e)}")
    
    return screenshot_paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_photos', methods=['POST'])
def get_photos():
    referencia_catastral = request.form.get('referencia_catastral')
    if not referencia_catastral:
        return jsonify({'error': 'Please provide a cadastral reference'}), 400
    
    try:
        screenshot_paths = get_aerial_photos(referencia_catastral)
        if not screenshot_paths:
            return jsonify({'error': 'No screenshots were generated'}), 500
        
        # Convert full paths to just filenames for the response
        screenshot_filenames = [os.path.basename(path) for path in screenshot_paths]
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(screenshot_paths)} screenshots',
            'screenshots': screenshot_filenames
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    return send_file(os.path.join(SCREENSHOT_DIR, filename))

if __name__ == '__main__':
    app.run(debug=True)
