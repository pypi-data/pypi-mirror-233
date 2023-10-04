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
from .fmgapi import FmgAPIError

logger = logging.getLogger(__name__)

class Vdom(FmgSystem):
    def get_all(self,device):
        print(device)
        payload = {
            "method": "get",
            "params": [{
                "fields": [["name"]],
                "loadsub": 1,
                "url": f"/dvmdb/device/{device}/vdom"
            }],
            "url": "/dvmdb/device/{device}/vdom",
            "id": 1
        }
        results = self.rest.post("",data=payload)
        #pprint.pprint(results)
        vdoms = []
        for i in results['result'][0]['data']:
            vdoms.append(i.get('name'))
        return vdoms

    def add(self,device: str, name: str):
        payload = {
            "method": "add",
            "params": [
                {
                "data": [
                    {
                    "comments": "",
                    "meta fields": {},
                    "name": name,
                    "opmode": "nat"
                    }
                ],
                "url": f"/dvmdb/device/{device}/vdom"
                }
            ],
            "id": 1
            }
        results = self.rest.post("",data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])
