def extract_only_parenthesis(format):
    import re
    _number = re.findall(r'\(.*?\)', format)
    if len(_number) > 0:
        res = str(_number[0])
        res = res.replace("(", "").replace(")", "").strip()
    else:
        res = ""
    return res


def extract_only_column_text(columns):
    import re
    new_col = str(columns).lower()

    _text = re.findall(r'([a-zA-Z ]+)', new_col)
    if len(_text) > 0:
        res = _text[0]
    else:
        res = ""
    return res


def spark_reformat_dtype_data(columns, format, convert_string=False):
    from pyspark.sql import types

    _format = str(extract_only_column_text(format)).upper()
    _format_text = str(extract_only_column_text(format)).upper()
    if str(_format).upper() == "DATE":
        _mask = "yyyy-MM-dd"
        _format = format
        _locale = "es_PE"
        _schema_type = "['date', 'null']"
        _type = types.StructField(columns, types.DateType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(10)"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper() == "TIMESTAMP":
        _mask = "yyyy-MM-dd HH:mm:ss.SSSSSS"
        _format = format
        _locale = "es_PE"
        _schema_type = "['timestamp', 'null']"
        _type = types.StructField(columns, types.TimestampType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC(26)"
            _locale = ""
            _schema_type = "['string', 'null']"

    elif str(_format).upper() == "TIME":
        _mask = ""
        _format = "ALPHANUMERIC(8)"
        _locale = "PE"
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
    elif str(_format).upper() in ("NUMERIC SHORT", "INTEGER"):
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['null', 'int32']"
        _type = types.StructField(columns, types.IntegerType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper() in ("NUMERIC BIG", "NUMERIC LARGE"):
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['null', 'int64']"
        _type = types.StructField(columns, types.IntegerType())
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"
    elif str(_format).upper().startswith("DECIMAL"):
        _parentheses = extract_only_parenthesis(format)
        _parentheses_split = str(_parentheses).split(",")
        if len(_parentheses_split) <= 1:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = 0
        else:
            _decimal_left = int(_parentheses_split[0])
            _decimal_right = int(_parentheses_split[1])

        _mask = ""
        _format = format
        _locale = ""
        _schema_type = f"['null', '{format}']"
        _type = types.StructField(columns, types.DecimalType(precision=_decimal_left, scale=_decimal_right))
        _type_string = types.StructField(columns, types.StringType())
        if convert_string:
            _mask = ""
            _format = "ALPHANUMERIC"
            _locale = ""
            _schema_type = "['string', 'null']"

    else:
        _mask = ""
        _format = format
        _locale = ""
        _schema_type = "['string', 'null']"
        _type = types.StructField(columns, types.StringType())
        _type_string = types.StructField(columns, types.StringType())
        _format_text = "STRING"

    result = dict()
    result["_format"] = _format
    result["_mask"] = _mask
    result["_locale"] = _locale
    result["_type"] = _type
    result["_type_string"] = _type_string
    result["_schema_type"] = _schema_type
    result["_format_text"] = _format_text

    return result