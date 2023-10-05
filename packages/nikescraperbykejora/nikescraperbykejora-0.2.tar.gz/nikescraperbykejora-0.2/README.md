# Nike Scraper By Kejora

A simple Python package for scraping detailed product information from the Nike Indonesia site (nike.com/id).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this package, you need to install it in your Python environment. You can do this using pip:

```bash
pip install -U nikescraperbykejora
```

Make sure you have created a virtual environment before installing the package.

This package has the following dependencies:

pandas>=2.1.1
httpx>=0.25.0
playwright>=1.38.0
selectolax>=0.3.16
These dependencies will be automatically installed when you install 'nikescraperbykejora'.

## Usage

### Directory Structure
Make directory structure to use package as below:

```bash
example_scraper/
├── main.py
├── .gitignore
└── README.md
``` 

### Scraping a Single Product
You can scrape data for a single Nike product using the provided main.py script as below:

```bash
import asyncio
import os
from nikescraperbykejora.scrapingresult import ProductScraperHandler


async def main():
    # User input for scraping one product
    target_url_one = "https://www.exampleurlproducttoscrape.com/single" # Change with url you want to scrape, DON'T skip quotation mark (" ")
    txt_file_name = "Product Name.txt" # Change with the name of product you want to scrape, DON'T skip .txt

    # Get the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    os.chdir(project_directory)

    # Specify the full path to the result file
    result_file_path = os.path.join(project_directory, "result", txt_file_name)

    await ProductScraperHandler.one_product(target_url_one, result_file_path)


if __name__ == "__main__":
    asyncio.run(main())
```
 
#### Example Scraping a Single Product

![example_scraping_single_product](example_scraping_one_product.png)

Here's an example of how to use it. Scraping detail data of Nike Air Force 1 '07 with the url: 
```bash
https://www.nike.com/id/t/air-force-1-07-shoe-NMmm1B/DD8959-100
```

So...the code for scraping in your main.py file as below.

```bash
import asyncio
import os
from nikescraperbykejora.scrapingresult import ProductScraperHandler


async def main():
    # User input for scraping one product
    target_url_one = "https://www.nike.com/id/t/air-force-1-07-shoe-NMmm1B/DD8959-100"
    txt_file_name = "Nike Air Force 1 '07.txt"

    # Get the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    os.chdir(project_directory)

    # Specify the full path to the result file
    result_file_path = os.path.join(project_directory, "result", txt_file_name)

    await ProductScraperHandler.one_product(target_url_one, result_file_path)


if __name__ == "__main__":
    asyncio.run(main())
```

### Scraping Multi Product
You can scrape data for some Nike products in product category using the provided main.py script as below:

```bash
import asyncio
import os
from nikescraperbykejora.scrapingresult import ProductScraperHandler

async def main():
    # User input for scraping multi products
    target_url_multi = "https://www.exampleurlproducttoscrape.com/multi" # Change with url you want to scrape
    csv_file_name = "Product Category Name.CSV" # Change with the name of product category you want to scrape, DON'T skip .CSV
    product_count = 14 # Change with product count that displayed on the page
    timeout_seconds = 10 # Change with a higher integer value if scraping fails due to timeout

    # Get the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    os.chdir(project_directory)

    # Specify the full path to the result file
    result_file_path = os.path.join(project_directory, "result", csv_file_name)

    await ProductScraperHandler.multi_product(target_url_multi, result_file_path, product_count, timeout_seconds)

if __name__ == "__main__":
    asyncio.run(main())
```
 
#### Example Scraping Multi Product

![example_scraping_multi_product](example_scraping_multi_product.png)

On nike.com/id navbar you choose Men > Football > Shop by price Rp1.500.001 - Rp2.999.999, so below the data will be display
on the site:
```bash
https://www.nike.com/id/w/mens-1500001-2999999-football-shoes-1gdj0z2952fznik1zy7ok
```
- Multi Product Category Name : Men's Rp1.500.001 - Rp2.999.999 Football Shoes
- Product count : 14 # It could be that when you try this URL, the product count value is different

And...the code for scraping in your main.py file as below.

```bash
import asyncio
from nikescraperbykejora.idsavedresult import ProductScraperHandler

async def main():
    # User input for scraping multiple products
    target_url_multi = "https://www.nike.com/id/w/mens-1500001-2999999-football-shoes-1gdj0z2952fznik1zy7ok" 
    csv_file_name = "Men's Rp1.500.001 - Rp2.999.999 Football Shoes.csv" 
    product_count = 14
    timeout_seconds = 10 

    # Get the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))

    os.chdir(project_directory)

    # Specify the full path to the result file
    result_file_path = os.path.join(project_directory, "result", csv_file_name)

    await ProductScraperHandler.multi_product(target_url_multi, result_file_path, product_count, timeout_seconds)

if __name__ == "__main__":
    asyncio.run(main())
```

#### WARNING
Make sure double quotation mark (" ") for url, .txt for single product file name, .csv for multi product file name.

### Scraping Result
The scraping result will be saved in the 'result' directory that automatically appears after the scraping process is complete.


## Contributing
If you'd like to contribute to this project, please follow these steps:

- Fork the repository on GitHub.
- Create a new branch with a descriptive name.
- Make your changes and commit them.
- Push your changes to your fork.
- Submit a pull request to the original repository.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
