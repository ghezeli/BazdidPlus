# Web Scraping Project

## Overview
This project is a comprehensive web scraping solution designed for collecting, analyzing, and storing data from websites. It is built with modular components to ensure flexibility and scalability.

## Files in the Project
- `config.json`: Stores configuration settings including scraping methods, database credentials, and website-specific details.
- `database.py`: Handles database operations, including saving scraped data into a PostgreSQL database.
- `generate_html_patterns.py`: Generates HTML patterns (e.g., tags, classes) for structured data extraction.
- `html_patterns.json`: Stores the HTML patterns for various websites in JSON format.
- `main.py`: The main script orchestrating the scraping process.
- `scraper.py`: Contains the scraping logic to fetch and parse website data.
- `structure_learning.py`: Implements the logic to learn and adapt to changes in website structures automatically.
- `utils.py`: Provides utility functions, such as saving data to files.
- `validate_html_patterns.py`: Validates the stored HTML patterns against live websites.

## How to Run
1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Update the `config.json` file with your specific settings (e.g., database credentials, website URLs).
    - Example:
      ```json
      {
        "settings": {
          "scraping_method": "requests+beautifulsoup",
          "specific_requirements": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
          },
          "database": {
            "type": "PostgreSQL",
            "host": "localhost",
            "port": 5432,
            "user": "your_user",
            "password": "your_password",
            "dbname": "your_dbname"
          }
        },
        "websites": [
          {
            "url": "https://example.com",
            "scraping_method": "requests+beautifulsoup",
            "interval": "5m",
            "pages": [
              {
                "title": "Page Title",
                "url": "https://example.com/page"
              }
            ]
          }
        ]
      }
      ```
3. Run the main script:
    ```bash
    python main.py
    ```

## Dependencies
- Python 3.8+
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `psycopg2`

## Notes
- Ensure the database is set up and accessible before running the scripts.
- Use `generate_html_patterns.py` to generate patterns for new websites.
- Validate patterns using `validate_html_patterns.py` to avoid scraping errors.

## License
This project is licensed under the MIT License.
