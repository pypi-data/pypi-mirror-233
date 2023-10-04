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
from .fmgapi import FmgAPIError,FmgScriptTypes, FmgAPIObjectExists, FmgApiObjectNotFound

logger = logging.getLogger(__name__)

class Adom(FmgSystem):
    def lock(self) -> None:
        logger.info(f"Locking adom {self.adom_name}")
        payload = {
            "method": "exec",
            "id": 1,
            "params": [
                {
                    "url": f"/dvmdb/adom/{self.adom_name}/workspace/lock"}
                ]}
        self.rest.post(data=payload)
        logger.debug(f"{self.adom_name} locked")

    def unlock(self):
        logger.info(f"Unlocking adom {self.adom_name}")
        payload_object = {
            "method": "exec",
            "params": [
                {"url": f"/dvmdb/adom/{self.adom_name}/workspace/unlock"}],
                "id": 1
                }
        self.rest.post(data=payload_object)
        logger.info(f"{self.adom_name} unlocked")

    def commit(self):
        payload_object = {
            "method": "exec",
            "params": [{
                "url": f"/dvmdb/adom/{self.adom_name}/workspace/commit"
                }],
                "id": 1
            }
        results = self.rest.post(data=payload_object)
        logger.info(f"{self.adom_name} comitted")


    def vdom_add(self, device: str, name: str):
        payload = {
            "method": "add",
            "params": [
                {
                "data": [
                    {
                    "comments": "",
                    "meta fields": {},
                    "name": str(name),
                    "opmode": "nat"
                    }
                ],
                "url": f"/dvmdb/adom/{self.adom_name}/device/{device}/vdom"
                }
            ],
            "id": 1
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIObjectExists(results['result'][0]['status']['message'])

    def vdom_delete(self,device:str, vdom:str ):
        payload = {
            "method": "delete",
            "params": [
                {
                "url": f"/dvmdb/device/{device}/vdom/{vdom}"
                }
            ],
            "id": 1
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])

    def script_upload_remote_fg(self, script_name: str, script_data: str):
        payload = \
            {
                "method": "add",
                "params": [{
                    "url": f"/dvmdb/adom/{self.adom_name}/script/",
                    "data": {
                        "name": script_name,
                        "content": script_data,
                        "target": FmgScriptTypes.exec_remote_fortigate.value,
                        "type": 1
                    }}],
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])



    def script_run(self, script_name: str,device: str,vdom:str):
        payload = {
            "method": "exec",
            "params": [
                {
                "data": {
                    "adom": self.adom_name,
                    "scope": [
                    {
                        "name": device,
                        "vdom": vdom,
                    }
                    ],
                    "script": script_name,
                },
                "url": f"/dvmdb/adom/{self.adom_name}/script/execute"
                }
            ],
            "id": 1
        }
        results = self.rest.post(data=payload)
        if results['result'][0]['status'].get('code') == -3:
            raise FmgApiObjectNotFound (results['result'][0]['status'].get('message'))

        if 'task' in results['result'][0]['data']:
            res = self.rest.wait_for_task( results['result'][0]['data']['task'], verbose=True)
            if res['result'][0]['data'][0]['state'] != 4:
                print(f"Script has errors on {device}:")
                print(self.rest.get_device_logs(device))

        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])


    def script_delete(self, script_name: str):
        payload = \
            {
                "method": "delete",
                "params": [{
                    "url": f"/dvmdb/adom/{self.adom_name}/script/{script_name}",
                }],
                "id": 1,
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgApiObjectNotFound(results['result'][0]['status']['message'])

    def script_get_all(self):
        payload = {
            "method": "get",
            "params": [
                {
                    "url": f"/dvmdb/adom/{self.adom_name}/script/"
                }
                ],
        }
        return self.rest.post(data=payload)

    def install(self,device_name:str , vdom_name:str):
        payload = {
            "method": "exec",
            "params": [{
                "data": {
                    "adom": self.adom_name,
                    "scope": [
                    {
                        "name": device_name,
                        "vdom": vdom_name,
                    }
                    ]
                },
                "url": "/securityconsole/install/device"
                }
            ],
            "id": 1
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])

    def policy_package_create(self,pkg_name: str):
        payload = {
                "method": "set",
                "params":
                    [
                        {
                            "data": [{
                                "name": pkg_name,
                                "type": "pkg"
                            }, ],
                            "url": f"/pm/pkg/adom/{self.adom_name}/"
                        }
                    ]
            }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])

    def policy_package_install_target(self, pkg_name: str, device_name: str, vdom: str = "root"):
        payload = {
             "method": "add",
             "params": [{
                "data": [{
                        "name": f"{device_name}",
                        "vdom": f"{vdom}"
                    }],
                "url": f"pm/pkg/adom/{self.adom_name}/{pkg_name}/scope member"
                }]
        }
        results = self.rest.post(data=payload)
        if not results['result'][0]['status']['message'] == "OK":
            raise FmgAPIError(results['result'][0]['status']['message'])

