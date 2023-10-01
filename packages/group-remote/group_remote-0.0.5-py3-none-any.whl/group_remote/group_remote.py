# TODO: This is an example file which you should delete after implementing
import os
from circles_local_database_python.connector import Connector
# from circles_local_database_python.generic_crud.src.generic_crud import GenericCRUD
from language_local_python_package.src.language_enum_class import LanguageCode
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from url_local.url_circlez import UrlCirclez
from url_local.component_name_enum import ComponentName
from url_local.entity_name_enum import EntityName
from url_local.action_name_enum import ActionName
import requests
from dotenv import load_dotenv
load_dotenv()


GROUP_REMOTE_COMPONENT_ID = 213
GROUP_PROFILE_COMPONENT_NAME="Group Remote Python"
DEVELOPER_EMAIL="yarden.d@circ.zone"

GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT={
    'component_id':GROUP_REMOTE_COMPONENT_ID,
    'component_name':GROUP_PROFILE_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Code.value,
    'component_type':LoggerComponentEnum.ComponentType.Remote.value,
    "developer_email":DEVELOPER_EMAIL
}

GROUP_REMOTE_API_VERSION = 1


class GroupsRemote:

    def __init__(self) -> None:
        self.url_circlez = UrlCirclez()
        self.logger = Logger.create_logger(object=GROUP_REMOTE_PYTHON_LOGGER_CODE_OBJECT)
        self.brand_name = os.getenv("BRAND_NAME")
        self.env_name = os.getenv("ENVIRONMENT_NAME")



    def get_all_groups(self, langCode: LanguageCode = None): #GET
        self.logger.start("Start get_all_groups group-remote")

        query_params = {"langCode": langCode.value } if langCode else None

        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.GET_ALL_GROUPS.value, # "getAllGroups",
                query_parameters = query_params
            )

            self.logger.info("Endpoint group remote - getAllGroups action: " + url)


            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.get(url, headers=header)
            self.logger.end(f"End get_all_groups group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End get_all_groups group-remote")



    def get_group_by_name(self, groupName: str, langCode: LanguageCode = None): #GET
        self.logger.start("Start get_group_by_name group-remote")
        query_params = {}
        if langCode:
            query_params['langCode'] = langCode.value
        query_params["name"] = groupName

        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.GET_GROUP_BY_NAME.value, # "getGroupByName",
                query_parameters = query_params
            )

            self.logger.info("Endpoint group remote - getGroupByName action: " + url)

            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.get(url, headers=header)
            self.logger.end(f"End get_group_by_name group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End get_group_by_name group-remote")



    def get_group_by_id(self, groupId: str, langCode: LanguageCode = None): #GET
        self.logger.start("Start get_group_by_id group-remote")
        query_params = {"langCode": langCode.value } if langCode else None

        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.GET_GROUP_BY_ID.value, # "getGroupById",
                path_parameters = { 'groupId': groupId},
                query_parameters = query_params,  
            )

            self.logger.info("Endpoint group remote - getGroupById action: " + url)

            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.get(url, headers=header)
            self.logger.end(f"End get_group_by_id group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End get_group_by_id group-remote")



    def create_group(self, title: str, titleLangCode: str = None, parentGroupId: str = None, isInterest: bool = None, image: str = None): #POST
        self.logger.start("Start create group-remote")

        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.CREATE_GROUP.value, # "createGroup",
            )

            self.logger.info("Endpoint group remote - createGroup action: " + url)

            payload = {
                "title": title
            }

            if titleLangCode:
                payload["titleLangCode"] = titleLangCode
            if parentGroupId:
                payload["parentGroupId"] = parentGroupId
            if isInterest:
                payload["isInterest"] = isInterest
            if image:
                payload["image"] = image
        
            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.post(url, json=payload, headers=header)
            self.logger.end(f"End create group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End create group-remote")



    def update_group(self, groupId: int, title: str = None, titleLangCode: str = None, parentGroupId: str = None, isInterest: bool = None, image: str = None): #PATCH
        self.logger.start("Start update group-remote")
        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.UPDATE_GROUP.value, # "updateGroup",
                path_parameters = { 'groupId': groupId },

            )

            self.logger.info("Endpoint group remote - updateGroup action: " + url)

            payload = {
                "title": title,
            }

            if titleLangCode is not None:
                payload["titleLangCode"] = titleLangCode
            if parentGroupId is not None:
                payload["parentGroupId"] = parentGroupId
            if isInterest is not None:
                payload["isInterest"] = isInterest
            if image is not None:
                payload["image"] = image

            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.patch(url, json=payload, headers=header)
            self.logger.end(f"End update group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End update group-remote")



    def delete_group(self, groupId: int): #DELETE
        self.logger.start("Start delete group-remote")
        try:
            url = self.url_circlez.endpoint_url(
                brand_name = self.brand_name,
                environment_name = self.env_name,
                component = ComponentName.GROUP.value,
                entity = EntityName.GROUP.value,
                version = GROUP_REMOTE_API_VERSION,
                action = ActionName.DELETE_GROUP.value, # "deleteGroup",
                path_parameters = { 'groupId': groupId },
            )

            self.logger.info("Endpoint group remote - deleteGroup action: " + url)

            header = self.create_header(self.logger.userContext.get_jwt_token())

            response = requests.delete(url, headers=header)
            self.logger.end(f"End delete group-remote, response: {str(response)}")
            return response
        

        except requests.ConnectionError as exception:
            self.logger.exception("ConnectionError Exception- Network problem (e.g. failed to connect)", exception)
        except requests.Timeout as exception:
            self.logger.exception("Timeout Exception- Request timed out", exception)
        except requests.RequestException as exception:
            self.logger.exception(f"RequestException Exception- General error: {str(exception)}", exception)
        except Exception as exception:
            self.logger.exception(f"An unexpected error occurred: {str(exception)}", exception)
        
        self.logger.end(f"End delete group-remote")



    def create_header(self, jwt_token: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
        }
        return headers
        
