'''
# AWS::CodeArtifact Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS CodeArtifact is a fully managed artifact repository service that makes it easy for organizations of any size to securely store, publish, and share software packages used in their software development process. CodeArtifact can be configured to automatically fetch software packages and dependencies from public artifact repositories so developers have access to the latest versions. CodeArtifact works with commonly used package managers and build tools like Maven, Gradle, npm, yarn, twine, pip, and NuGet making it easy to integrate into existing development workflows.

For further information on AWS CodeArtifact, see the [AWS CodeArtifact documentation](https://docs.aws.amazon.com/codeartifact/).

Add a CodeArtifact Domain to your stack:

```python
import * as codeartifact from '@renovosolutions/cdk-library-aws-codeartifact';

new codeartifact.Domain(stack, 'domain', { name: 'example-domain' });
```

Add a CodeArtifact Repository to your stack:

```python
import * as codeartifact from '@renovosolutions/cdk-library-aws-codeartifact';

const domain = new codeartifact.Domain(stack, 'domain', { name: 'example-domain' });
const repository = new codeartifact.Repository(stack, 'repository', {
    name: 'repository',
    domain,
});
```

It is also possible to use the `addRepository` method on `codeartifact.Domain` to add a repository.

```python
import * as codeartifact from '@renovosolutions/cdk-library-aws-codeartifact';

const domain = new codeartifact.Domain(stack, 'domain', { name: 'example-domain' });

domain.addRepository('repo', {
  name: 'repository'
});
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_codeartifact as _aws_cdk_aws_codeartifact_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.DomainAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "domain_arn": "domainArn",
        "domain_encryption_key": "domainEncryptionKey",
        "domain_name": "domainName",
        "domain_owner": "domainOwner",
        "encryption_key": "encryptionKey",
    },
)
class DomainAttributes:
    def __init__(
        self,
        *,
        domain_arn: typing.Optional[builtins.str] = None,
        domain_encryption_key: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''Attributes of a domain.

        :param domain_arn: The ARN of the domain.
        :param domain_encryption_key: The key used to encrypt the domain.
        :param domain_name: The name of the domain.
        :param domain_owner: The account that owns the domain.
        :param encryption_key: The key used to encrypt the domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7b57e6f705057fbfd8ef15a9e407146526314b561907b70acd79342710acbb)
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
            check_type(argname="argument domain_encryption_key", value=domain_encryption_key, expected_type=type_hints["domain_encryption_key"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_owner", value=domain_owner, expected_type=type_hints["domain_owner"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_arn is not None:
            self._values["domain_arn"] = domain_arn
        if domain_encryption_key is not None:
            self._values["domain_encryption_key"] = domain_encryption_key
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_owner is not None:
            self._values["domain_owner"] = domain_owner
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def domain_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the domain.'''
        result = self._values.get("domain_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.'''
        result = self._values.get("domain_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain.'''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain.'''
        result = self._values.get("domain_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The key used to encrypt the domain.'''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.DomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "encryption_key": "encryptionKey",
        "permissions_policy_document": "permissionsPolicyDocument",
    },
)
class DomainProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ) -> None:
        '''The properties for a new domain.

        :param name: A string that specifies the name of the requested domain.
        :param encryption_key: The key used to encrypt the domain. Default: - An AWS managed key is created automatically.
        :param permissions_policy_document: The document that defines the resource policy that is set on a domain. Default: - No policy is set. The account will have full permissions to the domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f5f59315f919735f5fc10d9cd68873759bc3e62b1058a0d0ae3c5c14746263)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document

    @builtins.property
    def name(self) -> builtins.str:
        '''A string that specifies the name of the requested domain.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The key used to encrypt the domain.

        :default: - An AWS managed key is created automatically.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def permissions_policy_document(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''The document that defines the resource policy that is set on a domain.

        :default: - No policy is set. The account will have full permissions to the domain.
        '''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.ExternalConnection"
)
class ExternalConnection(enum.Enum):
    '''CodeArtifact supports an external connection to the following public repositories.

    :see: https://docs.aws.amazon.com/codeartifact/latest/ug/external-connection.html#supported-public-repositories
    '''

    NPM = "NPM"
    '''npm public registry.'''
    DOTNET_NUGETORG = "DOTNET_NUGETORG"
    '''NuGet Gallery.'''
    PYTHON_PYPI = "PYTHON_PYPI"
    '''Python Package Index.'''
    MAVEN_CENTRAL = "MAVEN_CENTRAL"
    '''Maven Central.'''
    MAVEN_GOOGLEANDROID = "MAVEN_GOOGLEANDROID"
    '''Google Android repository.'''
    MAVEN_GRADLEPLUGINS = "MAVEN_GRADLEPLUGINS"
    '''Gradle plugins repository.'''
    MAVEN_COMMONSWARE = "MAVEN_COMMONSWARE"
    '''CommonsWare Android repository.'''


@jsii.interface(jsii_type="@renovosolutions/cdk-library-aws-codeartifact.IDomain")
class IDomain(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''The ARN of the domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The name of the domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainEncryptionKey")
    def domain_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="domainOwner")
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The key used to encrypt the domain.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addRepository")
    def add_repository(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence["IRepository"]] = None,
    ) -> "IRepository":
        '''Add a repository to this domain.

        :param id: -
        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions to the given principal on this domain.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read and write permissions to the given principal on this domain.

        :param grantee: -
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant write permissions to the given principal on this domain.

        :param grantee: -
        '''
        ...


class _IDomainProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-aws-codeartifact.IDomain"

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''The ARN of the domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The name of the domain.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainEncryptionKey")
    def domain_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.

        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="domainOwner")
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain.

        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainOwner"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The key used to encrypt the domain.

        :attribute: true
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))

    @jsii.member(jsii_name="addRepository")
    def add_repository(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence["IRepository"]] = None,
    ) -> "IRepository":
        '''Add a repository to this domain.

        :param id: -
        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6226dcf957cec254ad7d5f3ce70d8f0157d23ee09202c35ff72f0965eaf72f1)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RepositoryOptions(
            name=name,
            description=description,
            external_connections=external_connections,
            permissions_policy_document=permissions_policy_document,
            upstreams=upstreams,
        )

        return typing.cast("IRepository", jsii.invoke(self, "addRepository", [id, props]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions to the given principal on this domain.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89c95160c98b7bc731a3dda48ff57dbf2a4329d256f9b934a485b6437ec969b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read and write permissions to the given principal on this domain.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de879289a2865d249eb73cc01451762177dd66b867f236474446ea51d7f1997)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant write permissions to the given principal on this domain.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8d56f47d7009e285cc3b15ed33e913a074a77d73c8a1b31b23f985ab5a1b9b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDomain).__jsii_proxy_class__ = lambda : _IDomainProxy


