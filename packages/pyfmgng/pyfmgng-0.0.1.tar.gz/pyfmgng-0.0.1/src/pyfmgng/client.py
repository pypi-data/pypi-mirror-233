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

from .fmgapi import FmgRestAPI
from .vdom import Vdom
from .adom import Adom
from .firewall import Firewall

logger = logging.getLogger(__name__)


class FmgClient:
    def __init__(self,  host: str, username: str, password: str, adom_name: str = "root", verify:bool = False, port: int = 443,):
        self.adom_name = adom_name
        self.rest = FmgRestAPI(host,port, username, password, verify)
        self.adom = Adom(self.rest,adom_name)
        self.vdom = Vdom(self.rest,adom_name)
        self.firewall = Firewall(self.rest,adom_name)


    def install(self, device_name: str, vdom_name: str):
        payload = {
            "method": "exec",
            "params": [
                {
                "data": {
                    "adom": self.adom_name,
                    "scope": [
                    {
                        "name": device_name,
                        "vdom": vdom_name
                    }
                    ]
                },
                "url": "/securityconsole/install/device"
                }
            ],
            "session": "string",
            "id": 1
            }
        results = self.rest.post("",data=payload)

        if 'task' in results['result'][0]['data']:
            task_id = results['result'][0]['data']['task']
            self.rest.wait_for_task(task_id, verbose=True)

        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])