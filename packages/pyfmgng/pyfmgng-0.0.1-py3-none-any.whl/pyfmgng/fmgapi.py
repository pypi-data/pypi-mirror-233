# coding: utf-8
'''
------------------------------------------------------------------------------
Copyright 2023 Per Abildgaard Toft <p@t1.dk>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
------------------------------------------------------------------------------
'''
__author__ = "Per Abildgaard Toft"

import logging
import requests
import json
from enum import Enum
import time
import urllib3
urllib3.disable_warnings()


logger = logging.getLogger(__name__)

class FmgAPIError(RuntimeError):
    pass

class FmgAPIObjectExists(RuntimeError):
    pass

class FmgApiObjectNotFound(RuntimeError):
    pass

class FmgAuthenticationError(FmgAPIError):
    pass

class FmgScriptTypes(Enum):
    exec_local_db = 0
    exec_remote_fortigate = 1
    exec_policy_db_adom = 2




class FmgRestAPI:
    ssl_verify = True
    token = None
    def __init__(self,  host:str , port:int , username: str, password: str, verify:bool = True):
        """
        Parameters
        ----------
        host : str
            FortiManager host
        port : int
            FortiManager port
        verify : bool
            Verify SSL

        Return
        -----------
            resp : str
                Reponse as JSON

        Methods
        ------
        TBD

        Raises
        ------
        FmgAPIError
            If Fortimanger returns an Error
        FmgAuthenticationError(FmgAPIError)
            Raised if auth fails
        """
        self.host = host
        self.port = port
        self.session = requests.Session()
        self.ssl_verify = verify
        self.login(username,password)


    @property
    def base_url(self) -> str:
        return f"https://{self.host}:{self.port}/jsonrpc"


    def raw_request(self, method: str,  params: dict, data: str) -> str:
        """
        Parameters
        ----------
        method : str
            HTTP Request Method: GET, POST, PUT, PATCH, DELETE
        params : dict
            Dictionary with http post parameters
        data : dict
            Dict with request payload

        Returns:
        --------
         Json encoded response: str

        Raises:
        -------
        FmgAPIError
            In case Server returns an errror
        """
        #Encode json string, if a dict or list was passed
        if not isinstance(data,(dict)):
            raise Exception("Passed data not a dict")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["AuthToken"] = self.token
            data['session'] = self.token


        json_data = json.dumps(data)

        try:
            uri = f'{self.base_url}'

            resp = self.session.request(
                method,
                uri,
                params=params,
                data=json_data,
                headers=headers,
                verify=self.ssl_verify
            )
        except requests.RequestException as e:
            raise FmgAPIError(str(e)) from e
        finally:
            logger.debug(
                f"Request <{method} {uri} params={params} json={json_data} "
                f"headers={headers}; response={resp}"
            )

        if resp.status_code == 401:
            raise FmgAPIError(f"Authentication failed: {resp}")
        elif resp.status_code == 404:
            raise FmgAPIError("API Endpoint not found: uri")
        elif resp.status_code >= 400:
            try:
                err = resp.json().get("errors", "Unknown error")
                raise FmgAPIError(err)
            except (TypeError, ValueError):
                FmgAPIError(resp.text)
        if resp.ok:
            try:
                return resp.json()
            except (TypeError, ValueError) as e:
                raise FmgAPIError(
                    f'JSON deserialization failed for {method} {uri} params={params} data={json_data} Error: {e}'
                )

    def post(self, params: dict = None, data: dict = None):
        """
        HTTP Post request to Fortimanager

        Parameters
        ----------
        params : dict
            Dictionary with http post parameters
        data : dict
            Dict with request payload

        Returns:
        --------
            Json encoded response: str

        Raises:
        -------
        FmgAPIError
            In case Server returns an errror
        """
        return self.raw_request("POST",params,data)


    def login(self, username: str, password: str) -> str:
        """
        Login to FortiManager

        Parameters:
        ----------
        username : str
            FortiManager username
        password: str
            FortiManager password
        """
        if not username:
            raise FmgAuthenticationError("Missing username")
        if not password:
            raise FmgAuthenticationError("Missing password")

        payload = {
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "data": {
                        "passwd": password,
                        "user": username,
                    },
                    "url": "/sys/login/user"
                }
            ]
        }
        response = self.post(data=payload)

        if 'session' in response:
            self.token = response['session']
        else:
            raise FmgAuthenticationError("Auth to FortiManager failed")

    def logout(self):
        """
        Logout of FortiManager
        """
        payload = { "method": "exec", "params": [{"data": [{"unlocked": True}], "url": "sys/logout"}], "id": 1}
        self.post(params=None, data=payload)



    def task_get(self,task_id):
        payload = {
            "method": "get",
            "params": [
                {
                "url": f"/task/task/{task_id}"
                }
            ],
            "id": 1
            }
        return self.post(params=None, data=payload)

    def task_get_line(self,task_id):
        payload = {
            "method": "get",
            "params": [
                {
                "loadsub": 0,
                "url": f"/task/task/{task_id}/line"
                }
            ],
            "session": "string",
            "id": 1
            }
        return self.post(data=payload)

    def wait_for_task(self,task_id, verbose = False):
            if verbose == True: print(f"Task id {task_id} running...")
            task_running=True
            task_lines = []
            task = None
            while(task_running):
                    time.sleep(3)
                    task = self.task_get_line(task_id)
                    print(f"Task {task['result'][0]['data'][-1]['percent']}%")
                    if len(task['result'][0]['data']) > 0 and 'percent' in task['result'][0]['data'][-1]:
                        if task['result'][0]['data'][-1]['percent'] == 100:
                            task_running=False
                            #Task is done, collect output
                            for line in task['result'][0]['data']:
                                task_lines.append(line['detail'])
            if verbose == True:
                print(f"Task id {task_id} completed:")
                for line in task_lines:
                        print(f"\t {line}")
            return task

    def get_device_logs(self,device_name:str) -> list:
        payload= {
            "method": "get",
            "params": [
                {
                    "url": f"/dvmdb/script/log/latest/device/{device_name}"
                }
            ],
            "id": 1
            }
        return self.post(data=payload)['result'][0]['data']['content']
