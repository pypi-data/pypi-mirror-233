import sys
import typing as t

from pydantic import Field

from sqlmesh.integrations.github.cicd.config import GithubCICDBotConfig

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

CICDBotConfig = Annotated[
    t.Union[
        GithubCICDBotConfig,
    ],
    Field(discriminator="type_"),
]