@jsii.interface(jsii_type="@renovosolutions/cdk-library-aws-codeartifact.IRepository")
class IRepository(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) This interface represents a CodeArtifact Repository resource.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> IDomain:
        '''(experimental) The domain that contains the repository.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''(experimental) The ARN of the repository.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainName")
    def repository_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain that contains the repository.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainOwner")
    def repository_domain_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The account that owns the domain that contains the repository.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given principal on this repository.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read and write permissions to the given principal on this repository.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant write permissions to the given principal on this respository.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IRepositoryProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) This interface represents a CodeArtifact Repository resource.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-aws-codeartifact.IRepository"

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> IDomain:
        '''(experimental) The domain that contains the repository.

        :stability: experimental
        '''
        return typing.cast(IDomain, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''(experimental) The ARN of the repository.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainName")
    def repository_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain that contains the repository.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainOwner")
    def repository_domain_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The account that owns the domain that contains the repository.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDomainOwner"))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the given principal on this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6bf87c5661665a87a5851d63f6c0d0394af0c9122c2ac57f19eca74a7d233e8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read and write permissions to the given principal on this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003f71e3f6082b72659f8ea8654e2d6ee77d481ba701f276b2028b8d54afd397)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant write permissions to the given principal on this respository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf5f6c6eccb0cf5ffcc9539980aa91cafbe60fd8d36f9bad41f265a6c69b709)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRepository).__jsii_proxy_class__ = lambda : _IRepositoryProxy


@jsii.implements(IRepository)
class Repository(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.Repository",
):
    '''A CodeArtifact domain.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: IDomain,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domain: The domain that the repository will be created in.
        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f015acc0ace33c60a540e2f16e5c20845354b4a8de4f3343d215e9a973541d19)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RepositoryProps(
            domain=domain,
            name=name,
            description=description,
            external_connections=external_connections,
            permissions_policy_document=permissions_policy_document,
            upstreams=upstreams,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRepositoryArn")
    @builtins.classmethod
    def from_repository_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        repository_arn: builtins.str,
    ) -> IRepository:
        '''Reference an existing repository by its ARN.

        :param scope: -
        :param id: -
        :param repository_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79c8dae6bd04395a2f6e939ca36997c9e2a4a4d202ab271ff0756672929044c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument repository_arn", value=repository_arn, expected_type=type_hints["repository_arn"])
        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn]))

    @jsii.member(jsii_name="fromRepositoryAttributes")
    @builtins.classmethod
    def from_repository_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain: typing.Optional[IDomain] = None,
        repository_arn: typing.Optional[builtins.str] = None,
        repository_domain_name: typing.Optional[builtins.str] = None,
        repository_domain_owner: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> IRepository:
        '''Reference an existing repository by its attributes.

        :param scope: -
        :param id: -
        :param domain: The domain that contains the repository.
        :param repository_arn: The ARN of the repository.
        :param repository_domain_name: The name of the domain that contains the repository.
        :param repository_domain_owner: The account that owns the domain that contains the repository.
        :param repository_name: The name of the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b408fb1098e7ef418d58ede91b2fc5c1dcdf0d049eab02c3bc0b8e87361a9962)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = RepositoryAttributes(
            domain=domain,
            repository_arn=repository_arn,
            repository_domain_name=repository_domain_name,
            repository_domain_owner=repository_domain_owner,
            repository_name=repository_name,
        )

        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions to the given principal on this repository.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de4d9c2e07bdc756d69a74981d621ed4e41afcca18e36fca52aa2553864bd45b)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [principal]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read and write permissions to the given principal on this repository.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959ed23373822b9e82766c664a44d63684951d2167d68c9944ea9f150a9c0a7f)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [principal]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant write permissions to the given principal on this respository.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0126135afc9aa676c8ecfbb468e0eb0a65d11740ca789610544a04b58f4959)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [principal]))

    @builtins.property
    @jsii.member(jsii_name="cfnRepository")
    def cfn_repository(self) -> _aws_cdk_aws_codeartifact_ceddda9d.CfnRepository:
        '''The underlying CfnRepository.'''
        return typing.cast(_aws_cdk_aws_codeartifact_ceddda9d.CfnRepository, jsii.get(self, "cfnRepository"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> IDomain:
        '''The name of the repository domain.'''
        return typing.cast(IDomain, jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''The ARN of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository.'''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainName")
    def repository_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain that contains the repository.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="repositoryDomainOwner")
    def repository_domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain that contains the repository.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDomainOwner"))

    @builtins.property
    @jsii.member(jsii_name="readActions")
    def read_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "readActions"))

    @read_actions.setter
    def read_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba4aea784c00fc59772d0209b485f5f92b18806ecc66e4208832dd74bc1bf7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readActions", value)

    @builtins.property
    @jsii.member(jsii_name="writeActions")
    def write_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "writeActions"))

    @write_actions.setter
    def write_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1044c8814fc0f1099137d98110e5a2943f8f6b31f3884c5387d505316f0eb5d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeActions", value)


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.RepositoryAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "repository_arn": "repositoryArn",
        "repository_domain_name": "repositoryDomainName",
        "repository_domain_owner": "repositoryDomainOwner",
        "repository_name": "repositoryName",
    },
)
class RepositoryAttributes:
    def __init__(
        self,
        *,
        domain: typing.Optional[IDomain] = None,
        repository_arn: typing.Optional[builtins.str] = None,
        repository_domain_name: typing.Optional[builtins.str] = None,
        repository_domain_owner: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Attributes of a repository.

        :param domain: The domain that contains the repository.
        :param repository_arn: The ARN of the repository.
        :param repository_domain_name: The name of the domain that contains the repository.
        :param repository_domain_owner: The account that owns the domain that contains the repository.
        :param repository_name: The name of the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__429930bd98ef3ebdbe0434af721380b04d5f00979c562425a4eb2b531a45fe74)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument repository_arn", value=repository_arn, expected_type=type_hints["repository_arn"])
            check_type(argname="argument repository_domain_name", value=repository_domain_name, expected_type=type_hints["repository_domain_name"])
            check_type(argname="argument repository_domain_owner", value=repository_domain_owner, expected_type=type_hints["repository_domain_owner"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if repository_arn is not None:
            self._values["repository_arn"] = repository_arn
        if repository_domain_name is not None:
            self._values["repository_domain_name"] = repository_domain_name
        if repository_domain_owner is not None:
            self._values["repository_domain_owner"] = repository_domain_owner
        if repository_name is not None:
            self._values["repository_name"] = repository_name

    @builtins.property
    def domain(self) -> typing.Optional[IDomain]:
        '''The domain that contains the repository.'''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[IDomain], result)

    @builtins.property
    def repository_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the repository.'''
        result = self._values.get("repository_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_domain_name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain that contains the repository.'''
        result = self._values.get("repository_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain that contains the repository.'''
        result = self._values.get("repository_domain_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''The name of the repository.'''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.RepositoryOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "external_connections": "externalConnections",
        "permissions_policy_document": "permissionsPolicyDocument",
        "upstreams": "upstreams",
    },
)
class RepositoryOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
    ) -> None:
        '''The options for creating a new repository.

        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a636f29448d960284f7603fa966ca17ad684748da6d01567a5a3d33191e41a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_connections", value=external_connections, expected_type=type_hints["external_connections"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument upstreams", value=upstreams, expected_type=type_hints["upstreams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if external_connections is not None:
            self._values["external_connections"] = external_connections
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if upstreams is not None:
            self._values["upstreams"] = upstreams

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the repository.

        :defualt: - No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_connections(self) -> typing.Optional[typing.List[ExternalConnection]]:
        '''An array of external connections associated with the repository.

        :see: https://docs.aws.amazon.com/codeartifact/latest/ug/external-connection.html
        '''
        result = self._values.get("external_connections")
        return typing.cast(typing.Optional[typing.List[ExternalConnection]], result)

    @builtins.property
    def permissions_policy_document(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''The document that defines the permissions policy for the repository.'''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    @builtins.property
    def upstreams(self) -> typing.Optional[typing.List[IRepository]]:
        '''An array of upstream repositories associated with the repository.

        :see: https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html
        '''
        result = self._values.get("upstreams")
        return typing.cast(typing.Optional[typing.List[IRepository]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.RepositoryProps",
    jsii_struct_bases=[RepositoryOptions],
    name_mapping={
        "name": "name",
        "description": "description",
        "external_connections": "externalConnections",
        "permissions_policy_document": "permissionsPolicyDocument",
        "upstreams": "upstreams",
        "domain": "domain",
    },
)
class RepositoryProps(RepositoryOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
        domain: IDomain,
    ) -> None:
        '''The properties of a CodeArtifact Repository.

        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        :param domain: The domain that the repository will be created in.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0c09a5f8de7dcf1971d406958c7ab381b0f1fcc28a0ae662f95354e97dda83)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_connections", value=external_connections, expected_type=type_hints["external_connections"])
            check_type(argname="argument permissions_policy_document", value=permissions_policy_document, expected_type=type_hints["permissions_policy_document"])
            check_type(argname="argument upstreams", value=upstreams, expected_type=type_hints["upstreams"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "domain": domain,
        }
        if description is not None:
            self._values["description"] = description
        if external_connections is not None:
            self._values["external_connections"] = external_connections
        if permissions_policy_document is not None:
            self._values["permissions_policy_document"] = permissions_policy_document
        if upstreams is not None:
            self._values["upstreams"] = upstreams

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the repository.

        :defualt: - No description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_connections(self) -> typing.Optional[typing.List[ExternalConnection]]:
        '''An array of external connections associated with the repository.

        :see: https://docs.aws.amazon.com/codeartifact/latest/ug/external-connection.html
        '''
        result = self._values.get("external_connections")
        return typing.cast(typing.Optional[typing.List[ExternalConnection]], result)

    @builtins.property
    def permissions_policy_document(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument]:
        '''The document that defines the permissions policy for the repository.'''
        result = self._values.get("permissions_policy_document")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument], result)

    @builtins.property
    def upstreams(self) -> typing.Optional[typing.List[IRepository]]:
        '''An array of upstream repositories associated with the repository.

        :see: https://docs.aws.amazon.com/codeartifact/latest/ug/repos-upstream.html
        '''
        result = self._values.get("upstreams")
        return typing.cast(typing.Optional[typing.List[IRepository]], result)

    @builtins.property
    def domain(self) -> IDomain:
        '''The domain that the repository will be created in.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(IDomain, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDomain)
class Domain(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-codeartifact.Domain",
):
    '''A CodeArtifact domain.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: A string that specifies the name of the requested domain.
        :param encryption_key: The key used to encrypt the domain. Default: - An AWS managed key is created automatically.
        :param permissions_policy_document: The document that defines the resource policy that is set on a domain. Default: - No policy is set. The account will have full permissions to the domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a1c70b6f21a271752333026d264664e6374a35bee4abfd96ff12323951846d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            name=name,
            encryption_key=encryption_key,
            permissions_policy_document=permissions_policy_document,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainArn")
    @builtins.classmethod
    def from_domain_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        domain_arn: builtins.str,
    ) -> IDomain:
        '''Reference an existing domain by its ARN.

        :param scope: -
        :param id: -
        :param domain_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa810b9d4c9e904304669494f6d0245d0a76ab4a5aa0b90870c6676b3a4597c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument domain_arn", value=domain_arn, expected_type=type_hints["domain_arn"])
        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainArn", [scope, id, domain_arn]))

    @jsii.member(jsii_name="fromDomainAttributes")
    @builtins.classmethod
    def from_domain_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domain_arn: typing.Optional[builtins.str] = None,
        domain_encryption_key: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_owner: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> IDomain:
        '''Import an existing domain given its attributes.

        Either ``domainArn`` or ``domainName`` is required.

        :param scope: -
        :param id: -
        :param domain_arn: The ARN of the domain.
        :param domain_encryption_key: The key used to encrypt the domain.
        :param domain_name: The name of the domain.
        :param domain_owner: The account that owns the domain.
        :param encryption_key: The key used to encrypt the domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b7e75fcf0d084ee238d1600931c3438b8dd4ae5132277422924eae292e84ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = DomainAttributes(
            domain_arn=domain_arn,
            domain_encryption_key=domain_encryption_key,
            domain_name=domain_name,
            domain_owner=domain_owner,
            encryption_key=encryption_key,
        )

        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addRepository")
    def add_repository(
        self,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
        permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
    ) -> IRepository:
        '''Add a repository to this domain.

        :param id: -
        :param name: The name of the repository.
        :param description: The description of the repository.
        :param external_connections: An array of external connections associated with the repository.
        :param permissions_policy_document: The document that defines the permissions policy for the repository.
        :param upstreams: An array of upstream repositories associated with the repository.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5f942e12ab722a3ce1fa710c6d9e66e6e4ef0510f4dec0c1db76960b2d79e4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RepositoryOptions(
            name=name,
            description=description,
            external_connections=external_connections,
            permissions_policy_document=permissions_policy_document,
            upstreams=upstreams,
        )

        return typing.cast(IRepository, jsii.invoke(self, "addRepository", [id, props]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read permissions to the given principal on this domain.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553b5ddd9d0ec028a375aae3b95504ab1ac2363bcf7afc10670a78f1ca2a9c57)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [principal]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant read and write permissions to the given principal on this domain.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efa8897a1ba8238b66eda397bad61dd40135edf60ae44ab58ebcca65d292590c)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [principal]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant write permissions to the given principal on this domain.

        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad34c7e084131668debf2ddee299de8badcc7208daced34cfd3d363ed536dd6)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [principal]))

    @builtins.property
    @jsii.member(jsii_name="cfnDomain")
    def cfn_domain(self) -> _aws_cdk_aws_codeartifact_ceddda9d.CfnDomain:
        '''The underlying CfnDomain resource.'''
        return typing.cast(_aws_cdk_aws_codeartifact_ceddda9d.CfnDomain, jsii.get(self, "cfnDomain"))

    @builtins.property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''The ARN of the domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The name of the domain.'''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainEncryptionKey")
    def domain_encryption_key(self) -> typing.Optional[builtins.str]:
        '''The key used to encrypt the domain.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="domainOwner")
    def domain_owner(self) -> typing.Optional[builtins.str]:
        '''The account that owns the domain.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainOwner"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The key used to encrypt the domain.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="readActions")
    def read_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "readActions"))

    @read_actions.setter
    def read_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9189566f87451a923f1d2a1ebb0751d18ed3f4a2902d760a0cabc30a20276a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readActions", value)

    @builtins.property
    @jsii.member(jsii_name="writeActions")
    def write_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "writeActions"))

    @write_actions.setter
    def write_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b249b2f7e018646b97193c782088bc09273f0980acf915d99148818eacc83989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeActions", value)


__all__ = [
    "Domain",
    "DomainAttributes",
    "DomainProps",
    "ExternalConnection",
    "IDomain",
    "IRepository",
    "Repository",
    "RepositoryAttributes",
    "RepositoryOptions",
    "RepositoryProps",
]

publication.publish()

def _typecheckingstub__ce7b57e6f705057fbfd8ef15a9e407146526314b561907b70acd79342710acbb(
    *,
    domain_arn: typing.Optional[builtins.str] = None,
    domain_encryption_key: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f5f59315f919735f5fc10d9cd68873759bc3e62b1058a0d0ae3c5c14746263(
    *,
    name: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6226dcf957cec254ad7d5f3ce70d8f0157d23ee09202c35ff72f0965eaf72f1(
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89c95160c98b7bc731a3dda48ff57dbf2a4329d256f9b934a485b6437ec969b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de879289a2865d249eb73cc01451762177dd66b867f236474446ea51d7f1997(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8d56f47d7009e285cc3b15ed33e913a074a77d73c8a1b31b23f985ab5a1b9b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6bf87c5661665a87a5851d63f6c0d0394af0c9122c2ac57f19eca74a7d233e8(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003f71e3f6082b72659f8ea8654e2d6ee77d481ba701f276b2028b8d54afd397(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf5f6c6eccb0cf5ffcc9539980aa91cafbe60fd8d36f9bad41f265a6c69b709(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f015acc0ace33c60a540e2f16e5c20845354b4a8de4f3343d215e9a973541d19(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: IDomain,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79c8dae6bd04395a2f6e939ca36997c9e2a4a4d202ab271ff0756672929044c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    repository_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b408fb1098e7ef418d58ede91b2fc5c1dcdf0d049eab02c3bc0b8e87361a9962(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain: typing.Optional[IDomain] = None,
    repository_arn: typing.Optional[builtins.str] = None,
    repository_domain_name: typing.Optional[builtins.str] = None,
    repository_domain_owner: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4d9c2e07bdc756d69a74981d621ed4e41afcca18e36fca52aa2553864bd45b(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959ed23373822b9e82766c664a44d63684951d2167d68c9944ea9f150a9c0a7f(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0126135afc9aa676c8ecfbb468e0eb0a65d11740ca789610544a04b58f4959(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba4aea784c00fc59772d0209b485f5f92b18806ecc66e4208832dd74bc1bf7d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1044c8814fc0f1099137d98110e5a2943f8f6b31f3884c5387d505316f0eb5d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429930bd98ef3ebdbe0434af721380b04d5f00979c562425a4eb2b531a45fe74(
    *,
    domain: typing.Optional[IDomain] = None,
    repository_arn: typing.Optional[builtins.str] = None,
    repository_domain_name: typing.Optional[builtins.str] = None,
    repository_domain_owner: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a636f29448d960284f7603fa966ca17ad684748da6d01567a5a3d33191e41a(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0c09a5f8de7dcf1971d406958c7ab381b0f1fcc28a0ae662f95354e97dda83(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
    domain: IDomain,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1c70b6f21a271752333026d264664e6374a35bee4abfd96ff12323951846d9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa810b9d4c9e904304669494f6d0245d0a76ab4a5aa0b90870c6676b3a4597c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    domain_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b7e75fcf0d084ee238d1600931c3438b8dd4ae5132277422924eae292e84ac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domain_arn: typing.Optional[builtins.str] = None,
    domain_encryption_key: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_owner: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5f942e12ab722a3ce1fa710c6d9e66e6e4ef0510f4dec0c1db76960b2d79e4(
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    external_connections: typing.Optional[typing.Sequence[ExternalConnection]] = None,
    permissions_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    upstreams: typing.Optional[typing.Sequence[IRepository]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553b5ddd9d0ec028a375aae3b95504ab1ac2363bcf7afc10670a78f1ca2a9c57(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efa8897a1ba8238b66eda397bad61dd40135edf60ae44ab58ebcca65d292590c(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad34c7e084131668debf2ddee299de8badcc7208daced34cfd3d363ed536dd6(
    principal: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9189566f87451a923f1d2a1ebb0751d18ed3f4a2902d760a0cabc30a20276a44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b249b2f7e018646b97193c782088bc09273f0980acf915d99148818eacc83989(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
