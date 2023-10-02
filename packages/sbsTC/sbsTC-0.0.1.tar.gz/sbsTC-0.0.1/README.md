# sbsTC
[![PyPI version](https://badge.fury.io/py/sbsTC.svg)](https://pypi.org/project/sbsTC/)

## Description
Retrieves the official exchange rate for Peru within a specified date range from SBS. This library is written in Python 3.11

## Installation
```
pip install sbsTC
```

## Basic Code
```python
from sbsTC import SbsTC

tc = SbsTC()
data = tc.get_exchange('USD','25/09/2023','30/09/2023')
print(data)
```

### The following result is obtained:
```python
{
    '25/09/2023': {'buy': '3.765', 'sell': '3.773'},
    '26/09/2023': {'buy': '3.779', 'sell': '3.787'},
    '27/09/2023': {'buy': '3.793', 'sell': '3.799'},
    '28/09/2023': {'buy': '3.801', 'sell': '3.806'},
    '29/09/2023': {'buy': '3.790', 'sell': '3.797'}
}
```

## Settings
| Option        | Description      | Default        | Allowed values                             |
|:-------------:|:----------------:|:--------------:|:------------------------------------------:|
| `date_format` | Date format      | `%d/%m/%Y`     | [http://strftime.org](http://strftime.org) |

## Example
```python
from sbsTC import SbsTC
tc = SbsTC(date_format='%Y-%m-%d')
data = tc.get_exchange('USD','25/09/2023')
print(data)
```
### The following result is obtained:
```python
{'2023-09-25': {'buy': '3.765', 'sell': '3.773'}}
```

### If no information is found:
```python
DataNotFound: No hay información disponible para el rango seleccionado
```


## Currencies
Permitted currencies:

| Currency         | Code   |
|:----------------:|:------:|
| American dollar  | `USD`  |
| Euro             | `EUR`  |
| Japan Yen        | `JPY`  |
| Canadian dollar  | `CAD`  |
| Swedish Krona    | `SEK`  |
| Swiss Franc      | `CHF`  |
| British Pound    | `GBP`  |

## Methods

### get_exchange(`currency`,`from_date`,`to_date=None`)
Obtains the currency exchange rate for the provided currency based on a given date range. The result will be a dictionary of exchange rates. ([https://docs.python.org/3/tutorial/datastructures.html#dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)).

## Considerations
* The information is available from the year 2000 onwards.
* The obtained exchange rate is as of the previous day.