# BF PNRPU Schedule Parser

This program is a web scraper that extracts schedule data from the BF PNRPU (Perm National Research Polytechnic University) university schedule webpage. It uses Selenium for web page interaction and Beautiful Soup 4 (BS4) for parsing HTML content. 

## Features

* **Adjustable date range**: Select a specific date range for fetching schedule data. If the `date_from` and `date_to` fields are left blank in the config file, the program will use the default date range provided by the webpage.
* **Group and teacher filtering**: Specify a group or teacher to filter the schedule data.
* **Formatted output**: The extracted schedule data is displayed in a clear, well-formatted table.

## Configuration

Customize the behavior of the program by editing the `config.json` file. The available settings include:

* `headless_launch`: Set to `true` for headless browser execution, `false` to display the browser window (mainly for debugging).
* `window_size`: Configure the Python console window size using the "mode" command (e.g. `"mode 160, 300"`, where `160` is width and `300` is height).
* `date_from`: Specify the starting date for fetching schedule data (e.g. `"25.09.2023"`). Leave it as an empty string to use the default date from the webpage.
* `date_to`: Specify the end date for fetching schedule data (e.g. `"08.10.2023"`). Leave it as an empty string to use the default date from the webpage.
* `group`: Specify the group or teacher for filtering schedule data.
