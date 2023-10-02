def faker_generated_data(naming=None,
                         format=None,
                         parentheses=None,
                         columns_integer_default=None,
                         columns_date_default=None,
                         columns_string_default=None,
                         columns_decimal_default=None
                         ):
    from faker import Faker
    import random
    import string
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    fake = Faker()
    _fake = None
    format = str(format).upper()

    if format.startswith(("INTEGER", "NUMERIC", "NUMERIC SHORT", "NUMERIC BIG", "NUMERIC LARGE")):
        _fake = fake.pyint(min_value=0, max_value=9999)
        if naming in list(columns_integer_default.keys()):
            new_int = int(columns_integer_default[naming])
            _fake = fake.pyint(min_value=new_int, max_value=new_int)

    elif format.startswith("TIMESTAMP"):
        d2 = datetime.now()
        d1 = d2 - relativedelta(months=6)
        _fake = str(fake.date_time_between(start_date=d1, end_date=d2))
    elif format.startswith("DECIMAL"):
        _parentheses_split = str(parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])
        min_value_left = int("1" * (_decimal_left - _decimal_right))
        max_value_left = int("9" * (_decimal_left - _decimal_right))
        _fake = str(fake.pydecimal(left_digits=_decimal_left,
                                   right_digits=_decimal_right,
                                   positive=True,
                                   min_value=min_value_left,
                                   max_value=max_value_left))
        if naming in list(columns_decimal_default.keys()):
            new_decimal = float(columns_decimal_default[naming])
            _fake = fake.bothify(text=f'{new_decimal}')
    elif format.startswith("TIME"):
        _fake = fake.time()
    elif format.startswith("DATE"):
        if naming in list(columns_date_default.keys()):
            new_text = columns_date_default[naming]
            _fake = str(datetime.strptime(new_text, '%Y-%m-%d'))
        else:
            d2 = datetime.today()
            d1 = d2 - relativedelta(months=1)
            _fake = str(fake.date_between(start_date=d1, end_date=d2))
    elif format.startswith("STRING"):
        if naming in ("g_entific_id",):
            _fake = fake.bothify(text='PE')
        elif naming in ("gf_frequency_type", "frequency_type"):
            _fake = fake.bothify(text='?', letters='DM')
        elif naming in list(columns_string_default.keys()):
            new_text = columns_string_default[naming]
            _fake = fake.bothify(text=new_text)
        else:
            _fake = ''.join(random.choices(string.ascii_letters + string.digits, k=int(parentheses)))
    return _fake
