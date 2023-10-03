from .entity import uSwidEntity as uSwidEntity
from .enums import uSwidVersionScheme as uSwidVersionScheme
from .errors import NotSupportedError as NotSupportedError
from .link import uSwidLink as uSwidLink
from .payload import uSwidPayload as uSwidPayload
from _typeshed import Incomplete
from typing import List, Optional

class uSwidIdentity:
    tag_id: Incomplete
    tag_version: Incomplete
    software_version: Incomplete
    version_scheme: Incomplete
    summary: Incomplete
    product: Incomplete
    colloquial_version: Incomplete
    revision: Incomplete
    edition: Incomplete
    persistent_id: Incomplete
    lang: str
    generator: str
    payloads: Incomplete
    def __init__(self, tag_id: Optional[str] = ..., tag_version: int = ..., software_name: Optional[str] = ..., software_version: Optional[str] = ...) -> None: ...
    @property
    def software_name(self) -> Optional[str]: ...
    def merge(self, identity_new: uSwidIdentity) -> None: ...
    def add_entity(self, entity: uSwidEntity) -> None: ...
    def add_link(self, link: uSwidLink) -> None: ...
    def add_payload(self, payload: uSwidPayload) -> None: ...
    @property
    def links(self) -> List[uSwidLink]: ...
    @property
    def entities(self) -> List[uSwidEntity]: ...
