# Base class from which to inherit other Nautobot API classes
# This class implements a least common member view of fields that
# all Nautobot API endpoints require.

import requests
from typing import Optional, Dict, Any, Union
import os
from dotenv import load_dotenv

class NautobotBase:
    load_dotenv()

    base_url = os.getenv("NAUTOBOT_API_BASE_URL") or "http://nautobot.yourorganization.com"
    token = f"Token {os.getenv('NAUTOBOT_API_TOKEN')}" or "Token YourSecureTokenHere"
    headers = {
        "Authorization": token,
#        "Authorization": "Token 971dd4d8b01e8137ca9d39b48687492af4be60c6",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, id: Optional[str] = None, endpoint: Optional[str] = None, **kwargs):
        self.id = id
        self.endpoint = endpoint or getattr(self.__class__, "endpoint", None)
        self.extra = kwargs  # store any additional fields

    @classmethod
    def fetch(cls, object_id: Optional[str] = None, params: Optional[Dict] = None) -> Dict:
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        url = f"{cls.base_url}/{cls.endpoint}/"
        if object_id:
            url += f"{object_id}/"
        response = requests.get(url, headers=cls.headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(cls, object_id: Optional[str] = None, params: Optional[Dict] = None):
        data = cls.fetch(object_id, params)
        if object_id:
            # single object
            return cls.from_json(data)
        else:
            # multiple objects
            results = data.get("results", [])
            return {item["id"]: cls.from_json(item) for item in results}

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        # Default behavior: just store id
        return cls(id=data.get("id"), **data)


# -------------------- Location Class --------------------
class Location(NautobotBase):
    endpoint = "dcim/locations"

    def __init__(self, id: str, object_type: Optional[str] = None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.object_type = object_type

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        data_copy = data.copy()
        data_copy.pop("id", None)
        object_type = data_copy.pop("object_type", None)
        return cls(id=data["id"], object_type=object_type, **data_copy)


# -------------------- RackGroup Class --------------------
class RackGroup(NautobotBase):
    endpoint = "dcim/rack-groups"

    def __init__(
        self,
        id: str,
        display: Optional[str] = None,
        rack_count: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent: Optional[str] = None,
        location: Optional[Union[Dict[str, Any], Location]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(id=id, **kwargs)
        self.display = display
        self.rack_count = rack_count
        self.name = name
        self.description = description
        self.parent = parent

        # Handle nested Location object
        if isinstance(location, dict):
            self.location = Location.from_json(location)
        elif isinstance(location, Location):
            self.location = location
        else:
            self.location = None

        self.custom_fields = custom_fields or {}
        self.extra = kwargs

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        data_copy = data.copy()
        data_copy.pop("id", None)
        location_data = data_copy.pop("location", None)
        return cls(
            id=data["id"],
            display=data_copy.pop("display", None),
            rack_count=data_copy.pop("rack_count", None),
            name=data_copy.pop("name", None),
            description=data_copy.pop("description", None),
            parent=data_copy.pop("parent", None),
            location=location_data,
            custom_fields=data_copy.pop("custom_fields", None),
            **data_copy
        )

# -------------------- RackGroup Class --------------------
class Rack(NautobotBase):
    endpoint = "dcim/racks"

    def __init__(
        self,
        id: str,
        display: Optional[str] = None,
        device_count: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent: Optional[str] = None,
        location: Optional[Union[Dict[str, Any], Location]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(id=id, **kwargs)
        self.display = display
        self.device_count = device_count
        self.name = name
        self.description = description
        self.parent = parent

  # Handle nested Location object
        if isinstance(location, dict):
            self.location = Location.from_json(location)
        elif isinstance(location, Location):
            self.location = location
        else:
            self.location = None

        self.custom_fields = custom_fields or {}
        self.extra = kwargs

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        data_copy = data.copy()
        data_copy.pop("id", None)
        location_data = data_copy.pop("location", None)
        return cls(
            id=data["id"],
            display=data_copy.pop("display", None),
            device_count=data_copy.pop("device_count", None),
            name=data_copy.pop("name", None),
            description=data_copy.pop("description", None),
            parent=data_copy.pop("parent", None),
            location=location_data,
            custom_fields=data_copy.pop("custom_fields", None),
            **data_copy
        )

# -------------------- Device Class --------------------
class Device(NautobotBase):
    endpoint = "dcim/devices"

    def __init__(
        self,
        id: str,
        display: Optional[str] = None,
        module_count: Optional[int] = None,
        interface_count: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parent: Optional[str] = None,
        location: Optional[Union[Dict[str, Any], Location]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(id=id, **kwargs)
        self.display = display
        self.module_count = module_count
        self.name = name
        self.description = description
        self.parent = parent

  # Handle nested Location object
        if isinstance(location, dict):
            self.location = Location.from_json(location)
        elif isinstance(location, Location):
            self.location = location
        else:
            self.location = None

        self.custom_fields = custom_fields or {}
        self.extra = kwargs

    @classmethod
    def from_json(cls, data: Dict[str, Any]):
        data_copy = data.copy()
        data_copy.pop("id", None)
        location_data = data_copy.pop("location", None)
        return cls(
            id=data["id"],
            display=data_copy.pop("display", None),
            module_count=data_copy.pop("rack_count", None),
            name=data_copy.pop("name", None),
            description=data_copy.pop("description", None),
            parent=data_copy.pop("parent", None),
            location=location_data,
            custom_fields=data_copy.pop("custom_fields", None),
            **data_copy
        )

# -------------------- Usage Example --------------------
if __name__ == "__main__":
    # Fetch all RackGroups
    try:
        all_rack_groups = RackGroup.get()
        print(f"[Init] Loaded {len(all_rack_groups)} RackGroup objects.")
    except request.HTTPError as e:
        print(f"[Init] Error loading RackGroups: {e}")

    # Fetch all Racks
    try:
        all_racks = Rack.get()
        print(f"[Init] Loaded {len(all_racks)} Rack objects.")
    except requests.HTTPError as e:
        print(f"[Init] Error loading RackGroups: {e}")

    # Fetch all Devices
    try:
        all_devices = Device.get()
        print(f"[Init] Loaded {len(all_devices)} Device objects.")
    except requests.HTTPError as e:
        print("[Init] Error loading Devices: {e}")
