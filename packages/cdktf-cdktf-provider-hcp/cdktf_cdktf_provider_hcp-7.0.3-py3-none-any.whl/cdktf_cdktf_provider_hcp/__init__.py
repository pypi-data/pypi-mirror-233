'''
# Terraform CDK hcp Provider ~> 0.45

This repo builds and publishes the Terraform hcp Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-hcp](https://www.npmjs.com/package/@cdktf/provider-hcp).

`npm install @cdktf/provider-hcp`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-hcp](https://pypi.org/project/cdktf-cdktf-provider-hcp).

`pipenv install cdktf-cdktf-provider-hcp`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Hcp](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Hcp).

`dotnet add package HashiCorp.Cdktf.Providers.Hcp`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-hcp](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-hcp).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-hcp</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-hcp-go`](https://github.com/cdktf/cdktf-provider-hcp-go) package.

`go get github.com/cdktf/cdktf-provider-hcp-go/hcp`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-hcp).

## Versioning

This project is explicitly not tracking the Terraform hcp Provider version 1:1. In fact, it always tracks `latest` of `~> 0.45` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform hcp Provider](https://registry.terraform.io/providers/hashicorp/hcp/0.45.0)

  * This links to the minimum version being tracked, you can find the latest released version [in our releases](https://github.com/cdktf/cdktf-provider-hcp/releases)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
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

__all__ = [
    "aws_network_peering",
    "aws_transit_gateway_attachment",
    "azure_peering_connection",
    "boundary_cluster",
    "consul_cluster",
    "consul_cluster_root_token",
    "consul_snapshot",
    "data_hcp_aws_network_peering",
    "data_hcp_aws_transit_gateway_attachment",
    "data_hcp_azure_peering_connection",
    "data_hcp_boundary_cluster",
    "data_hcp_consul_agent_helm_config",
    "data_hcp_consul_agent_kubernetes_secret",
    "data_hcp_consul_cluster",
    "data_hcp_consul_versions",
    "data_hcp_hvn",
    "data_hcp_hvn_peering_connection",
    "data_hcp_hvn_route",
    "data_hcp_packer_bucket_names",
    "data_hcp_packer_image",
    "data_hcp_packer_iteration",
    "data_hcp_packer_run_task",
    "data_hcp_vault_cluster",
    "data_hcp_vault_plugin",
    "data_hcp_vault_secrets_app",
    "data_hcp_vault_secrets_secret",
    "hvn",
    "hvn_peering_connection",
    "hvn_route",
    "packer_channel",
    "packer_channel_assignment",
    "packer_run_task",
    "provider",
    "vault_cluster",
    "vault_cluster_admin_token",
    "vault_plugin",
    "vault_secrets_app",
    "vault_secrets_secret",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import aws_network_peering
from . import aws_transit_gateway_attachment
from . import azure_peering_connection
from . import boundary_cluster
from . import consul_cluster
from . import consul_cluster_root_token
from . import consul_snapshot
from . import data_hcp_aws_network_peering
from . import data_hcp_aws_transit_gateway_attachment
from . import data_hcp_azure_peering_connection
from . import data_hcp_boundary_cluster
from . import data_hcp_consul_agent_helm_config
from . import data_hcp_consul_agent_kubernetes_secret
from . import data_hcp_consul_cluster
from . import data_hcp_consul_versions
from . import data_hcp_hvn
from . import data_hcp_hvn_peering_connection
from . import data_hcp_hvn_route
from . import data_hcp_packer_bucket_names
from . import data_hcp_packer_image
from . import data_hcp_packer_iteration
from . import data_hcp_packer_run_task
from . import data_hcp_vault_cluster
from . import data_hcp_vault_plugin
from . import data_hcp_vault_secrets_app
from . import data_hcp_vault_secrets_secret
from . import hvn
from . import hvn_peering_connection
from . import hvn_route
from . import packer_channel
from . import packer_channel_assignment
from . import packer_run_task
from . import provider
from . import vault_cluster
from . import vault_cluster_admin_token
from . import vault_plugin
from . import vault_secrets_app
from . import vault_secrets_secret
