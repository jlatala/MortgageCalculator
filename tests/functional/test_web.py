import pytest
import dash
from dash import html
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from credit_calculator.web.app import app
from credit_calculator.web.layouts.layout import get_layout
import credit_calculator.web.callbacks.callbacks


class LoanType:
    fixed = 0
    declining = 1


def test_web_app_is_running(dash_duo):
    app.layout = get_layout()
    dash_duo.start_server(app)
    assert dash_duo.driver.title == "Mortgage Calculator"
    assert dash_duo.get_logs() == [], "browser console should contain no error"


@pytest.mark.parametrize(
    "loan_type,extra_payment,expected",
    [(LoanType.fixed, 400, "2,379.87"), (LoanType.declining, 0, "2,500.00")],
)
def test_correct_installment_value(dash_duo, loan_type, extra_payment, expected):
    app.layout = get_layout()
    dash_duo.start_server(app)
    # select fixed loan type
    loan_type_radio_labels = dash_duo.driver.find_elements(
        By.CLASS_NAME, "label-loan-type-radio"
    )
    loan_type_radio_labels[loan_type].click()
    # go to advanced options
    settings_tabs = dash_duo.driver.find_element(By.ID, "settings-tabs")
    settings_tabs = settings_tabs.find_elements(By.CSS_SELECTOR, "*")
    settings_tabs[3].click()
    # set extra payments
    monthly_overpayment_input = dash_duo.driver.find_element(
        By.ID, "monthly-overpayment-input"
    )
    monthly_overpayment_input.send_keys(Keys.BACK_SPACE, extra_payment, Keys.ENTER)
    summary_heading_text = dash_duo.driver.find_element(By.ID, "summary-heading-text")
    dash_duo.wait_for_text_to_equal(
        "#summary-heading-text", f"Your monthly payment {expected}$", timeout=10
    )
