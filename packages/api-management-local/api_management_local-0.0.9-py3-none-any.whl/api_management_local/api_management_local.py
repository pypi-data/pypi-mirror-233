# TODO: This is an example file which you should delete after implementing
from dotenv import load_dotenv
import json
from circles_local_database_python.connector import Connector
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD

API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID = 212  
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME = "api-management-local-python-package"
DEVELOPER_EMAIL = "heba.a@circ.zone"

object1 = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()

logger=Logger.create_logger(object=object1)
class APIManagementLocal( GenericCRUD):
    def __init__(self) -> None:
        pass

    @staticmethod
    # TODO Can we make this method private?
    def insert_data_into_table( data:tuple)->None:
        logger.start(object={'data':str(data)})
        try:
            json_data = {
                'api_type_id': data[0], 
                'endpoint': data[1], 
                'outgoing_header': data[2], 
                'outgoing_body': data[3], 
                 'outgoing_body_signigicant_fields_hash': data[4], 
                'incoming_message': data[5]  }
            GenericCRUD.insert(table_name="api_call.api_call_view", json_data=json_data)
            logger.end()
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
        
    @staticmethod
    # TODO This method should return both soft and hard limits
    def get_limits_by_api_type_id(api_type_id:str)->list:
        logger.start(object={'api_type_id':api_type_id})
        try:
           api_type_id_str="api_type_id="+api_type_id
           list=GenericCRUD._select_by_where(table_name="api_limit.api_limit_view",select_clause_value=api_type_id_str)
           logger.end(object={'list':str(list)})
           return list 
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
            
    @staticmethod
    def get_actual_by_api_type_id( api_type_id:int, hours: int) -> int:
        logger.start(object={'api_type_id':str(api_type_id),'hours':str(hours)})
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        try:
            # TODO: We should count only successful API calls
            cursor.execute("""
                  SELECT COUNT(*)
                  FROM api_call_view
                  WHERE api_type_id = %s
                  AND TIMESTAMPDIFF(HOUR, created_timestamp, NOW()) <= %s
                  """.format(api_type_id, hours))
            count_result = cursor.fetchone()[0]
            logger.end(object={'count_result':count_result})
            return count_result
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
    
    @staticmethod
    # TODO Can we make this method private?
    def  get_json_with_only_sagnificant_fields_by_api_type_id( json1:json, api_type_id:int)-> json:
        connection = Connector.connect("api_type")
        try:
            # TODO create public method try_to_call_api( ....) which uses insert_data_into_table() private method, get_limits_by_api_type_id() and get_actual_by_api_type_id() 
            cursor = connection.cursor()
            query = f"SELECT field_name FROM api_type.api_type_field_view WHERE api_type_id = %s"
            cursor.execute(query, (api_type_id,))
            significant_fields = [row[0] for row in cursor.fetchall()]
            data = json.loads(json1)
            filtered_data = {key: data[key] for key in significant_fields if key in data}
            filtered_json = json.dumps(filtered_data)
            logger.end(object={'filtered_json':str(filtered_json)})
            return filtered_json
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise
        

