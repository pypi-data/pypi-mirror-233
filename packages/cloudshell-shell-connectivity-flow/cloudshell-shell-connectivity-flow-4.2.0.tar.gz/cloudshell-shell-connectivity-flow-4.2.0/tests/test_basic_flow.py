import json
from unittest.mock import Mock

import pytest

from cloudshell.shell.flows.connectivity.basic_flow import AbstractConnectivityFlow
from cloudshell.shell.flows.connectivity.models.connectivity_model import (
    ConnectivityActionModel,
)
from cloudshell.shell.flows.connectivity.models.driver_response import (
    ConnectivityActionResult,
)
from tests.base import create_net_ad, create_request


@pytest.fixture()
def connectivity_flow(parse_connectivity_request_service):
    class ConnectivityFlow(AbstractConnectivityFlow):
        IS_SUCCESS = True

        def _generic_change_vlan_fn(
            self, action: ConnectivityActionModel
        ) -> ConnectivityActionResult:
            if self.IS_SUCCESS:
                return ConnectivityActionResult.success_result_vm(
                    action, "successful", "mac address"
                )
            else:
                return ConnectivityActionResult.fail_result(action, "fail")

        _set_vlan = _generic_change_vlan_fn
        _remove_vlan = _generic_change_vlan_fn

    return ConnectivityFlow(parse_connectivity_request_service)


def test_connectivity_flow(connectivity_flow, driver_request):
    res = connectivity_flow.apply_connectivity(json.dumps(driver_request))
    aid = "96582265-2728-43aa-bc97-cefb2457ca44_0900c4b5-0f90-42e3-b495"
    assert json.loads(res) == {
        "driverResponse": {
            "actionResults": [
                {
                    "actionId": aid,
                    "type": "removeVlan",
                    "updatedInterface": "mac address",
                    "infoMessage": "removeVlan 10-11 applied successfully",
                    "errorMessage": "",
                    "success": True,
                }
            ]
        }
    }


def test_connectivity_flow_failed(connectivity_flow, driver_request):
    connectivity_flow.IS_SUCCESS = False
    res = connectivity_flow.apply_connectivity(json.dumps(driver_request))
    assert json.loads(res) == {
        "driverResponse": {
            "actionResults": [
                {
                    "actionId": (
                        "96582265-2728-43aa-bc97-cefb2457ca44_0900c4b5-0f90-42e3-b495"
                    ),
                    "type": "removeVlan",
                    "updatedInterface": "centos",
                    "infoMessage": "",
                    "errorMessage": (
                        "Failed to removeVlan 10-11 for centos on VM ID vm_uid for vNIC"
                        " vnic. Error: fail"
                    ),
                    "success": False,
                }
            ]
        }
    }


def test_request_without_vlan_service(connectivity_flow):
    request = {
        "driverRequest": {
            "actions": [
                {
                    "connectionId": "f8f81164-c469-4575-b5eb-96aef13ddb38",
                    "connectionParams": {
                        "vlanId": "2",
                        "mode": "Access",
                        "vlanServiceAttributes": [
                            {
                                "attributeName": "Allocation Ranges",
                                "attributeValue": "2-4094",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "Isolation Level",
                                "attributeValue": "Exclusive",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "Access Mode",
                                "attributeValue": "Access",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "VLAN ID",
                                "attributeValue": "",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "Pool Name",
                                "attributeValue": "",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "Virtual Network",
                                "attributeValue": "",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "Default VLAN",
                                "attributeValue": "",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "QnQ",
                                "attributeValue": "False",
                                "type": "vlanServiceAttribute",
                            },
                            {
                                "attributeName": "CTag",
                                "attributeValue": "",
                                "type": "vlanServiceAttribute",
                            },
                        ],
                        "type": "setVlanParameter",
                    },
                    "connectorAttributes": [
                        {
                            "attributeName": "Selected Network",
                            "attributeValue": "2",
                            "type": "connectorAttribute",
                        }
                    ],
                    "actionTarget": {
                        "fullName": "arista1/Chassis 0/Ethernet2",
                        "fullAddress": "192.168.105.53/CH0/P2",
                        "type": "actionTarget",
                    },
                    "customActionAttributes": [],
                    "actionId": "f8f81164-c469-4575-b5eb-96aef13ddb38_d275f4fa-7264-4c7f-90ad-fe63a29e2628",  # noqa
                    "type": "setVlan",
                }
            ]
        }
    }
    connectivity_flow.apply_connectivity(json.dumps(request))


