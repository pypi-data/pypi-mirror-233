'''Implements the COMCOM interface.'''
import functools
import json
from typing import Dict, List, Any, Tuple, Union
import requests


class COMCOMQueryError(BaseException):
    """Raised if any query to any node returns an error."""
    pass


class COMCOMConnectionError(BaseException):
    """Raised if connecting to any node returns an error."""
    pass


def _ensure_connected(f):
    @functools.wraps(f)
    def inner(self, *args, **kwargs):
        if not self._connected:
            raise COMCOMConnectionError(
                'Not connected to a COMCOM instance. You must call `connect()` on a COMCOMClient instance before making queries'
            )
        return f(self, *args, **kwargs)

    return inner


def _remove_unique_id(response: dict) -> dict:
    """Return *response* with the key 'unique_id' removed regardless of nesting."""
    if isinstance(response, dict):
        if 'unique_id' in response:
            del response['unique_id']
        for value in response.values():
            if isinstance(value, dict):
                _remove_unique_id(value)
    return response


class COMCOMClient:
    '''Interface for interacting with COMCOM. Creating/interacting with input_slots
       and connecting agents to COMCOM'''

    def __init__(self, comcom_info: dict, verify=True):
        self.session = requests.Session()
        self._comcom_info = comcom_info
        self.name = comcom_info['name']
        self._domain = comcom_info['domain']
        self._api_key = comcom_info['api_key']
        self._headers = {'X-API-KEY': self._api_key}
        self._connected = False
        self.send_unique_ids = True
        self._verify = verify

        if 'secure' not in self._comcom_info or self._comcom_info['secure']:
            self._secure = True
            if not self.name:
                self._url = 'https://{domain}/'.format(**self._comcom_info)
            else:
                self._url = 'https://{name}.{domain}/'.format(
                    **self._comcom_info)
        else:
            self._secure = False
            if not self.name:
                self._url = 'http://{domain}/'.format(**self._comcom_info)
            else:
                self._url = 'http://{name}.{domain}/'.format(
                    **self._comcom_info)

    def connect(self) -> Dict:
        """
        Establishes initial connection to COMCOM, then allows calling of other function to 
        """
        response_data = self.session.get(
            self._url + 'connect', verify=self._verify, headers=self._headers).json()

        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise COMCOMConnectionError("Connection failed!", response_data)

        if response_data['status'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': response_data['status']}

    '''def disconnect(self) -> Dict:
        """Establishes initial connection to COMCOM, then allows calling of other function to 
        """
        response_data = self.session.get(self._url + 'connect', verify=self._verify, headers=self._headers).json()

        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise COMCOMConnectionError("Connection failed!", response_data)

        self._connected = False

        return {'connection': response_data['status']}'''

    @_ensure_connected
    def _query(
        self, query_method: Any, path: str, data: Union[dict, str] = None, unique_id: str = None
    ) -> Union[dict, Tuple[dict, str]]:
        """Internal helper function to make a REST API call with the given *query* and *data*."""
        if not self._connected:
            raise COMCOMConnectionError(
                'Not connected to a agent. You must call `connect()` on a AgentClient instance before making queries'
            )
        result = {}
        if unique_id is not None:
            if data:
                data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}

        data = json.loads(json.dumps(data))

        full_path = f'{self._url}{path}'
        try:
            if data is not None:
                response = query_method(full_path, verify=self._verify,
                                        headers=self._headers, json=data)
            else:
                response = query_method(
                    full_path, verify=self._verify, headers=self._headers)
            response.raise_for_status()
            response = response.json()
            if response['status'] != 'okay':
                raise COMCOMQueryError(response['message'])
            if not self.send_unique_ids:
                response = _remove_unique_id(response['message'])
            else:
                response = response['message']
        except Exception as exception:
            raise COMCOMQueryError(str(exception)) from None

        if unique_id is not None:
            return response, unique_id

        return response

    def connect_to_agent(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function to attempt to connect to an accessible agent on the network to COMCOM,
            which can then be later used for other purposes
        '''
        return self._query(self.session.post, 'connect_to_agent', data=data)

    def disconnect_agent(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call that disconnects from agent with specific agent_id, and removes it
            from all input_slots
        '''
        return self._query(self.session.post, 'disconnect_agent', data=data)

#     def modify_agent(self, data : Dict) -> Union[dict, Tuple[dict, str]]:
#         '''
#             Function call to set agent parameters such as ingress/outgress nodes, or modify genes
#         '''
#         return self._query(self.session.post, 'config_agent', data=data)

    def call_agent_command(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to pass data through comcom and call command on agent
        '''
        return self._query(self.session.post, 'call_agent_command', data=data)

    def clear_agents(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call that removes all connected agents in COMCOM, and in its input_slots.
            Does not delete input_slots which will continue processing data, and sending it nowhere.
        '''
        return self._query(self.session.post, 'clear_agents', data={})

    def connect_input_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call which takes in config json and construction an input_slot based
            on it.
        '''
        return self._query(self.session.post, 'connect_input_slot', data=data)

    def connect_output_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call which takes in config json and construction an output_slot and pipeline based
            on it.
        '''
        return self._query(self.session.post, 'connect_output_slot', data=data)

    def disconnect_input_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function that takes in unique input_slot_id, and deletes it and its pipeline from COMCOM.
            Does not modify which agents are connected, and stops processing of any data sent through
            that input_slot
        '''
        return self._query(self.session.post, 'disconnect_input_slot', data=data)

    def modify_input_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Complex function call which can add agents, delete agents, rearrange pipeline functions, 
            insert functon into pipeline, modify parameters, or remove functions from pipeline.
        '''
        return self._query(self.session.post, 'modify_input_slot', data=data)

    def modify_output_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Complex function call which can add agents, delete agents, rearrange pipeline functions, 
            insert functon into pipeline, modify parameters, or remove functions from pipeline.
        '''
        return self._query(self.session.post, 'modify_output_slot', data=data)

    def toggle_input_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function which sets flag to prevent input slot from processing and sending data to
            agents that are connected to it
        '''
        return self._query(self.session.post, 'toggle_input_slot', data=data)

    def query_input_slot(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function which sets flag to activate an agent for a single input
        '''
        return self._query(self.session.post, 'query_input_slot', data=data)

    def clear_input_slots(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call that tells COMCOM to clear all input slots, thus ending their data processing
        '''
        return self._query(self.session.post, 'clear_input_slots', data={})

    def load_comcom_config(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call that takes in file path, and loads in config file that comcom has access to
            might change later to simply read the json directly, but for now its a local file
        '''

        return self._query(self.session.post, 'load_comcom_config', data=data)

    def list_comcom(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call that takes in file path, and loads in config file that comcom has access to
            might change later to simply read the json directly, but for now its a local file
        '''

        return self._query(self.session.post, 'list_comcom', data={})

    def list_agent_connections(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to list all unique agent connections in comcom
        '''
        return self._query(self.session.post, 'list_agent_connections', data={})

    def list_input_slots(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to list all input_slots in comcom
        '''
        return self._query(self.session.post, 'list_input_slots', data={})

    def list_output_slots(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to list all output_slots in comcom
        '''
        return self._query(self.session.post, 'list_output_slots', data={})

    def list_preprocessing_functions(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to list all unique agent connections in comcom
        '''
        return self._query(self.session.post, 'list_preprocessing_functions', data={})

    def get_agent_data(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data about connection with passed agent_id
        '''
        return self._query(self.session.post, 'get_agent_data', data=data)

    def get_output_slot_data(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data about output_slot with passed output_slot_id
        '''
        return self._query(self.session.post, 'get_output_slot_data', data=data)

    def get_input_slot_data(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data about input_slot with passed input_slot_id
        '''
        return self._query(self.session.post, 'get_input_slot_data', data=data)

    def query_db(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data from db
        '''
        return self._query(self.session.post, 'query_db', data=data)

    def clear_comcom(self) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data from db
        '''
        return self._query(self.session.post, 'clear_comcom', data={})

    def clear_outputslot_command_queue(self, data: Dict) -> Union[dict, Tuple[dict, str]]:
        '''
            Function call to get data from db
        '''
        return self._query(self.session.post, 'clear_outputslot_command_queue', data=data)
