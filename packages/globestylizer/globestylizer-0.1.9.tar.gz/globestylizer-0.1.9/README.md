# globestylizer

## About state_abbr()

`globestylizer` is a Python library for use in the Boston Globe. It contains a function called `state_abbr` and has one dependency: pandas.

The intended use case for this library is for cleaning a pandas Dataframe that contains state abbreviations that are not adherent to Globe style, and returning a copy of the Dataframe that is in Globe style.

## Installation

In your virtual environment, for example pipenv, `pipenv install globestylizer`. Remember that this is dependent on pandas as well.

## Usage

Import globestylizer in your py file or Jupyter notebook: `import globestylizer`

You can call the `state_abbr` function on any pandas Dataframe and it will parse the entire Dataframe for state abbreviations or full state names. It is case-insensitive so it can handle any variety of capitalizations. Here's example data:

|  State1   |  State2   | Value |
| :-------: | :-------: | :---: |
|  Alaska   |  Alaska   |  15   |
|    AK     |    AK     |  654  |
|    AL     |    AL     | 45.32 |
|  Alabama  |  Alabama  |  789  |
| Tennessee | Tennessee |  15   |
|   Tenn.   |   Tenn.   |   3   |
|    TN     |    TN     | 31.2  |
|  WYOMING  |  WYOMING  |  789  |
|  wyoming  |  wyoming  |  455  |
|  WYoming  |  WYoming  |  11   |
|    WY     |    WY     |   2   |

Assuming you have a pandas Dataframe defined as `df`, you can call it as so:

`abbreviated_df = globestylizer.state_abbr(df)`

And `abbreviated_df` will return:

| State1 | State2 | Value |
| :----: | :----: | :---: |
| Alaska | Alaska | 15.0  |
| Alaska | Alaska | 654.0 |
|  Ala.  |  Ala.  | 45.32 |
|  Ala.  |  Ala.  | 789.0 |
| Tenn.  | Tenn.  | 15.0  |
| Tenn.  | Tenn.  |  3.0  |
| Tenn.  | Tenn.  | 31.2  |
|  Wyo.  |  Wyo.  | 789.0 |
|  Wyo.  |  Wyo.  | 455.0 |
|  Wyo.  |  Wyo.  | 11.0  |
|  Wyo.  |  Wyo.  |  2.0  |

You also have the option of parsing only selected columns. If you have state names as part of strings in other columns that you don't want abbreviated, pass in the columns that you _do_ want abbreviated as a second argument. Assuming you have data as such, and only want to clean the column 'State2':

|  State1   |  State2   | Value |
| :-------: | :-------: | :---: |
|  Alaska   |  Alaska   |  15   |
|    AK     |    AK     |  654  |
|    AL     |    AL     | 45.32 |
|  Alabama  |  Alabama  |  789  |
| Tennessee | Tennessee |  15   |
|   Tenn.   |   Tenn.   |   3   |
|    TN     |    TN     | 31.2  |
|  WYOMING  |  WYOMING  |  789  |
|  wyoming  |  wyoming  |  455  |
|  WYoming  |  WYoming  |  11   |
|    WY     |    WY     |   2   |

Pass in the column name as the second argument.

`partially_abbreviated_df = globestylizer.state_abbr(df, columns=['State2'])`

And `partially_abbreviated_df` will return:

|  State1   | State2 | Value |
| :-------: | :----: | :---: |
|  Alaska   | Alaska | 15.0  |
|    AK     | Alaska | 654.0 |
|    AL     |  Ala.  | 45.32 |
|  Alabama  |  Ala.  | 789.0 |
| Tennessee | Tenn.  | 15.0  |
|   Tenn.   | Tenn.  |  3.0  |
|    TN     | Tenn.  | 31.2  |
|  WYOMING  |  Wyo.  | 789.0 |
|  wyoming  |  Wyo.  | 455.0 |
|  WYoming  |  Wyo.  | 11.0  |
|    WY     |  Wyo.  |  2.0  |
