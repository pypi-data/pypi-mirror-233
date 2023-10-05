from dataclasses import dataclass


@dataclass
class AccessRequester:
    user_id: str
    tenant_id: str
