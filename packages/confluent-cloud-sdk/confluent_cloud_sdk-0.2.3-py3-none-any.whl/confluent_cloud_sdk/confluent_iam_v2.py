#  SPDX-License-Identifier: GPL-2.0-only
#  Copyright 2022 John Mille <john@compose-x.io>


from __future__ import annotations

from datetime import datetime as dt
from datetime import timedelta as td
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from requests.models import Response
    from .client_factory import ConfluentClient

from compose_x_common.compose_x_common import keyisset

from .confluent_cloud_api import ResourcesList
from .confluent_cloud_api.iam_v2_apikey import SpecModel as IamV2ApiKey
from .confluent_cloud_api.iam_v2_serviceaccount import Spec as IamV2ServiceAccount


class IamV2Object:
    """
    IAM V2 Objects class
    """

    api_v2_path = "/iam/v2"
    api_keys_path = "/api-keys"
    services_accounts_path = "/service-accounts"

    def __init__(
        self,
        client_factory: ConfluentClient,
        display_name: str = None,
        description: str = None,
    ):
        self._resource = None
        self._resource_class = None
        self._client = client_factory
        self._id = None
        self._name = display_name
        self._description = description
        self._environment = None
        self.api_path = None

    @property
    def resource(self) -> Union[IamV2ApiKey, IamV2ServiceAccount]:
        return self._resource

    @property
    def obj_id(self) -> Union[None, str]:
        if self._resource:
            return self._resource.id.__root__
        return None

    def read(self) -> Union[dict, Response]:
        if not self._resource:
            return {}
        return self._client.get(self._resource.metadata.self)

    def update(self, description: str):
        req = self._client.patch(
            self._resource.metadata.self, data={"description": description}
        )
        if self._resource_class:
            self._resource = self._resource_class(**req.json())
        return req

    def delete(self):
        return self._client.delete(self._resource.metadata.self)


class ServiceAccount(IamV2Object):
    """
    Class to manipulate Confluent cloud service account
    """

    api_path = f"{IamV2Object.api_v2_path}{IamV2Object.services_accounts_path}"

    def __init__(
        self,
        client_factory: ConfluentClient,
        resource_id: str = None,
        display_name: str = None,
        description: str = None,
        spec: dict = None,
    ):
        super().__init__(client_factory, display_name, description)
        self._resource_class = IamV2ServiceAccount
        self._api_keys: dict = {}

        if resource_id and not spec:
            self._resource = self._resource_class(
                **client_factory.get(
                    f"{self._client.api_url}{self.api_path}/{resource_id}"
                ).json()
            )
        elif spec:
            self._resource = self._resource_class(**spec)

    @property
    def api_keys(self) -> dict[str, ApiKey]:
        return self._api_keys

    @property
    def api_keys_list(self) -> list:
        return list(self.api_keys.values())

    @property
    def friendly_name(self) -> str:
        if not self._resource:
            return ""
        if self._resource.display_name:
            return self._resource.display_name
        elif self._resource.description:
            return self._resource.description
        else:
            return self.obj_id

    def create(self):
        """
        `create <https://docs.confluent.io/cloud/current/api.html#operation/createIamV2ServiceAccount>`_
        """
        url = f"{self._client.api_url}{self.api_path}"
        if not self._description:
            description = self._name.title()
        else:
            description = self._description
        payload = {"display_name": self._name, "description": description}
        req = self._client.post(url, data=payload)
        self._resource = self._resource_class(**req.json())
        return req

    def import_api_keys(self):
        if not self._resource:
            return
        url = f"{self._client.api_url}{ApiKey.api_path}?spec.owner={self.obj_id}&page_size=50"
        req = self._client.get(url).json()
        for _api_key in req["data"]:
            owner = _api_key["spec"]["owner"]
            if owner["id"] != self.obj_id:
                continue
            try:
                new_key = ApiKey(
                    self._client,
                    spec=_api_key,
                )
                self.api_keys[new_key.obj_id] = new_key
            except Exception as error:
                print(error)
                new_key = ApiKey(
                    self._client,
                    resource_id=_api_key["id"],
                )
                self.api_keys[new_key.obj_id] = new_key

    def create_api_key(
        self,
        resource_id: str = None,
        environment_id: str = None,
        display_name: str = None,
        description: str = None,
    ) -> ApiKey:
        api_key = ApiKey(self._client)
        api_key.create(
            self.obj_id, resource_id, environment_id, display_name, description
        )
        self.api_keys[api_key.obj_id] = api_key
        return api_key

    def delete_api_key(self, api_key_id: str):
        if api_key_id in self.api_keys:
            self.api_keys[api_key_id].delete()
            del self.api_keys[api_key_id]


class ApiKey(IamV2Object):
    """
    `API Key <https://docs.confluent.io/cloud/current/api.html#section/The-Api-Keys-Model>`_
    """

    api_path = f"{IamV2Object.api_v2_path}{IamV2Object.api_keys_path}"

    def __init__(
        self,
        client_factory: ConfluentClient,
        display_name: str = None,
        description: str = None,
        resource_id: str = None,
        spec: dict = None,
    ):
        super().__init__(client_factory, display_name, description)
        self._resource_class = IamV2ApiKey

        if resource_id and not spec:
            self._resource = self._resource_class(
                **client_factory.get(
                    f"{self._client.api_url}{self.api_path}/{resource_id}"
                ).json()
            )
        elif spec:
            self._resource = self._resource_class(**spec)

    @property
    def age(self) -> Union[td, None]:
        if not self._resource:
            return None
        now = dt.now()
        return now - self.resource.metadata.created_at.replace(tzinfo=None)

    def create(
        self,
        owner_id: str,
        resource_id: str = None,
        environment_id: str = None,
        display_name: str = None,
        description: str = None,
    ):
        """
        `create <https://docs.confluent.io/cloud/current/api.html#operation/createIamV2ApiKey>`_
        """
        url = f"{self._client.api_url}{self.api_path}"

        spec: dict = {
            "owner": {"id": owner_id},
        }
        if not display_name and resource_id:
            display_name = f"{owner_id}_{resource_id}"
        if display_name:
            spec["display_name"] = display_name

        if not description and display_name:
            description = display_name.replace(r"_", " ").title()
        if description:
            spec["description"] = description

        resource: dict = {}
        if resource_id:
            resource["id"] = resource_id
        if resource and environment_id:
            resource["environment"] = environment_id
        if resource:
            spec["resource"] = resource

        req = self._client.post(
            url,
            data={"spec": spec},
        )
        self._resource = self._resource_class(**req.json())
        return req
