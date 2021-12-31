import argparse
from credit_calculator.web.app import app
from credit_calculator.web.layouts.layout import get_layout
import credit_calculator.web.callbacks.callbacks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Mortgage Calculator web server")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    app.layout = get_layout()
    app.run_server(debug=args.debug)