def test_connectivity_flow_set_vlan(connectivity_flow, driver_request):
    driver_request["driverRequest"]["actions"][0]["type"] = "setVlan"
    res = connectivity_flow.apply_connectivity(json.dumps(driver_request))
    aid = "96582265-2728-43aa-bc97-cefb2457ca44_0900c4b5-0f90-42e3-b495"
    assert json.loads(res) == {
        "driverResponse": {
            "actionResults": [
                {
                    "actionId": aid,
                    "type": "setVlan",
                    "updatedInterface": "mac address",
                    "infoMessage": "setVlan 10-11 applied successfully",
                    "errorMessage": "",
                    "success": True,
                }
            ]
        }
    }


def test_connectivity_flow_abstract_methods(parse_connectivity_request_service):
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        AbstractConnectivityFlow(parse_connectivity_request_service)


def test_abstract_methods_raises(parse_connectivity_request_service, action_model):
    class TestClass(AbstractConnectivityFlow):
        def _set_vlan(self, action: ConnectivityActionModel):
            return super()._set_vlan(action_model)

        def _remove_vlan(self, action: ConnectivityActionModel):
            return super()._remove_vlan(action_model)

    inst = TestClass(parse_connectivity_request_service)
    with pytest.raises(NotImplementedError):
        inst._set_vlan(action_model)

    with pytest.raises(NotImplementedError):
        inst._remove_vlan(action_model)


def test_set_vlan_request_returns_one_response_action(connectivity_flow):
    action = create_net_ad()
    request = create_request(action)

    res = connectivity_flow.apply_connectivity(request)

    assert res
    action_results = json.loads(res)["driverResponse"]["actionResults"]
    assert len(action_results) == 1


def test_do_not_run_set_vlan_if_remove_vlan_failed(connectivity_flow):
    action = create_net_ad()
    request = create_request(action)

    connectivity_flow.IS_SUCCESS = False
    connectivity_flow._set_vlan = Mock()
    res = connectivity_flow.apply_connectivity(request)

    assert res
    action_results = json.loads(res)["driverResponse"]["actionResults"]
    assert len(action_results) == 1
    assert action_results[0]["success"] is False
    connectivity_flow._set_vlan.assert_not_called()


def test_do_run_set_vlan_if_remove_vlan_success(parse_connectivity_request_service):
    def return_success_result(action):
        return ConnectivityActionResult.success_result(action, "successful")

    class TestedConnectivityFlow(AbstractConnectivityFlow):
        _remove_vlan = Mock(side_effect=return_success_result)
        _set_vlan = Mock(side_effect=return_success_result)

    action = create_net_ad()
    request = create_request(action)

    flow = TestedConnectivityFlow(parse_connectivity_request_service)
    res = flow.apply_connectivity(request)

    assert res
    flow._remove_vlan.assert_called_once()
    flow._set_vlan.assert_called_once()


def test_failed_response_if_remove_vlan_failed(parse_connectivity_request_service):
    class TestedConnectivityFlow(AbstractConnectivityFlow):
        def _remove_vlan(self, a: ConnectivityActionModel):
            1 / 0

        _set_vlan = None

    action = create_net_ad(set_vlan=False)
    request = create_request(action)

    flow = TestedConnectivityFlow(parse_connectivity_request_service)
    res = flow.apply_connectivity(request)

    assert res
    res = json.loads(res)
    assert len(res["driverResponse"]["actionResults"]) == 1
    action_result = res["driverResponse"]["actionResults"][0]
    assert action_result["success"] is False
    emsg = "division by zero"
    assert emsg in action_result["errorMessage"]
