import datetime


class DateUtils:
    @staticmethod
    def full_datetime_to_str(_dt, _format="%Y%m%d %H:%M:%S"):
        if _dt in (None, ""):
            return None
        if isinstance(_dt, str):
            return _dt
        return _dt.strftime(_format)

    @staticmethod
    def str_to_datetime(_str, _format="%Y/%m/%d"):
        if _str in (None, ""):
            return None
        input_date = datetime.datetime.strptime(_str, _format)
        output_date = input_date.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.datetime.strptime(output_date, "%Y-%m-%d %H:%M:%S")