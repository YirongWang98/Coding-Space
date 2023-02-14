{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fb0f9086",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import time\n",
    "import re\n",
    "import os\n",
    "import pandas as pd\n",
    "\n",
    "from bs4 import BeautifulSoup\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.chrome.service import Service\n",
    "from selenium.common.exceptions import NoSuchElementException\n",
    "from selenium.webdriver.common.by import By"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "e82fa832",
   "metadata": {},
   "outputs": [],
   "source": [
    "link_rent = \"https://www.renthop.com/apartments-for-rent/manhattan-new-york-ny\"\n",
    "path = \"/Users/remilin/Downloads/chromedriver\"\n",
    "s = Service(path)\n",
    "browser = webdriver.Chrome(service = s)\n",
    "browser.get(link_rent)\n",
    "time.sleep(3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "6638a014",
   "metadata": {},
   "outputs": [],
   "source": [
    "def check_exists_by_xpath(xpath):\n",
    "    try:\n",
    "        browser.find_element(By.XPATH,xpath)\n",
    "    except NoSuchElementException:\n",
    "        return False\n",
    "    return True"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "73772436",
   "metadata": {},
   "outputs": [],
   "source": [
    "page_num = 2\n",
    "location = []\n",
    "price = []\n",
    "apttype = []\n",
    "bath = []\n",
    "\n",
    "for i in range(0, page_num):\n",
    "    page_source = browser.page_source\n",
    "    soup = BeautifulSoup(page_source, 'lxml')\n",
    "    rent_content = soup.find_all('div', class_='search-info d-block align-top')\n",
    "    \n",
    "    #extract the rating star and review content\n",
    "    for rent in rent_content:\n",
    "        address_text = rent.find('a').text.strip()\n",
    "        price_detail = rent.find('div', class_='d-inline-block align-middle b font-size-20').text.strip()\n",
    "        apt_type = rent.find('div', style=\"margin-left: 3px;\").text.strip()\n",
    "        bath_number = rent.find('div', style=\"margin-left: 1px;\").text.strip()\n",
    "\n",
    "            \n",
    "        #append them into list\n",
    "        location.append(address_text)\n",
    "        price.append(price_detail)\n",
    "        apttype.append(apt_type)\n",
    "        bath.append(bath_number)\n",
    "            \n",
    "   \n",
    "    #use selenium to click the next button\n",
    "    if (check_exists_by_xpath('//a[@class=\"next-page font-blue\"]')):\n",
    "        browser.find_element(By.XPATH,'//a[@class=\"next-page font-blue\"]').click()\n",
    "        time.sleep(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "6b07af3f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['808 Columbus Avenue, Apt 07H',\n",
       " '795 Columbus Avenue, Apt 09N',\n",
       " '95 Wall Street, Apt 1005',\n",
       " '95 Wall Street, Apt 806',\n",
       " '41 Bedford Street, Apt 3C',\n",
       " '1654 Third Avenue, Apt 13',\n",
       " '120 W. 21st, Apt 303',\n",
       " '120 W. 21st, Apt 1508',\n",
       " '93rd Street & 2nd Avenue',\n",
       " 'East 50th Street',\n",
       " '1 Columbus Place, Apt N6E',\n",
       " '75 West End Ave, Apt S18G',\n",
       " '401 E 34th St, Apt S24E',\n",
       " '401 E 34th St, Apt S07E',\n",
       " '10 Hanover Square, Apt 07J',\n",
       " '243 W 109 Street',\n",
       " '10 Hanover Square, Apt 22K',\n",
       " '20 Cornelia Street, Apt 15',\n",
       " 'East 11th Street',\n",
       " '133 Avenue D',\n",
       " '788 Columbus Ave, Apt 7M',\n",
       " 'Columbus Avenue',\n",
       " '243 W 109 Street',\n",
       " '95 Wall Street, Apt 1921',\n",
       " '808 Columbus Avenue, Apt 09H',\n",
       " '10 Hanover Square, Apt 22K',\n",
       " '801 Amsterdam Avenue, Apt 11H',\n",
       " '37.5 Bedford Street, Apt 3B',\n",
       " '20 Cornelia Street, Apt 15',\n",
       " '37.5 Bedford Street, Apt 3B',\n",
       " 'East 11th Street',\n",
       " '133 Avenue D',\n",
       " '95 Wall Street, Apt 625',\n",
       " 'East 44th Street',\n",
       " '252 West 76 Street, Apt 2D',\n",
       " '199 East 3rd Street',\n",
       " '30 Charlton Street, Apt 5G',\n",
       " '117 West 13th Street, Apt 49',\n",
       " '416 East 13 Street, Apt 6',\n",
       " '512 East 5th Street, Apt 10',\n",
       " '11 Jones Street, Apt 10',\n",
       " '120 1st Avenue, Apt 14',\n",
       " '105th Street and Columbus Ave ...']"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "location"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "a076c1c2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['$6,351',\n",
       " '$4,507',\n",
       " '$4,235',\n",
       " '$3,779',\n",
       " '$3,200',\n",
       " '$2,400',\n",
       " '$5,302',\n",
       " '$5,340',\n",
       " '$3,121',\n",
       " '$3,350',\n",
       " '$6,500',\n",
       " '$4,500',\n",
       " '$4,469',\n",
       " '$4,368',\n",
       " '$4,260',\n",
       " '$1,950',\n",
       " '$4,260',\n",
       " '$2,895',\n",
       " '$3,995',\n",
       " '$1,475',\n",
       " '$6,500',\n",
       " '$5,495',\n",
       " '$1,950',\n",
       " '$4,360',\n",
       " '$6,603',\n",
       " '$4,260',\n",
       " '$3,793',\n",
       " '$3,550',\n",
       " '$2,895',\n",
       " '$3,750',\n",
       " '$3,995',\n",
       " '$1,475',\n",
       " '$4,043',\n",
       " '$5,475',\n",
       " '$4,495',\n",
       " '$7,290',\n",
       " '$4,495',\n",
       " '$3,900',\n",
       " '$5,995',\n",
       " '$2,595',\n",
       " '$3,400',\n",
       " '$4,495',\n",
       " '$1,750']"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "price"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "b5e586a0",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['2 Bed',\n",
       " '1 Bed',\n",
       " 'Studio',\n",
       " '1 Bed',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '2 Bed',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " 'Studio',\n",
       " 'Private Room',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " '1 Bed',\n",
       " 'Private Room',\n",
       " '2 Bed',\n",
       " '2 Bed',\n",
       " 'Private Room',\n",
       " '1 Bed',\n",
       " '2 Bed',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " 'Studio',\n",
       " '1 Bed',\n",
       " 'Private Room',\n",
       " 'Studio',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '4 Bed',\n",
       " '1 Bed',\n",
       " '1 Bed',\n",
       " '3 Bed',\n",
       " 'Studio',\n",
       " '2 Bed',\n",
       " '2 Bed',\n",
       " 'Private Room']"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "apttype"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "93a50c59",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['2 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '2 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '2 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '2 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '1.5 Bath',\n",
       " '1 Bath',\n",
       " '1 Bath',\n",
       " '2 Bath',\n",
       " '2 Bath']"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "bath"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "67900c32",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1e1e3d3f",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f29daded",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
