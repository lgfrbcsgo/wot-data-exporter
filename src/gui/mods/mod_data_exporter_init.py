from debug_utils import LOG_CURRENT_EXCEPTION


def init():
    try:
        from mod_data_exporter import main
        main()
    except Exception:
        LOG_CURRENT_EXCEPTION()


def fini():
    pass
