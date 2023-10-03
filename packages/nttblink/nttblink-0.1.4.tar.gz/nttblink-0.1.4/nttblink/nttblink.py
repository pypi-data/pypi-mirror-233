import os
import requests
import logging
import json
from pprint import pprint as pp

from dotenv import load_dotenv

class BlinkHandler(logging.Handler):
    def __init__(self, blink_instance):
        super().__init__()
        self.blink_instance = blink_instance

    def emit(self, record):
        log_entry = self.format(record)
        self.blink_instance.log(log_entry)

class Blink:
    def __init__(self):
        if os.path.exists('.env'):
            print('Loading .env file')
            load_dotenv()
        try:
            blink = os.environ['BLINK']
            blink = json.loads(blink)
            print('Loaded BLINK environment variable')
            pp(blink)
        except:
            raise Exception('Could not find BLINK environment variable.')
        self.project_id = blink['project_id']
        self.token = blink['token']
        self.base_url = blink['base_url']
        self.automation_id = blink['automation_id']
        self.path_prefix = "ds"
        self.job_id = blink['job_id']
        self.survey_vars = blink['survey_vars']
        self.timeout = 10
        self.verify_variables()
        self.status('running')
        self.logger = logging.getLogger(__name__)
        self.handler = BlinkHandler(self)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def verify_variables(self):
        required = ['project_id', 'token', 'base_url', 'automation_id', 'job_id']
        for var in required:
            if self.__dict__[var.lower()] is None:
                raise Exception(f'{var} is not set in .env file or environment variables')

    def handle_error(self, response):
        error_messages = {
            403: 'Unauthorized, check your token',
            404: 'Not found, check your project id',
            500: 'Internal server error',
        }
        raise Exception(error_messages.get(response.status_code, 'Unknown error'))

    def status(self, status: str) -> dict:
        if self.job_id is None:
            raise Exception('BLINK_JOB_ID is not set in .env file or environment variables')
        if status not in ['running', 'success', 'failure']:
            raise Exception('status must be success or failure')
        response = requests.put(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/jobs/{self.job_id}', 
                                json={'status': status},
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.json()

    def log(self, message: str) -> dict:
        print(message)
        if self.job_id is None:
            raise Exception('BLINK_JOB_ID is not set in .env file or environment variables')
        response = requests.put(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/jobs/{self.job_id}', 
                                json={'message': message},
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.json()

    def secret_list(self, **kwargs) -> list:
        """
        Lists all secrets in a Blink project relating to this automation id. It takes no arguments and returns a list of secrets.
        """
        logging.info('Listing secrets')
        scope = kwargs.get('scope', 'automation')
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets?scope={scope}',
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.json()

    def secret_get(self, secret_id: int) -> dict:
        """
        Gets a secret metadata from Blink. It takes a secret ID as an argument and returns the secret data.
        """
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets/{secret_id}',
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.json()

    def secret_create(self, secret_name: str, secret_description: str, secret_data: dict, **kwargs) -> dict:
        """
        Creates a secret in Blink. It takes a secret name, description, and data as arguments
        and returns the secret ID of the created secret. The data must be a dictionary.
        """
        if not isinstance(secret_data, dict):
            raise Exception('secret_data must be a dictionary')
        if secret_name is None:
            raise Exception('secret_name is required')
        scope = kwargs.get('scope', 'automation')
        overwrite = kwargs.get('overwrite', True)
        if scope not in ['automation', 'project']:
            raise Exception('scope must be automation or project')

        body = {"name": secret_name, "description": secret_description, "data": secret_data, "scope": scope, "overwrite": overwrite}
        response = requests.post(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/secrets', 
                                 json=body,
                                 headers={'Authorization': 'Bearer ' + self.token}, 
                                 timeout=self.timeout)
        if response.status_code != 201:
            self.handle_error(response)
        print(f'Created secret {secret_name}')
        return response.json()

    def secret_set_to_env(self, **kwargs):
        """
        imports secrets from the Blink API and sets them as environment variables. 
        It loops through all the secrets, gets their data, and sets each key-value pair as an environment variable 
        with the key in uppercase and spaces replaced with underscores.
        """
        scope = kwargs.get('scope', 'automation')
        secrets = self.secret_list(scope=scope)
        print(f'Found {len(secrets)} secrets')
        for secret in secrets:
            for key, value in self.secret_get(secret['id'])['data'].items():
                key = key.upper().replace(' ', '_')
                os.environ[key] = value

    def document_list(self, **kwargs):
        """
        Lists all documents in a Blink project. It takes no arguments and returns a list of documents.
        """
        scope = kwargs.get('scope', 'automation')
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents?scope={scope}',
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.json()

    def document_download(self, document_id, path):
        """
        Downloads a file from Blink. It takes a document ID and a path as arguments
        and returns the content type of the downloaded file. The file will be saved at the path provided.
        """
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents/{document_id}',
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        with open(path, 'wb') as f:
            f.write(response.content)
        return response.headers['Content-Type']
    
    def document_download_binary(self, document_id):
        """
        Downloads a file from Blink. It takes a document ID as an argument
        and returns the content type and content of the downloaded file.
        """
        response = requests.get(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents/{document_id}',
                                headers={'Authorization': 'Bearer ' + self.token}, 
                                timeout=self.timeout)
        if response.status_code != 200:
            self.handle_error(response)
        return response.headers['Content-Type'], response.content
    
    def document_upload(self, path, **kwargs):
        """
        Uploads a file to Blink. It takes a path to a file as an argument and returns
        the document ID of the uploaded file. The file must exist at the path provided.
        """
        scope = kwargs.get('scope', 'automation')
        if not os.path.exists(path):
            raise Exception(f'File {path} does not exist')
        with open(path, 'rb') as f:
            response = requests.post(f'{self.base_url}/{self.path_prefix}/{self.project_id}/{self.automation_id}/documents',
                                     data={'scope': scope},
                                     files={'file': f},
                                     headers={'Authorization': 'Bearer ' + self.token}, 
                                     timeout=self.timeout)
        if response.status_code != 201:
            self.handle_error(response)
        return response.json()



