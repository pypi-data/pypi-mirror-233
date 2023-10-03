from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Server config settings
    """

    DUMP_ARGS: bool = False
    COLUMNS: int = 110
    # https://rich.readthedocs.io/en/stable/appendix/colors.html
    LOG_LEVEL_ELAPCE_TPL: str = "[reverse turquoise2] ELAPCE [/]"

    LOG_LEVEL_START_TPL: str = "[reverse i aquamarine1] START  [/]"
    LOG_LEVEL_END_TPL: str = "[reverse i green4] END    [/reverse i green4]"

    LOG_LEVEL_TEST_TPL: str = "[reverse grey70] TEST   [/]"
    LOG_LEVEL_DATA_TPL: str = "[reverse cornflower_blue] DATA   [/]"
    LOG_LEVEL_DEV_TPL: str = "[reverse grey70] DEV    [/]"
    LOG_LEVEL_INFO_TPL: str = "[reverse blue] INFO   [/]"
    LOG_LEVEL_TRACE_TPL: str = "[reverse dodger_blue2] TRACE  [/]"
    LOG_LEVEL_RUN_TPL: str = "[reverse yellow] RUN    [/]"
    LOG_LEVEL_GO_TPL: str = "[reverse royal_blue1] GO     [/]"
    LOG_LEVEL_LIST_TPL: str = "[reverse wheat4] LIST   [/]"
    LOG_LEVEL_DEBUG_TPL: str = "[reverse #9f2844] DEBUG  [/]"
    LOG_LEVEL_SUCCESS_TPL: str = "[reverse green] SUCCS  [/]"
    LOG_LEVEL_LOG_TPL: str = "[reverse chartreuse4] LOG    [/]"
    LOG_LEVEL_TIME_TPL: str = "[reverse spring_green4] TIME   [/]"
    LOG_LEVEL_WARN_TPL: str = "[reverse bright_red] WARN   [/]"
    LOG_LEVEL_WARNING_TPL: str = "[reverse bright_red] WARN   [/]"
    LOG_LEVEL_FATAL_TPL: str = "[reverse bright_red] FATAL  [/]"
    LOG_LEVEL_ERR_TPL: str = "[reverse #ff5252] ERR    [/]"
    LOG_LEVEL_ERROR_TPL: str = "[reverse #ff5252] ERROR  [/]"


config = Settings()
