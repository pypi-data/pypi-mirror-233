
from typing import List
from dotenv import load_dotenv
from location_profile_local.src.constants_location_profile import LocationProfileLocalConstants  # noqa: E402
load_dotenv()
from logger_local.Logger import Logger # noqa: E402
from circles_local_database_python.generic_crud import GenericCRUD  # noqa: E402
from circles_local_database_python.connector import Connector   # noqa: E402


logger = Logger.create_logger(object=LocationProfileLocalConstants.OBJECT_FOR_LOGGER_CODE)


class LocationProfile(GenericCRUD):
    def __init__(self):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME)
        self.connector = Connector.connect("location_profile")
        self.cursor = self.connector.cursor()
        logger.end(INIT_METHOD_NAME)

    def get_last_location_id_by_profile_id(self, profile_id: int) -> int:
        GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_location_id_by_profile_id"
        logger.start(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})

        logger.info(object={'profile_id': profile_id})
        query_get = "SELECT location_id FROM location_profile.location_profile_view WHERE profile_id=%s ORDER BY start_timestamp DESC LIMIT 1"
        self.cursor.execute(query_get, (profile_id,))
        rows = self.cursor.fetchall()
        location_id = None
        if len(rows) > 0:
            location_id, = rows[0]

        logger.end(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_id': location_id})
        return location_id

    def get_location_ids_by_profile_id(self, profile_id: int) -> List[int]:
        GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME = "get_location_ids_by_profile_id"
        logger.start(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})

        logger.info(object={'profile_id': profile_id})
        query_get = "SELECT location_id FROM location_profile.location_profile_view WHERE profile_id=%s ORDER BY start_timestamp DESC"
        self.cursor.execute(query_get, (profile_id,))
        rows = self.cursor.fetchall()
        location_ids = [None]
        if len(rows) > 0:
            for row in rows:
                location_id, = row
                location_ids.append(location_id)

        logger.end(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_id': location_id})
        return location_ids

    def insert_location_profile(self, profile_id: int, location_id: int, lang_code: str = 'en', title: str = 'Home', title_approved=True):
        INSERT_LOCATION_PROFILE_METHOD_NAME = 'insert_location_profile'
        logger.start(INSERT_LOCATION_PROFILE_METHOD_NAME,
                     object={"location_id": location_id})

        query_insert = "INSERT INTO location_profile.location_profile_table(profile_id, location_id) VALUES (%s, %s)"
        self.cursor.execute(query_insert, (profile_id, location_id))

        reaction_id = self.cursor.lastrowid()
        query_insert_ml = "INSERT INTO location_profile.location_profile_ml_table(location_profile_id, lang_code, title, title_approved) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query_insert_ml, (reaction_id,
                            lang_code, title, title_approved))
        self.connector.commit()

        logger.end(INSERT_LOCATION_PROFILE_METHOD_NAME)
