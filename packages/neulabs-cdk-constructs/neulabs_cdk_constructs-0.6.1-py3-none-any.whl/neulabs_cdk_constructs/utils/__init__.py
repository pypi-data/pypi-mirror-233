import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.utils.BaseTagProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_name": "repositoryName",
        "repository_version": "repositoryVersion",
        "team": "team",
    },
)
class BaseTagProps:
    def __init__(
        self,
        *,
        repository_name: typing.Optional[builtins.str] = None,
        repository_version: typing.Optional[builtins.str] = None,
        team: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository_name: 
        :param repository_version: 
        :param team: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59f73fdaf30660375badd7563a2c88d571a3f3c13954be279edbfc5e101a01f)
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument repository_version", value=repository_version, expected_type=type_hints["repository_version"])
            check_type(argname="argument team", value=team, expected_type=type_hints["team"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if repository_version is not None:
            self._values["repository_version"] = repository_version
        if team is not None:
            self._values["team"] = team

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("repository_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team(self) -> typing.Optional[builtins.str]:
        result = self._values.get("team")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseTagProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BaseTagProps",
]

publication.publish()

def _typecheckingstub__f59f73fdaf30660375badd7563a2c88d571a3f3c13954be279edbfc5e101a01f(
    *,
    repository_name: typing.Optional[builtins.str] = None,
    repository_version: typing.Optional[builtins.str] = None,
    team: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
