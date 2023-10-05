import json
from abc import ABC, abstractmethod
from collections.abc import Generator

from .helpers.types import ActionDict
from .helpers.vlan_helper import (
    iterate_dict_actions_by_vlan_range,
    patch_virtual_network,
    patch_vlan_service_vlan_id,
)
from .helpers.vnic_helpers import (
    iterate_dict_actions_by_interface,
    iterate_dict_actions_by_requested_vnic,
)
from .models.connectivity_model import ConnectivityActionModel


class AbstractParseConnectivityService(ABC):
    @abstractmethod
    def get_actions(self, request: str) -> list[ConnectivityActionModel]:
        raise NotImplementedError()


class ParseConnectivityRequestService(AbstractParseConnectivityService):
    def __init__(
        self,
        is_vlan_range_supported: bool,
        is_multi_vlan_supported: bool,
        connectivity_model_cls: type[ConnectivityActionModel] = ConnectivityActionModel,
    ):
        """Parse a connectivity request and returns connectivity actions.

        :param is_vlan_range_supported: Indicates if VLAN ranges are supported
            like "120-130"
        :param is_multi_vlan_supported: Indicates if device supports comma separated
            VLAN request like "45, 65, 120-130"
        :param connectivity_model_cls: model that will be returned filled with request
            actions values
        """
        self.is_vlan_range_supported = is_vlan_range_supported
        self.is_multi_vlan_supported = is_multi_vlan_supported
        self.connectivity_model_cls = connectivity_model_cls

    def _iterate_dict_actions(self, request: str) -> Generator[ActionDict, None, None]:
        dict_actions = json.loads(request)["driverRequest"]["actions"]

        patched_actions = []
        for dict_action in dict_actions:
            patch_vlan_service_vlan_id(dict_action)
            patch_virtual_network(dict_action)
            patched_actions.append(dict_action)

        actions_split_by_vlan_range = []
        for dict_action in patched_actions:
            for new_action in iterate_dict_actions_by_vlan_range(
                dict_action, self.is_vlan_range_supported, self.is_multi_vlan_supported
            ):
                actions_split_by_vlan_range.append(new_action)

        actions_split_by_requested_vnic = []
        for dict_action in actions_split_by_vlan_range:
            for new_action in iterate_dict_actions_by_requested_vnic(dict_action):
                actions_split_by_requested_vnic.append(new_action)

        actions_split_by_iface: list[ActionDict] = []
        # for Cloud Provides in remove actions if in set action was specified several
        # vNICs for the same VLAN Service
        for dict_action in actions_split_by_requested_vnic:
            for new_action in iterate_dict_actions_by_interface(dict_action):
                actions_split_by_iface.append(new_action)

        # for backward compatibility
        yield from actions_split_by_iface

    def get_actions(self, request: str) -> list[ConnectivityActionModel]:
        return [
            self.connectivity_model_cls.parse_obj(da)
            for da in self._iterate_dict_actions(request)
        ]
