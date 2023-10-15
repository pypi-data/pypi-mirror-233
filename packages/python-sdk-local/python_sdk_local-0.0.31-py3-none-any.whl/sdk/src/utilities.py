import sys
import os
import datetime
from dotenv import load_dotenv
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.constants import *  # noqa: E402¸
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)


def timedelta_to_time_format(timedelta: datetime.timedelta):
    TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "timedelta_to_time_format()"
    logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)
    # The following line will cause TypeError: Object of type timedelta is not JSON serializable
    # logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME, object={'timedelta':  timedelta})

    # Calculate the total seconds and convert to HH:MM:SS format
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    logger.end(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME,
               object={'formatted_time':  formatted_time})
    return formatted_time


def is_list_of_dicts(obj):
    IS_LIST_OF_DICTS_FUNCTION_NAME = "is_list_of_dicts()"
    logger.start(IS_LIST_OF_DICTS_FUNCTION_NAME, object={"obj": obj})
    if not isinstance(obj, list):
        is_list_of_dicts_result = False
        logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={"is_list_of_dicts_result": is_list_of_dicts_result})
        return is_list_of_dicts_result
    for item in obj:
        if not isinstance(item, dict):
            is_list_of_dicts_result = False
            logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={'is_list_of_dicts_result': is_list_of_dicts_result})
            return is_list_of_dicts_result
    is_list_of_dicts_result = True
    logger.end(IS_LIST_OF_DICTS_FUNCTION_NAME, object={'is_list_of_dicts_result': is_list_of_dicts_result})
    return is_list_of_dicts_result
