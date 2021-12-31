# Mortgage Calculator

## Overview
This is web application that calculates payment schedule for mortgage loan.
### Main Features
- calcutate your monthly installment
- select from two types of mortgage loan (fixed or declining installments)
- contribute some extra payments to your loan, to check how it may impact payment schedule
- make extra payments mounthy or for given months
- select whether extra payments should decrease loan term or installment
## Screenshots
### Mortgage loan summary
![Screenshot](./screenshots/summary.png)
### Charts
![Screenshot](./screenshots/charts.png)
### Payment schedule
![Screenshot](./screenshots/schedule.png)
## Installation
Install with pip:

```
$ pip3 install -r requirements.txt
```
## Run Flask
```
$ python3 -m credit_calculator.web.index
```
By default the app is running on http://127.0.0.1:8050/
## Unittest
```
$ python3 -m unittest
```
## Reference
- [Dash](https://dash.plotly.com/)
