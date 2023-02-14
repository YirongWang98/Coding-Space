{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import requests\n",
    "import time\n",
    "import re\n",
    "import os\n",
    "import numpy as np\n",
    "import statistics as stats\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1: Data Acquisition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 159,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Price</th>\n",
       "      <th>Apt Type</th>\n",
       "      <th>Num of Bath</th>\n",
       "      <th>Neighborhood</th>\n",
       "      <th>District</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>530 West 50th Street, Apt 2 RE...</td>\n",
       "      <td>4500</td>\n",
       "      <td>2 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>Hell's Kitchen</td>\n",
       "      <td>Midtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>524 West 50th Street, Apt 2B</td>\n",
       "      <td>2395</td>\n",
       "      <td>Studio</td>\n",
       "      <td>1</td>\n",
       "      <td>Hell's Kitchen</td>\n",
       "      <td>Midtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>37 1/2 Bedford St</td>\n",
       "      <td>3200</td>\n",
       "      <td>Studio</td>\n",
       "      <td>1</td>\n",
       "      <td>West Village</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>96 5th Avenue, Apt 12A</td>\n",
       "      <td>5750</td>\n",
       "      <td>1 Bed/ Flex 2</td>\n",
       "      <td>1</td>\n",
       "      <td>Flatiron District</td>\n",
       "      <td>Midtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1 Astor Place, Apt 6V</td>\n",
       "      <td>4750</td>\n",
       "      <td>1 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>NoHo</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10844</th>\n",
       "      <td>19 South William Street, Apt 3...</td>\n",
       "      <td>6300</td>\n",
       "      <td>4 Bed</td>\n",
       "      <td>2</td>\n",
       "      <td>Financial District</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10845</th>\n",
       "      <td>East 48th Street</td>\n",
       "      <td>5350</td>\n",
       "      <td>1 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>Turtle Bay, Midtown East</td>\n",
       "      <td>Midtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10846</th>\n",
       "      <td>West 170th Street</td>\n",
       "      <td>2250</td>\n",
       "      <td>1 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>Washington Heights</td>\n",
       "      <td>Upper Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10847</th>\n",
       "      <td>246 Mott Street, Apt 7</td>\n",
       "      <td>4295</td>\n",
       "      <td>1 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>NoLita</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10848</th>\n",
       "      <td>Mott Street</td>\n",
       "      <td>4295</td>\n",
       "      <td>1 Bed</td>\n",
       "      <td>1</td>\n",
       "      <td>NoLita</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>10849 rows × 6 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                Location Price       Apt Type Num of Bath  \\\n",
       "0      530 West 50th Street, Apt 2 RE...  4500          2 Bed           1   \n",
       "1           524 West 50th Street, Apt 2B  2395         Studio           1   \n",
       "2                      37 1/2 Bedford St  3200         Studio           1   \n",
       "3                 96 5th Avenue, Apt 12A  5750  1 Bed/ Flex 2           1   \n",
       "4                  1 Astor Place, Apt 6V  4750          1 Bed           1   \n",
       "...                                  ...   ...            ...         ...   \n",
       "10844  19 South William Street, Apt 3...  6300          4 Bed           2   \n",
       "10845                   East 48th Street  5350          1 Bed           1   \n",
       "10846                  West 170th Street  2250          1 Bed           1   \n",
       "10847             246 Mott Street, Apt 7  4295          1 Bed           1   \n",
       "10848                        Mott Street  4295          1 Bed           1   \n",
       "\n",
       "                   Neighborhood             District  \n",
       "0                Hell's Kitchen    Midtown Manhattan  \n",
       "1                Hell's Kitchen    Midtown Manhattan  \n",
       "2                  West Village   Downtown Manhattan  \n",
       "3             Flatiron District    Midtown Manhattan  \n",
       "4                          NoHo   Downtown Manhattan  \n",
       "...                         ...                  ...  \n",
       "10844        Financial District   Downtown Manhattan  \n",
       "10845  Turtle Bay, Midtown East    Midtown Manhattan  \n",
       "10846        Washington Heights      Upper Manhattan  \n",
       "10847                    NoLita   Downtown Manhattan  \n",
       "10848                    NoLita   Downtown Manhattan  \n",
       "\n",
       "[10849 rows x 6 columns]"
      ]
     },
     "execution_count": 159,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Open File and load Data\n",
    "df = pd.read_csv('Apartment Info - 500pg.csv', index_col=False)\n",
    "df = df.drop(columns=['Unnamed: 0'])\n",
    "df['Price'] = df['Price'].str.replace(',', '')\n",
    "df['Price'] = df['Price'].str.replace('$', '')\n",
    "df['Apt Type'] = df['Apt Type'].str.replace('\\n','')\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 160,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array(['1', '2', '1.5', '2.5', '3', '4.5', '4', '3.5', '6', '10',\n",
       "       'Shared'], dtype=object)"
      ]
     },
     "execution_count": 160,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['Num of Bath'].unique()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Location</th>\n",
       "      <th>Price</th>\n",
       "      <th>Apt Type</th>\n",
       "      <th>Num of Bath</th>\n",
       "      <th>Neighborhood</th>\n",
       "      <th>District</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>10804</th>\n",
       "      <td>East 89th Street</td>\n",
       "      <td>3600</td>\n",
       "      <td>Studio</td>\n",
       "      <td>Shared</td>\n",
       "      <td>Yorkville, Upper East Side</td>\n",
       "      <td>Upper Manhattan</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "               Location Price Apt Type Num of Bath  \\\n",
       "10804  East 89th Street  3600   Studio      Shared   \n",
       "\n",
       "                     Neighborhood          District  \n",
       "10804  Yorkville, Upper East Side   Upper Manhattan  "
      ]
     },
     "execution_count": 161,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.loc[df['Num of Bath']=='Shared']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2: Data Exploration"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['Location' 'Price' 'Apt Type' 'Num of Bath' 'Neighborhood' 'District']\n"
     ]
    }
   ],
   "source": [
    "print(df.columns.values)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 193,
   "metadata": {},
   "outputs": [],
   "source": [
    "cvar_list = ['Apt Type', 'Neighborhood', 'District', 'Num of Bath']\n",
    "nvar_list = ['Price']\n",
    "\n",
    "df[cvar_list] = df[cvar_list].astype('category')\n",
    "df[nvar_list] = df[nvar_list].astype('float64')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 192,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "x_var = 'Num of Bath'\n",
    "y_var = 'Price'\n",
    "\n",
    "df4ssb = df\n",
    "\n",
    "ax = df4ssb.boxplot(column=y_var, by=x_var)\n",
    "# Set the label on the y-axis using set_ylabel method of the object ax\n",
    "#ax.set_ylabel(y_var)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 199,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "x_var = 'District'\n",
    "y_var = 'Price'\n",
    "\n",
    "df4ssb = df\n",
    "\n",
    "df4ssb.boxplot(column=y_var, by=x_var);"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3: Data Pre-processing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 163,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Location        8\n",
      "Price           0\n",
      "Apt Type        0\n",
      "Num of Bath     0\n",
      "Neighborhood    0\n",
      "District        0\n",
      "dtype: int64\n",
      "Location        0\n",
      "Price           0\n",
      "Apt Type        0\n",
      "Num of Bath     0\n",
      "Neighborhood    0\n",
      "District        0\n",
      "dtype: int64\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "(10841, 6)"
      ]
     },
     "execution_count": 163,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Missing Value Imputation\n",
    "print(df.isnull().sum())\n",
    "\n",
    "# Drop the rows that are missing locaiton\n",
    "# Updated list with no missing value\n",
    "df1 = df.dropna()\n",
    "\n",
    "print(df1.isnull().sum())\n",
    "\n",
    "df1.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4: Variable Transformation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 164,
   "metadata": {},
   "outputs": [],
   "source": [
    "DV = 'Price'\n",
    "df2 = df1.dropna(subset=[DV])\n",
    "\n",
    "cvar_list = ['Apt Type', 'Neighborhood', 'District', 'Num of Bath']\n",
    "nvar_list = ['Price']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 179,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Apt Type</th>\n",
       "      <th>Neighborhood</th>\n",
       "      <th>District</th>\n",
       "      <th>Num of Bath</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1 Bed</td>\n",
       "      <td>Financial District</td>\n",
       "      <td>Downtown Manhattan</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Apt Type        Neighborhood             District Num of Bath\n",
       "0    1 Bed  Financial District   Downtown Manhattan           1"
      ]
     },
     "execution_count": 179,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# To remove dummies \n",
    "df2[cvar_list].mode()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 174,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Standardize the numerical variables \n",
    "df3 = df2.drop(columns=['Location'])\n",
    "df4 = df3.copy()\n",
    "# Set the datatype for the variables in the cvar_list to be categorical in Python\n",
    "# Set the datatype for the variables in the nvar_list to be numerical in Python \n",
    "df4[cvar_list] = df3[cvar_list].astype('category')\n",
    "df4[nvar_list] = df3[nvar_list].astype('float64')\n",
    "\n",
    "df5 = df4.copy()\n",
    "df5[nvar_list] = (df4[nvar_list] - df4[nvar_list].mean())/df4[nvar_list].std()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "99\n",
      "95\n"
     ]
    }
   ],
   "source": [
    "# Convert the categorical variables into dummies (Step 1 of dummy coding)\n",
    "# prefix_sep is the sympol used to create the dummy variable names.\n",
    "# For example, if we choose underscore _, the dummy variable name will be Fuel_Type_Diesel\n",
    "# If we choose dash -, it will be Fuel_Type-Diesel\n",
    "df6 = df5.copy()\n",
    "df6 = pd.get_dummies(df5, prefix_sep='_')\n",
    "\n",
    "# Remove the redundant dummies (Step 2 of dummy coding)\n",
    "# Placeholder variable: rdummies\n",
    "rdummies = ['Apt Type_1 Bed', 'Neighborhood_Financial District', \n",
    "            'District_ Downtown Manhattan', 'Num of Bath_1']\n",
    "df7 = df6.copy()\n",
    "df7 = df6.drop(columns=rdummies)\n",
    "\n",
    "print(len(df6.columns.values))\n",
    "print(len(df7.columns.values))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5: Data Partition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 184,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "          Price  Apt Type_1 Bed/ Flex 2  Apt Type_1 Bed/ Flex 3  \\\n",
      "4779  -0.728561                       0                       0   \n",
      "6610   0.623508                       0                       0   \n",
      "386    0.564816                       0                       0   \n",
      "2625  -0.605645                       0                       0   \n",
      "10073 -0.296821                       0                       0   \n",
      "...         ...                     ...                     ...   \n",
      "2895   0.531321                       0                       0   \n",
      "7814  -0.430798                       0                       0   \n",
      "905   -0.150859                       0                       0   \n",
      "5192  -0.642520                       0                       0   \n",
      "235    0.162575                       0                       0   \n",
      "\n",
      "       Apt Type_2 Bed  Apt Type_2 Bed / Flex 3  Apt Type_2 Bed/ Flex 3  \\\n",
      "4779                0                        0                       0   \n",
      "6610                1                        0                       0   \n",
      "386                 1                        0                       0   \n",
      "2625                1                        0                       0   \n",
      "10073               1                        0                       0   \n",
      "...               ...                      ...                     ...   \n",
      "2895                1                        0                       0   \n",
      "7814                0                        0                       0   \n",
      "905                 0                        0                       0   \n",
      "5192                1                        0                       0   \n",
      "235                 0                        0                       0   \n",
      "\n",
      "       Apt Type_2 Bed/ Flex 4  Apt Type_3 Bed  Apt Type_3 Bed/ Flex 4  \\\n",
      "4779                        0               0                       0   \n",
      "6610                        0               0                       0   \n",
      "386                         0               0                       0   \n",
      "2625                        0               0                       0   \n",
      "10073                       0               0                       0   \n",
      "...                       ...             ...                     ...   \n",
      "2895                        0               0                       0   \n",
      "7814                        0               0                       0   \n",
      "905                         0               0                       0   \n",
      "5192                        0               0                       0   \n",
      "235                         0               1                       0   \n",
      "\n",
      "       Apt Type_3 Bed/ Flex 5  ...  Neighborhood_Turtle Bay, Midtown East  \\\n",
      "4779                        0  ...                                      0   \n",
      "6610                        0  ...                                      0   \n",
      "386                         0  ...                                      0   \n",
      "2625                        0  ...                                      0   \n",
      "10073                       0  ...                                      0   \n",
      "...                       ...  ...                                    ...   \n",
      "2895                        0  ...                                      0   \n",
      "7814                        0  ...                                      0   \n",
      "905                         0  ...                                      0   \n",
      "5192                        0  ...                                      0   \n",
      "235                         0  ...                                      0   \n",
      "\n",
      "       Neighborhood_Two Bridges  Neighborhood_Upper East Side  \\\n",
      "4779                          0                             0   \n",
      "6610                          0                             0   \n",
      "386                           0                             0   \n",
      "2625                          0                             0   \n",
      "10073                         0                             0   \n",
      "...                         ...                           ...   \n",
      "2895                          0                             0   \n",
      "7814                          0                             0   \n",
      "905                           0                             0   \n",
      "5192                          0                             0   \n",
      "235                           0                             0   \n",
      "\n",
      "       Neighborhood_Upper West Side  Neighborhood_Washington Heights  \\\n",
      "4779                              0                                0   \n",
      "6610                              0                                0   \n",
      "386                               0                                0   \n",
      "2625                              0                                0   \n",
      "10073                             0                                0   \n",
      "...                             ...                              ...   \n",
      "2895                              0                                0   \n",
      "7814                              0                                0   \n",
      "905                               1                                0   \n",
      "5192                              0                                0   \n",
      "235                               0                                0   \n",
      "\n",
      "       Neighborhood_West Chelsea, Chelsea  Neighborhood_West Village  \\\n",
      "4779                                    0                          0   \n",
      "6610                                    0                          0   \n",
      "386                                     0                          0   \n",
      "2625                                    0                          0   \n",
      "10073                                   0                          0   \n",
      "...                                   ...                        ...   \n",
      "2895                                    0                          0   \n",
      "7814                                    0                          0   \n",
      "905                                     0                          0   \n",
      "5192                                    0                          0   \n",
      "235                                     0                          0   \n",
      "\n",
      "       Neighborhood_Yorkville, Upper East Side  District_ Midtown Manhattan  \\\n",
      "4779                                         0                            0   \n",
      "6610                                         0                            0   \n",
      "386                                          1                            0   \n",
      "2625                                         0                            0   \n",
      "10073                                        0                            0   \n",
      "...                                        ...                          ...   \n",
      "2895                                         0                            0   \n",
      "7814                                         0                            0   \n",
      "905                                          0                            0   \n",
      "5192                                         0                            0   \n",
      "235                                          0                            0   \n",
      "\n",
      "       District_ Upper Manhattan  \n",
      "4779                           0  \n",
      "6610                           0  \n",
      "386                            1  \n",
      "2625                           1  \n",
      "10073                          1  \n",
      "...                          ...  \n",
      "2895                           0  \n",
      "7814                           1  \n",
      "905                            1  \n",
      "5192                           1  \n",
      "235                            0  \n",
      "\n",
      "[8672 rows x 95 columns]\n"
     ]
    }
   ],
   "source": [
    "# Required package: scikit-learn. Package name in Python: sklearn\n",
    "# Required subpackage: model_selection. Required function name: train_test_split\n",
    "from sklearn.model_selection import train_test_split\n",
    "\n",
    "# Placeholder variables: df4partition, testpart_size\n",
    "# test_size specifies the percentage for the test partition\n",
    "df4partition = df7\n",
    "testpart_size = 0.2\n",
    "\n",
    "# random_state specifies the seed for random number generator. \n",
    "# random_state = 1 unless otherwised noted\n",
    "df_nontestData, df_testData = train_test_split(df4partition, test_size=testpart_size, random_state=1)\n",
    "\n",
    "print(df_nontestData)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 6: LASSO Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 263,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                                               0\n",
      "Apt Type_1 Bed/ Flex 2                  -0.00000\n",
      "Apt Type_1 Bed/ Flex 3                  -0.00000\n",
      "Apt Type_2 Bed                           0.00000\n",
      "Apt Type_2 Bed / Flex 3                 -0.00000\n",
      "Apt Type_2 Bed/ Flex 3                   0.00000\n",
      "...                                          ...\n",
      "Neighborhood_West Village                0.00000\n",
      "Neighborhood_Yorkville, Upper East Side -0.00000\n",
      "District_ Midtown Manhattan              0.00000\n",
      "District_ Upper Manhattan               -0.00000\n",
      "Intercept                               -0.03414\n",
      "\n",
      "[95 rows x 1 columns]\n"
     ]
    }
   ],
   "source": [
    "# Part 6 Lasso analysis\n",
    "\n",
    "# Required package: scikit-learn. Package name in Python: sklearn\n",
    "# Required subpackage: linear_model. \n",
    "# Required function name: Lasso, LassoCV\n",
    "\n",
    "from sklearn.linear_model import Lasso, LassoCV\n",
    "\n",
    "# Separate the predictor values and the DV values into X and y respectively\n",
    "# Placeholder variable: DV\n",
    "DV = 'Price'\n",
    "y = df_nontestData[DV]\n",
    "X = df_nontestData.drop(columns=[DV])\n",
    "\n",
    "# Run Lasso with pre-specified penalty level (alpha)\n",
    "# Placeholder variable: alpha\n",
    "alpha = 0.05\n",
    "\n",
    "# The Lasso results are put into a Lasso model object clf\n",
    "clf = Lasso(alpha=alpha, random_state=1).fit(X,y)\n",
    "\n",
    "print(summary_coef(clf))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 264,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Est. Coefficient</th>\n",
       "      <th>Coef Abs</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Num of Bath_2</th>\n",
       "      <td>0.308005</td>\n",
       "      <td>0.308005</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Apt Type_3 Bed</th>\n",
       "      <td>0.246431</td>\n",
       "      <td>0.246431</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Apt Type_Studio</th>\n",
       "      <td>-0.243872</td>\n",
       "      <td>0.243872</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Intercept</th>\n",
       "      <td>-0.034140</td>\n",
       "      <td>0.034140</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Manhattan Valley, Upper West Side</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Alphabet City, East Village</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_Shared</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_6</th>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_4.5</th>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Gramercy Park</th>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>95 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                Est. Coefficient  Coef Abs\n",
       "Num of Bath_2                                           0.308005  0.308005\n",
       "Apt Type_3 Bed                                          0.246431  0.246431\n",
       "Apt Type_Studio                                        -0.243872  0.243872\n",
       "Intercept                                              -0.034140  0.034140\n",
       "Neighborhood_Manhattan Valley, Upper West Side         -0.000000  0.000000\n",
       "...                                                          ...       ...\n",
       "Neighborhood_Alphabet City, East Village               -0.000000  0.000000\n",
       "Num of Bath_Shared                                     -0.000000  0.000000\n",
       "Num of Bath_6                                           0.000000  0.000000\n",
       "Num of Bath_4.5                                         0.000000  0.000000\n",
       "Neighborhood_Gramercy Park                              0.000000  0.000000\n",
       "\n",
       "[95 rows x 2 columns]"
      ]
     },
     "execution_count": 264,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Rank the importance \n",
    "coef = (summary_coef(clf))\n",
    "coef.columns = ['Est. Coefficient']\n",
    "coef['Coef Abs'] = coef['Est. Coefficient'].abs()\n",
    "coef.sort_values(by=['Coef Abs'], ascending=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 269,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The optimal alpha is  0.00011188421026315361\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Est. Coefficient</th>\n",
       "      <th>Coef Abs</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Apt Type_8 Bed</th>\n",
       "      <td>11.936340</td>\n",
       "      <td>11.936340</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_6</th>\n",
       "      <td>11.705481</td>\n",
       "      <td>11.705481</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_4</th>\n",
       "      <td>6.190020</td>\n",
       "      <td>6.190020</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_4.5</th>\n",
       "      <td>5.667360</td>\n",
       "      <td>5.667360</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_3.5</th>\n",
       "      <td>4.525427</td>\n",
       "      <td>4.525427</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Chinatown</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Civic Center</th>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Cooperative Village, Lower East Side</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Morningside Heights, West Harlem</th>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Little Senegal, Central Harlem, Harlem</th>\n",
       "      <td>-0.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>95 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                    Est. Coefficient  \\\n",
       "Apt Type_8 Bed                                             11.936340   \n",
       "Num of Bath_6                                              11.705481   \n",
       "Num of Bath_4                                               6.190020   \n",
       "Num of Bath_4.5                                             5.667360   \n",
       "Num of Bath_3.5                                             4.525427   \n",
       "...                                                              ...   \n",
       "Neighborhood_Chinatown                                     -0.000000   \n",
       "Neighborhood_Civic Center                                   0.000000   \n",
       "Neighborhood_Cooperative Village, Lower East Side          -0.000000   \n",
       "Neighborhood_Morningside Heights, West Harlem               0.000000   \n",
       "Neighborhood_Little Senegal, Central Harlem, Ha...         -0.000000   \n",
       "\n",
       "                                                     Coef Abs  \n",
       "Apt Type_8 Bed                                      11.936340  \n",
       "Num of Bath_6                                       11.705481  \n",
       "Num of Bath_4                                        6.190020  \n",
       "Num of Bath_4.5                                      5.667360  \n",
       "Num of Bath_3.5                                      4.525427  \n",
       "...                                                       ...  \n",
       "Neighborhood_Chinatown                               0.000000  \n",
       "Neighborhood_Civic Center                            0.000000  \n",
       "Neighborhood_Cooperative Village, Lower East Side    0.000000  \n",
       "Neighborhood_Morningside Heights, West Harlem        0.000000  \n",
       "Neighborhood_Little Senegal, Central Harlem, Ha...   0.000000  \n",
       "\n",
       "[95 rows x 2 columns]"
      ]
     },
     "execution_count": 269,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# A user-defined function summary_coef\n",
    "# to display the estimated coefficients of a model candidate obtained by the Lasso analysis\n",
    "# Input:  a Lasso model object which is the output of the function Lasso \n",
    "# Output: the estimated coefficients of the model candidate reported by the input Lasso model object\n",
    "def summary_coef(model_object):\n",
    "  n_predictors = X.shape[1]\n",
    "  model_coef = pd.DataFrame(model_object.coef_.reshape(1, n_predictors), columns=X.columns.values)\n",
    "  model_coef['Intercept'] = model_object.intercept_\n",
    "  return model_coef.transpose()\n",
    "\n",
    "# Run Lasso with k-fold cross validation with k=5\n",
    "# Placeholder variable: kfolds\n",
    "kfolds = 5\n",
    "\n",
    "# Set n_jobs to be -1 to run LassoCV on all CPU cores.\n",
    "clf_optimal = LassoCV(cv=kfolds, random_state=1, n_jobs=-1).fit(X,y)\n",
    "\n",
    "# Display the optimal alpha that yields the final selected model (the best model candidate)\n",
    "print('The optimal alpha is ', clf_optimal.alpha_)\n",
    "\n",
    "# Display the estimated coefficients of the final selected model\n",
    "opt_coef = (summary_coef(clf_optimal))\n",
    "opt_coef.columns = ['Est. Coefficient']\n",
    "opt_coef['Coef Abs'] = opt_coef['Est. Coefficient'].abs()\n",
    "opt_coef.sort_values(by=['Coef Abs'], ascending=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 272,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Est. Coefficient</th>\n",
       "      <th>Coef Abs</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Apt Type_8 Bed</th>\n",
       "      <td>11.936340</td>\n",
       "      <td>11.936340</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_6</th>\n",
       "      <td>11.705481</td>\n",
       "      <td>11.705481</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_4</th>\n",
       "      <td>6.190020</td>\n",
       "      <td>6.190020</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_4.5</th>\n",
       "      <td>5.667360</td>\n",
       "      <td>5.667360</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_3.5</th>\n",
       "      <td>4.525427</td>\n",
       "      <td>4.525427</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_3</th>\n",
       "      <td>1.950924</td>\n",
       "      <td>1.950924</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Num of Bath_2.5</th>\n",
       "      <td>1.364358</td>\n",
       "      <td>1.364358</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Midtown</th>\n",
       "      <td>0.830196</td>\n",
       "      <td>0.830196</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_Lenox Hill, Upper East Side</th>\n",
       "      <td>0.768305</td>\n",
       "      <td>0.768305</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Neighborhood_SoHo</th>\n",
       "      <td>0.741471</td>\n",
       "      <td>0.741471</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                          Est. Coefficient   Coef Abs\n",
       "Apt Type_8 Bed                                   11.936340  11.936340\n",
       "Num of Bath_6                                    11.705481  11.705481\n",
       "Num of Bath_4                                     6.190020   6.190020\n",
       "Num of Bath_4.5                                   5.667360   5.667360\n",
       "Num of Bath_3.5                                   4.525427   4.525427\n",
       "Num of Bath_3                                     1.950924   1.950924\n",
       "Num of Bath_2.5                                   1.364358   1.364358\n",
       "Neighborhood_Midtown                              0.830196   0.830196\n",
       "Neighborhood_Lenox Hill, Upper East Side          0.768305   0.768305\n",
       "Neighborhood_SoHo                                 0.741471   0.741471"
      ]
     },
     "execution_count": 272,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Display the estimated coefficients of the final selected model\n",
    "opt_coef = (summary_coef(clf_optimal))\n",
    "opt_coef.columns = ['Est. Coefficient']\n",
    "opt_coef['Coef Abs'] = opt_coef['Est. Coefficient'].abs()\n",
    "opt_coef.sort_values(by=['Coef Abs'], ascending=False).head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 188,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0.2341632500409665\n",
      "0.3509730802737765\n"
     ]
    }
   ],
   "source": [
    "# Calcuate the ASE over the test partition based on the final selected model\n",
    "\n",
    "# y_test_actual is the actual values of the DV in the test partition\n",
    "y_test_actual = df_testData[DV]\n",
    "\n",
    "# X_test is the predictor values in the test partition\n",
    "X_test = df_testData.drop(columns=[DV])\n",
    "\n",
    "# Use predict method of the clf_optimal object to apply the model associated with clf_optimal to the test partition\n",
    "# y_test_predicted is the predicted values of the DV in the test partition \n",
    "y_test_predicted = clf_optimal.predict(X_test)\n",
    "\n",
    "# Get the number of obs in the test partition\n",
    "n_obs_test = df_testData.shape[0]\n",
    "\n",
    "# Derive ASE over the test partition based on the definition of ASE\n",
    "ASE_test = sum((y_test_actual - y_test_predicted)**2)/n_obs_test\n",
    "\n",
    "\n",
    "# Derive ASE over the nontest partition based on the definition of ASE\n",
    "y_nontest_actual = y\n",
    "y_nontest_predicted = clf_optimal.predict(X)\n",
    "n_obs_nontest = df_nontestData.shape[0]\n",
    "\n",
    "ASE_nontest = sum((y_nontest_actual - y_nontest_predicted)**2)/n_obs_nontest\n",
    "\n",
    "# Compare the ASE over the test partition and the nontest partition.\n",
    "# If the gap is big, the final selected model might overfit the historical data \n",
    "print(ASE_test)\n",
    "print(ASE_nontest)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
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
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
