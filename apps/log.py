import logging
import datetime


def logger_init(log_level):
    t = datetime.datetime.now()
    _filename = "log_{Y}_{M}_{D}_{h}_{m}_{s}".format(
        Y=str(t.year),
        M=str(t.month),
        D=str(t.day),
        h=str(t.hour),
        m=str(t.min),
        s=str(t.second),
    )

    logging.basicConfig(
        level=log_level,
        filemode='w',
        format='%(levelname)-8s | %(asctime)s | %(module)s:%(lineno)d | %(message)s'
    )

    # logging.info("Logger initialized. level=" + logging.getLevelName(log_level))
