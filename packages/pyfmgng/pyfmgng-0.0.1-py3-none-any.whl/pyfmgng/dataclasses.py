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


from dataclasses import dataclass
from dataclasses_json import dataclass_json

from typing import Dict, Optional, List, Generator
import json

@dataclass_json
@dataclass
class FirewallPolicy:
    dstaddr: list
    dstintf: list
    logtraffic: list
    name: str
    service: list
    srcaddr: list
    srcintf: list
    action: str
    nat: str
    schedule: str

    @classmethod
    def from_json(self, p: Optional[dict]):
        if p is None:
            return FirewallPolicy(
                dstaddr = "",
                dstintf = "",
                logtraffic = "",
                name = "",
                service = "",
                srcaddr = "",
                srcintf = "",
                action = "",
                nat = "",
                schedule= "")
        return FirewallPolicy(
            dstaddr = p.get('dstaddr'),
            dstintf = p.get('dstintf'),
            logtraffic = p.get('logtraffic'),
            name = p.get('name'),
            service = p.get('service'),
            srcaddr = p.get('srcaddr'),
            srcintf = p.get('srcintf'),
            action = p.get('action'),
            nat = p.get('nat'),
            schedule= p.get('schedule'),
            )

