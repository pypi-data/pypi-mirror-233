from typing import Dict, List, Any, Tuple, Union, Callable
import requests
from requests import Response
import logging

logger = logging.getLogger(__name__)


class TFQueryError(BaseException):
    """Raised if any query to TF returns an error."""
    pass


# example tf_info
# { "name": "MainTF",
#   "url": "https://tf.intelligent-artifacts.com:8090",
#   "api_key": "ABCD-1234"
# }

class TFClient:
    """Thinkflux Client Wrapper (interface to TF REST API)
    """

    def __init__(self, tf_info: dict, verify: bool = True) -> None:

        self._tf_info = tf_info

        self._url = tf_info['url']
        self._api_key = tf_info['api_key']
        self.name = tf_info['name']

        self.session = requests.Session()
        self.session.headers['X-API-KEY'] = self._api_key
        self.verify = verify
        self.session.verify = verify

    def set_verify(self, verify: bool):
        self.verify = verify
        self.session.verify = verify

    def _query(self,
               query_method: Callable,
               path: str,
               timeout: float = None,
               **kwargs) -> Response:
        response = query_method(path, verify=self.verify,
                                timeout=timeout, **kwargs)
        if response.status_code != 200:
            raise TFQueryError(
                f"Bad response {response} from TF: {response.content}")
        return response

    def ping(self) -> str:
        response = requests.get(self._url + '/ping', verify=self.verify)
        if response.status_code != 200:
            raise TFQueryError("Failed to ping Thinkflux")
        return response.text

    def show_status(self) -> dict:

        return self._query(requests.get, self._url + '/show_status').json()

    def clear_all_kbs(self) -> dict:

        return self._query(requests.get, self._url + '/clear_all_kbs').json()

    def clear_wm(self) -> dict:

        return self._query(requests.get, self._url + '/clear_wm').json()

    def clear_concepts_and_instances(self) -> dict:

        return self._query(requests.get, self._url + '/clear_concepts_and_instances').json()

    def add_schema_symbol_information(self) -> Response:

        return self._query(requests.get, self._url + '/add_schema_symbol_information')

    def observe(self, data: dict) -> dict:
        """Observe data on Thinkflux

        Args:
            data (dict): data percept to observe

        """

        return self._query(requests.post, self._url + '/observe', json=data).json()

    def add_interface_nodes(self, agent_config: dict) -> dict:
        """Add an interface node from GAIuS agent to Thinkflux

        Args:
            agent_config (dict): dictionary with configuration details for interface node

        agent_config dict needs the following fields:
        {
            "name": str,
            "domain: str,
            "secure": bool,
            "api_key": str,
            "interface_nodes": List[str]
        }

        """

        return self._query(requests.post, self._url + '/add_interface_nodes', json=agent_config).json()

    def list_interface_nodes(self) -> dict:

        return self._query(requests.get, self._url + '/list_interface_nodes').json()

    def delete_interface_nodes(self, data: dict) -> Response:

        return self._query(requests.post, self._url + '/delete_interface_nodes', json=data).json()

    def get_model_association_networks(self) -> Response:

        return self._query(requests.get, self._url + '/get_model_association_networks')

    def timer(self) -> Response:

        return self._query(requests.get, self._url + '/timer')

    def update_schema(self, data: dict) -> Response:

        return self._query(requests.post, self._url + '/update_schema', json=data)

    def bootstrap_concepts(self,
                           hierarchy: bool = False,
                           labelled: bool = False,
                           use_labels_for_concepts: bool = False,
                           use_labels_for_hierarchy: bool = False,
                           subsequence_clustering: bool = False) -> Response:
        json_obj = {'hierarchy': hierarchy,
                    'labelled': labelled,
                    'use_labels_for_concepts': use_labels_for_concepts,
                    'use_labels_for_hierarchy': use_labels_for_hierarchy,
                    'subsequence_clustering': subsequence_clustering}
        return self._query(requests.post, self._url + '/bootstrap_concepts', json=json_obj)

    def investigate(self, data: dict) -> Response:

        return self._query(requests.post, self._url + '/investigate_tf', json=data)

    def dreamer(self, data: dict) -> Response:

        return self._query(requests.post, self._url + '/dreamer', json=data)

    def load_schema_base(self, schema_base: dict) -> Response:

        return self._query(requests.post, self._url + '/load_sb', json=schema_base)

    def clear_all_emotives(self) -> dict:

        return self._query(requests.get, self._url + '/clear_all_emotives').json()

    def get_rules_kb(self) -> dict:

        return self._query(requests.get, self._url + '/get_rules_kb').json()

    def set_rules_kb(self, rules_kb: dict) -> dict:

        return self._query(requests.post, self._url + '/set_rules_kb', json=rules_kb).json()

    def set_symbolic_goal(self, symbolic_goal: dict) -> dict:

        return self._query(requests.post, self._url + '/set_symbolic_goal', json=symbolic_goal).json()

    def get_symbolic_goal(self) -> dict:

        return self._query(requests.get, self._url + '/get_symbolic_goal').json()

    def evaluate_world(self, data: dict) -> dict:

        return self._query(requests.post, self._url + '/evaluate_world', json=data).json()

    def get_plan(self) -> dict:

        return self._query(requests.get, self._url + '/get_plan').json()

    def get_concept(self, concept_name: str) -> dict:

        return self._query(requests.get, self._url + f"/concept/{concept_name}").json()

    def get_concepts(self) -> dict:

        return self._query(requests.get, self._url + f"/get_concepts").json()

    def get_instances(self) -> dict:

        return self._query(requests.get, self._url + f"/get_instances").json()
