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
from .fmgsystem import FmgSystem
from .dataclasses import FirewallPolicy
from typing import List
import json

logger = logging.getLogger(__name__)


class Firewall(FmgSystem):
    def get_firewall_policy(self,pkg_name:str) -> List[FirewallPolicy]:
        payload = {
            "method": "get", 
            "params": [
                {"url": f"/pm/config/adom/{self.adom_name}/pkg/{pkg_name}/firewall/policy"}
            ],
            "id": 1
            }
        firewall_policies = self.rest.post("",data=payload)['result'][0]['data']
        return [FirewallPolicy.from_json(p) for p in firewall_policies]

    def add_firewall_policy(self,p: FirewallPolicy, pkg_name:str):
        payload = {
                        "method": "add",
                        "params": [{
                                    "data": [p.to_json()],
                            "url": f"/pm/config/adom/{self.adom_name}/pkg/{pkg_name}/firewall/policy"
                        }],
                    "id": 1
        }
        print(json.dumps(payload, indent=2))