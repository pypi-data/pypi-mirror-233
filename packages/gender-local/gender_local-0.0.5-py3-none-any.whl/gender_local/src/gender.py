from typing import Dict
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.connector import Connector  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 201
PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'gender_local/src/gender.py'

object_to_insert = {
    'component_id': PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

class Gender(GenericCRUD):
    def __init__(self):
        INIT_METHOD_NAME = "__init__"
        logger.start(INIT_METHOD_NAME)
        self.connector = Connector.connect("profile")
        self.cursor = self.connector.cursor()
        logger.end(INIT_METHOD_NAME)

    def get_gender_id_by_title(self, title: str) -> int:
        GET_GENDER_ID_BY_TITLE_METHOD_NAME = 'get_gender_id_by_title'
        logger.start(GET_GENDER_ID_BY_TITLE_METHOD_NAME, object={'title': title})

        query_get = 'SELECT gender_id FROM gender_ml_table WHERE title = %s'
        self.cursor.execute(query_get, (title,))
        row = self.cursor.fetchone()
        if row is None:
            logger.end(GET_GENDER_ID_BY_TITLE_METHOD_NAME, object={'gender_id': None})
            return None
        gender_id, = row

        logger.end(GET_GENDER_ID_BY_TITLE_METHOD_NAME, object={'gender_id': gender_id})
        return gender_id