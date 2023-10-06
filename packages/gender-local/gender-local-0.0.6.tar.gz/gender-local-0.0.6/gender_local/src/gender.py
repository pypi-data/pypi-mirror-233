from gender_local.src.constants_gender_local import ConstantsGenderLocal
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.connector import Connector  # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=ConstantsGenderLocal.OBJECT_FOR_LOGGER_CODE)

class Gender(GenericCRUD):
    def __init__(self):
        logger.start()
        self.connector = Connector.connect("profile")
        self.cursor = self.connector.cursor()
        logger.end()

    def get_gender_id_by_title(self, title: str) -> int:
        logger.start(object={'title': title})

        query_get = 'SELECT gender_id FROM gender_ml_view WHERE title = %s'
        self.cursor.execute(query_get, (title,))
        row = self.cursor.fetchone()
        if row is None:
            logger.end(object={'gender_id': None})
            return None
        gender_id, = row

        logger.end(object={'gender_id': gender_id})
        return gender_id