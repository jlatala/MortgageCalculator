from credit_calculator.web.app import app
from credit_calculator.web.layouts.layout import get_layout
import credit_calculator.web.callbacks.callbacks


app.layout = get_layout()

if __name__ == "__main__":
    app.run_server(debug=True)