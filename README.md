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
Example:
- 300,000$ for 20 years with 5% interest rate
- 400$ as extra payment every month to decrease loan term
### Mortgage loan summary
![Screenshot](/screenshots/summary.PNG?raw=true "Mortgage loan summary")
### Charts
![Screenshot](/screenshots/charts.PNG?raw=true "Charts")
### Payment schedule
![Screenshot](/screenshots/schedule.PNG?raw=true "Payment schedule")
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
## Tests
### Requirements
 - Google Chrome
 - Chrome WebDriver
```
$ pip3 install -r test-requirements.txt
```
### Run tests
```
$ pytest
```
## Reference
- [Dash](https://dash.plotly.com/)
