import sys
import os
import datetime
from dotenv import load_dotenv
from python_sdk_local.sdk.src import utilities

sys.path.append(os.getcwd())
from python_sdk_local.sdk.src import utilities  # noqa: E402
from python_sdk_local.sdk.src.constants import *  # noqa: E402
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=OBJECT_TO_INSERT_TEST)

TEST_TIME_DELTA = datetime.timedelta(seconds=25853)
TEST_TIME_FORMAT = "07:10:53"


def test_timedelta_to_time_format():
    TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "test_timedelta_to_time_format"
    logger.start(TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)

    time_format = utilities.timedelta_to_time_format(TEST_TIME_DELTA)
    assert time_format == TEST_TIME_FORMAT

    logger.end(TEST_TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)


def test_is_list_of_dicts():
    TEST_IS_LIST_OF_DICTS_METHOD_NAME = "test_is_list_of_dicts"
    logger.start(TEST_IS_LIST_OF_DICTS_METHOD_NAME)

    assert utilities.is_list_of_dicts([]) == True
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}]) == True
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, 3]) == False
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, 'c']) == False
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, {'c': 3}]) == True
    assert utilities.is_list_of_dicts([{'a': 1}, {'b': 2}, {'c': {'d': 5}}, 4]) == False

    logger.end(TEST_IS_LIST_OF_DICTS_METHOD_NAME)
