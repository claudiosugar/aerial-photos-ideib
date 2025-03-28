# Aerial Photos IDEIB

A web application that retrieves historical aerial photos from the IDEIB website based on cadastral references.

## Features

- Web interface for entering cadastral references
- Automated navigation of the IDEIB website
- Screenshot generation for multiple historical years (1956-2023)
- Responsive grid layout for viewing results
- Headless browser automation

## Requirements

- Python 3.8 or higher
- Playwright
- Flask

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aerial-photos-ideib.git
cd aerial-photos-ideib
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Usage

1. Start the Flask application:
```bash
py aerial-photos-ideib.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Enter a cadastral reference (e.g., "07040A007000630") and click "Get Photos"

4. Wait for the screenshots to be generated and displayed in the grid

## Screenshots Directory

Generated screenshots are stored in the `screenshots` directory with the following naming convention:
```
foto_[cadastral_reference]_[year]_[timestamp].png
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 