def round_currency(func):
    def rounded(*args, **kwargs):
        return float(round(func(*args, **kwargs), 2))

    return rounded