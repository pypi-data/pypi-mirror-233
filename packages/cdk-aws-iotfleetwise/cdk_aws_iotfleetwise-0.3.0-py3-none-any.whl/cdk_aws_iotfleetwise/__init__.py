'''
[![NPM version](https://badge.fury.io/js/cdk-aws-iotfleetwise.svg)](https://badge.fury.io/js/cdk-aws-iotfleetwise)
[![PyPI version](https://badge.fury.io/py/cdk-aws-iotfleetwise.svg)](https://badge.fury.io/py/cdk-aws-iotfleetwise)
[![release](https://github.com/aws-samples/cdk-aws-iotfleetwise/actions/workflows/release.yml/badge.svg)](https://github.com/aws-samples/cdk-aws-iotfleetwise/actions/workflows/release.yml)

# cdk-aws-iotfleetwise

L2 CDK construct to provision AWS IoT Fleetwise

# Install

### Typescript

```sh
npm install cdk-aws-iotfleetwise
```

[API Reference](doc/api-typescript.md)

#### Python

```sh
pip install cdk-aws-iotfleetwise
```

[API Reference](doc/api-python.md)

# Sample

```python
import {
  SignalCatalog,
  VehicleModel,
  Vehicle,
  Campaign,
  CanVehicleInterface,
  CanVehicleSignal,
  SignalCatalogBranch,
  TimeBasedCollectionScheme,
} from 'cdk-aws-iotfleetwise';

const signalCatalog = new SignalCatalog(stack, 'SignalCatalog', {
  database: tsDatabaseConstruct,
  table: tsHeartBeatTableConstruct,
  nodes: [
    new SignalCatalogBranch({
      fullyQualifiedName: 'Vehicle',
    }),
    new SignalCatalogSensor({
      fullyQualifiedName: 'Vehicle.EngineTorque',
      dataType: 'DOUBLE',
    }),
  ],
});

const model_a = new VehicleModel(stack, 'ModelA', {
  signalCatalog,
  name: 'modelA',
  description: 'Model A vehicle',
  networkInterfaces: [
    new CanVehicleInterface({
      interfaceId: '1',
      name: 'vcan0',
    }),
  ],
  signals: [
    new CanVehicleSignal({
      fullyQualifiedName: 'Vehicle.EngineTorque',
      interfaceId: '1',
      messageId: 401,
      factor: 1.0,
      isBigEndian: true,
      isSigned: false,
      length: 8,
      offset: 0.0,
      startBit: 0,
    }),
  ],
});

const vin100 = new Vehicle(stack, 'vin100', {
  vehicleName: 'vin100',
  vehicleModel: model_a,
  createIotThing: true,
});

new Campaign(stack, 'Campaign', {
  name: 'TimeBasedCampaign',
  target: vin100,
  collectionScheme: new TimeBasedCollectionScheme(cdk.Duration.seconds(10)),
  signals: [new CampaignSignal('Vehicle.EngineTorque')],
});
```

## Getting started

To deploy a simple end-to-end example you can use the following commands

```sh
yarn install
projen && projen compile
# Define Amazon Timestream as fleetwise storage destination
npx cdk -a lib/integ.full.js deploy -c key_name=mykey
# Define Amazon S3 as fleetwise storage destination
npx cdk -a lib/integ.full.js deploy -c key_name=mykey -c use_s3=true
```

Where `mykey` is an existing keypair name present in your account.
The deploy takes about 15 mins mostly due to compilation of the IoT FleetWise agent in the
EC2 instance that simulate the vehicle. Once deploy is finshed, data will start to show up in your Timestream table.

## TODO

Warning: this construct should be considered at alpha stage and is not feature complete.

* Implement updates for all the custom resources
* Conditional campaigns

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more
information.

## License

This code is licensed under the MIT-0 License. See the LICENSE file.
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
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.AttributeVehicleSignalProps",
    jsii_struct_bases=[],
    name_mapping={"fully_qualified_name": "fullyQualifiedName"},
)
class AttributeVehicleSignalProps:
    def __init__(self, *, fully_qualified_name: builtins.str) -> None:
        '''Attribute Signal - needed when creating a vehicle with attributes.

        :param fully_qualified_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269cf8afd158afc9424e66958229160bebdbd3fdc0c9ec2880c4ba6ff3af2754)
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fully_qualified_name": fully_qualified_name,
        }

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AttributeVehicleSignalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Campaign(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Campaign",
):
    '''export class Campaign extends Construct { readonly name: string = '';

    readonly arn: string = '';
    readonly target: Vehicle = ({} as Vehicle);

    constructor(scope: Construct, id: string, props: CampaignProps) {
    super(scope, id);

    (this.name as string) = props.name;
    this.arn = ``arn:aws:iotfleetwise:${cdk.Aws.REGION}:${cdk.Aws.ACCOUNT_ID}:vehicle/${props.target}``;
    (this.target as Vehicle) = props.target;

    const handler = new Handler(this, 'Handler', {
    handler: 'campaignhandler.on_event',
    });

    const resource = new cdk.CustomResource(this, 'Resource', {
    serviceToken: Provider.getOrCreate(this, handler).provider.serviceToken,
    properties: {
    name: this.name,
    signal_catalog_arn: this.target.vehicleModel.signalCatalog.arn,
    data_destination_configs: JSON.stringify(props.dataDestinationConfigs.map(s => s.toObject())),
    target_arn: this.target.arn,
    collection_scheme: JSON.stringify(props.collectionScheme.toObject()),
    signals_to_collect: JSON.stringify(props.signals.map(s => s.toObject())),
    auto_approve: props.autoApprove || false,
    },
    });
    resource.node.addDependency(this.target);
    }
    }
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        campaign_s3arn: builtins.str,
        collection_scheme: "CollectionScheme",
        fw_timestream_role: builtins.str,
        name: builtins.str,
        signals: typing.Sequence["CampaignSignal"],
        target: "Vehicle",
        timestream_arn: builtins.str,
        auto_approve: typing.Optional[builtins.bool] = None,
        use_s3: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param campaign_s3arn: 
        :param collection_scheme: 
        :param fw_timestream_role: 
        :param name: 
        :param signals: 
        :param target: 
        :param timestream_arn: 
        :param auto_approve: 
        :param use_s3: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a25462d60fb15d2ea409daddf7579264c21c71256d7e5097a8818840df754d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CampaignProps(
            campaign_s3arn=campaign_s3arn,
            collection_scheme=collection_scheme,
            fw_timestream_role=fw_timestream_role,
            name=name,
            signals=signals,
            target=target,
            timestream_arn=timestream_arn,
            auto_approve=auto_approve,
            use_s3=use_s3,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Vehicle":
        return typing.cast("Vehicle", jsii.get(self, "target"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.CampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "campaign_s3arn": "campaignS3arn",
        "collection_scheme": "collectionScheme",
        "fw_timestream_role": "fwTimestreamRole",
        "name": "name",
        "signals": "signals",
        "target": "target",
        "timestream_arn": "timestreamArn",
        "auto_approve": "autoApprove",
        "use_s3": "useS3",
    },
)
class CampaignProps:
    def __init__(
        self,
        *,
        campaign_s3arn: builtins.str,
        collection_scheme: "CollectionScheme",
        fw_timestream_role: builtins.str,
        name: builtins.str,
        signals: typing.Sequence["CampaignSignal"],
        target: "Vehicle",
        timestream_arn: builtins.str,
        auto_approve: typing.Optional[builtins.bool] = None,
        use_s3: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param campaign_s3arn: 
        :param collection_scheme: 
        :param fw_timestream_role: 
        :param name: 
        :param signals: 
        :param target: 
        :param timestream_arn: 
        :param auto_approve: 
        :param use_s3: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a213d12d4f0017d8131228977cf0298662f687e10faedcf43f07ed71f9f22b36)
            check_type(argname="argument campaign_s3arn", value=campaign_s3arn, expected_type=type_hints["campaign_s3arn"])
            check_type(argname="argument collection_scheme", value=collection_scheme, expected_type=type_hints["collection_scheme"])
            check_type(argname="argument fw_timestream_role", value=fw_timestream_role, expected_type=type_hints["fw_timestream_role"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument signals", value=signals, expected_type=type_hints["signals"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument timestream_arn", value=timestream_arn, expected_type=type_hints["timestream_arn"])
            check_type(argname="argument auto_approve", value=auto_approve, expected_type=type_hints["auto_approve"])
            check_type(argname="argument use_s3", value=use_s3, expected_type=type_hints["use_s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "campaign_s3arn": campaign_s3arn,
            "collection_scheme": collection_scheme,
            "fw_timestream_role": fw_timestream_role,
            "name": name,
            "signals": signals,
            "target": target,
            "timestream_arn": timestream_arn,
        }
        if auto_approve is not None:
            self._values["auto_approve"] = auto_approve
        if use_s3 is not None:
            self._values["use_s3"] = use_s3

    @builtins.property
    def campaign_s3arn(self) -> builtins.str:
        result = self._values.get("campaign_s3arn")
        assert result is not None, "Required property 'campaign_s3arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_scheme(self) -> "CollectionScheme":
        result = self._values.get("collection_scheme")
        assert result is not None, "Required property 'collection_scheme' is missing"
        return typing.cast("CollectionScheme", result)

    @builtins.property
    def fw_timestream_role(self) -> builtins.str:
        result = self._values.get("fw_timestream_role")
        assert result is not None, "Required property 'fw_timestream_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signals(self) -> typing.List["CampaignSignal"]:
        result = self._values.get("signals")
        assert result is not None, "Required property 'signals' is missing"
        return typing.cast(typing.List["CampaignSignal"], result)

    @builtins.property
    def target(self) -> "Vehicle":
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("Vehicle", result)

    @builtins.property
    def timestream_arn(self) -> builtins.str:
        result = self._values.get("timestream_arn")
        assert result is not None, "Required property 'timestream_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_approve(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_approve")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_s3(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("use_s3")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CampaignSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CampaignSignal",
):
    def __init__(
        self,
        name: builtins.str,
        max_sample_count: typing.Optional[jsii.Number] = None,
        minimum_sampling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param name: -
        :param max_sample_count: -
        :param minimum_sampling_interval: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc8f60e5caf188657a2be99493d6c6cca2e07ce9a7a18a134da9ae36b96b8ee)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument max_sample_count", value=max_sample_count, expected_type=type_hints["max_sample_count"])
            check_type(argname="argument minimum_sampling_interval", value=minimum_sampling_interval, expected_type=type_hints["minimum_sampling_interval"])
        jsii.create(self.__class__, self, [name, max_sample_count, minimum_sampling_interval])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.CanVehicleInterfaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "interface_id": "interfaceId",
        "name": "name",
        "protocol_name": "protocolName",
        "protocol_version": "protocolVersion",
    },
)
class CanVehicleInterfaceProps:
    def __init__(
        self,
        *,
        interface_id: builtins.str,
        name: builtins.str,
        protocol_name: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interface_id: 
        :param name: 
        :param protocol_name: 
        :param protocol_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476577cef92a8fa770b9597accf9e1ad6477f591ce694f7e174f08b738fccee6)
            check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol_name", value=protocol_name, expected_type=type_hints["protocol_name"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_id": interface_id,
            "name": name,
        }
        if protocol_name is not None:
            self._values["protocol_name"] = protocol_name
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version

    @builtins.property
    def interface_id(self) -> builtins.str:
        result = self._values.get("interface_id")
        assert result is not None, "Required property 'interface_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("protocol_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanVehicleInterfaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.CanVehicleSignalProps",
    jsii_struct_bases=[],
    name_mapping={
        "factor": "factor",
        "fully_qualified_name": "fullyQualifiedName",
        "interface_id": "interfaceId",
        "is_big_endian": "isBigEndian",
        "is_signed": "isSigned",
        "length": "length",
        "message_id": "messageId",
        "offset": "offset",
        "start_bit": "startBit",
        "name": "name",
    },
)
class CanVehicleSignalProps:
    def __init__(
        self,
        *,
        factor: jsii.Number,
        fully_qualified_name: builtins.str,
        interface_id: builtins.str,
        is_big_endian: builtins.bool,
        is_signed: builtins.bool,
        length: jsii.Number,
        message_id: jsii.Number,
        offset: jsii.Number,
        start_bit: jsii.Number,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param factor: 
        :param fully_qualified_name: 
        :param interface_id: 
        :param is_big_endian: 
        :param is_signed: 
        :param length: 
        :param message_id: 
        :param offset: 
        :param start_bit: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83539059a704ff8bc42ab147130cf7bfdca4648e4ddfeeb24056b3218b2f25e6)
            check_type(argname="argument factor", value=factor, expected_type=type_hints["factor"])
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument interface_id", value=interface_id, expected_type=type_hints["interface_id"])
            check_type(argname="argument is_big_endian", value=is_big_endian, expected_type=type_hints["is_big_endian"])
            check_type(argname="argument is_signed", value=is_signed, expected_type=type_hints["is_signed"])
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument start_bit", value=start_bit, expected_type=type_hints["start_bit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "factor": factor,
            "fully_qualified_name": fully_qualified_name,
            "interface_id": interface_id,
            "is_big_endian": is_big_endian,
            "is_signed": is_signed,
            "length": length,
            "message_id": message_id,
            "offset": offset,
            "start_bit": start_bit,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def factor(self) -> jsii.Number:
        result = self._values.get("factor")
        assert result is not None, "Required property 'factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interface_id(self) -> builtins.str:
        result = self._values.get("interface_id")
        assert result is not None, "Required property 'interface_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_big_endian(self) -> builtins.bool:
        result = self._values.get("is_big_endian")
        assert result is not None, "Required property 'is_big_endian' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_signed(self) -> builtins.bool:
        result = self._values.get("is_signed")
        assert result is not None, "Required property 'is_signed' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def length(self) -> jsii.Number:
        result = self._values.get("length")
        assert result is not None, "Required property 'length' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def message_id(self) -> jsii.Number:
        result = self._values.get("message_id")
        assert result is not None, "Required property 'message_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def offset(self) -> jsii.Number:
        result = self._values.get("offset")
        assert result is not None, "Required property 'offset' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_bit(self) -> jsii.Number:
        result = self._values.get("start_bit")
        assert result is not None, "Required property 'start_bit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanVehicleSignalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CollectionScheme(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CollectionScheme",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def _scheme(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "scheme"))

    @_scheme.setter
    def _scheme(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62c607c503ea1f069076192828254db6442bc977ac1021fd615ae37bcefbaa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value)


class Fleet(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Fleet",
):
    '''The fleet of vehicles.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        fleet_id: builtins.str,
        signal_catalog: "SignalCatalog",
        description: typing.Optional[builtins.str] = None,
        vehicles: typing.Optional[typing.Sequence["Vehicle"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param fleet_id: 
        :param signal_catalog: 
        :param description: 
        :param vehicles: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a942dc531b4428a9bae4f62d79425d027063799bb2c04c6246ffce8d3d67099)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FleetProps(
            fleet_id=fleet_id,
            signal_catalog=signal_catalog,
            description=description,
            vehicles=vehicles,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="fleetId")
    def fleet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetId"))

    @builtins.property
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> "SignalCatalog":
        return typing.cast("SignalCatalog", jsii.get(self, "signalCatalog"))

    @builtins.property
    @jsii.member(jsii_name="vehicles")
    def vehicles(self) -> typing.Optional[typing.List["Vehicle"]]:
        return typing.cast(typing.Optional[typing.List["Vehicle"]], jsii.get(self, "vehicles"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.FleetProps",
    jsii_struct_bases=[],
    name_mapping={
        "fleet_id": "fleetId",
        "signal_catalog": "signalCatalog",
        "description": "description",
        "vehicles": "vehicles",
    },
)
class FleetProps:
    def __init__(
        self,
        *,
        fleet_id: builtins.str,
        signal_catalog: "SignalCatalog",
        description: typing.Optional[builtins.str] = None,
        vehicles: typing.Optional[typing.Sequence["Vehicle"]] = None,
    ) -> None:
        '''Interface.

        :param fleet_id: 
        :param signal_catalog: 
        :param description: 
        :param vehicles: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e5ee4932a72282d0ddd688f14f3920d9b916b8bdcb6e08d8a47c67b5f3bb80)
            check_type(argname="argument fleet_id", value=fleet_id, expected_type=type_hints["fleet_id"])
            check_type(argname="argument signal_catalog", value=signal_catalog, expected_type=type_hints["signal_catalog"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument vehicles", value=vehicles, expected_type=type_hints["vehicles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fleet_id": fleet_id,
            "signal_catalog": signal_catalog,
        }
        if description is not None:
            self._values["description"] = description
        if vehicles is not None:
            self._values["vehicles"] = vehicles

    @builtins.property
    def fleet_id(self) -> builtins.str:
        result = self._values.get("fleet_id")
        assert result is not None, "Required property 'fleet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signal_catalog(self) -> "SignalCatalog":
        result = self._values.get("signal_catalog")
        assert result is not None, "Required property 'signal_catalog' is missing"
        return typing.cast("SignalCatalog", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vehicles(self) -> typing.Optional[typing.List["Vehicle"]]:
        result = self._values.get("vehicles")
        return typing.cast(typing.Optional[typing.List["Vehicle"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Logging(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Logging",
):
    '''Configures FleetWise logging to CloudWatch logs.

    If enabled, this will ensure the log group is accessible,
    or create a new one if it is not.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        enable_logging: builtins.str,
        log_group_name: builtins.str,
        keep_log_group: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param enable_logging: 
        :param log_group_name: Name of log group to configure. This can be either single name such as ``AWSIoTFleetWiseLogs`` or a fully pathed entry such as: ``/iot/FleetWiseLogs``
        :param keep_log_group: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb677f859fffb46727a72afd2bc25ca9d39bd0c6f2a5fc1867741f792db9ea2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LoggingProps(
            enable_logging=enable_logging,
            log_group_name=log_group_name,
            keep_log_group=keep_log_group,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.LoggingProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_logging": "enableLogging",
        "log_group_name": "logGroupName",
        "keep_log_group": "keepLogGroup",
    },
)
class LoggingProps:
    def __init__(
        self,
        *,
        enable_logging: builtins.str,
        log_group_name: builtins.str,
        keep_log_group: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''FleetWise Logging Properties.

        :param enable_logging: 
        :param log_group_name: Name of log group to configure. This can be either single name such as ``AWSIoTFleetWiseLogs`` or a fully pathed entry such as: ``/iot/FleetWiseLogs``
        :param keep_log_group: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c608d0ebf721a940ef1739636fd3712fb5e4e16c021bf87c058d93fd289017a)
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument keep_log_group", value=keep_log_group, expected_type=type_hints["keep_log_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_logging": enable_logging,
            "log_group_name": log_group_name,
        }
        if keep_log_group is not None:
            self._values["keep_log_group"] = keep_log_group

    @builtins.property
    def enable_logging(self) -> builtins.str:
        result = self._values.get("enable_logging")
        assert result is not None, "Required property 'enable_logging' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Name of log group to configure.

        This can be either single name
        such as ``AWSIoTFleetWiseLogs`` or a fully pathed entry such as:
        ``/iot/FleetWiseLogs``
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_log_group(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("keep_log_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkFileDefinition(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.NetworkFileDefinition",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def _definition(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "definition"))

    @_definition.setter
    def _definition(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aff3fc7963ae067809a85a81a89d183e26d9987949bacbc88ea80a52c4a3058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)


class SignalCatalog(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalog",
):
    '''The Signal Catalog represents the list of all signals that you want to collect from all the vehicles.

    The AWS IoT Fleetwise preview can only support a single Signal Catalog per account.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        deregister: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Sequence["SignalCatalogNode"]] = None,
        vss_file: typing.Optional[builtins.str] = None,
        vss_generate_prefix_branch: typing.Optional[builtins.bool] = None,
        vss_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param deregister: Deregister FleetWise on stack deletion. If set to 'true', FleetWise will be deregistered from the Timestream destination. Default: - false
        :param description: Description of the Signal Catalog. If not provided no description is set. Default: - None
        :param name: Name of the Signal Catalog. If not provided, default value is used. Default: - default
        :param nodes: An array of signal nodes. Nodes are a general abstraction of a signal. A node can be specified as an actuator, attribute, branch, or sensor. See ``SignalCatalogBranch``, ``SignalCatalogSensor``, ``SignalCatalogActuator``, or ``SignalCatalogAttribute`` for creating nodes. Default: - []
        :param vss_file: A YAML file that conforms to the `Vehicle Signal Specification format <https://covesa.github.io/vehicle_signal_specification/>`_ and contains a list of signals. If provided, the contents of the file, along with the ``prefix`` property will be appended after any ``SignalCatalogNode`` objects provided. Default: - None
        :param vss_generate_prefix_branch: If set to true, this will parse the vssPrefix into branch nodes. For instance if ``OBD.MyData`` was provided, the ``OBD.MyData`` will be parsed into branch nodes of ``OBD`` and ``OBD.MyData``. By default this is set to true. If you define branches in another way such as via ``SignalCatalogNode``, set this to false to suppress creation of branch nodes. Default: - true
        :param vss_prefix: A prefix to prepend to the fully qualified names found in the VSS file. The format of the prefix is in dotted notation, and will be the prepended to all signal names. For instance, with the prefix of ``OBD.MyData`` and signal names of ``PidA`` and ``PidB`` will be combined to create ``OBD.MyData.PidA`` and ``OBD.MyData.PidB``. Default: - None
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22558683b7f3a3144e5c43c42cacdbb2432fc40b9a2310c13f631b3e9aa6cf16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SignalCatalogProps(
            deregister=deregister,
            description=description,
            name=name,
            nodes=nodes,
            vss_file=vss_file,
            vss_generate_prefix_branch=vss_generate_prefix_branch,
            vss_prefix=vss_prefix,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the signal catalog.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogActuatorProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "fully_qualified_name": "fullyQualifiedName",
        "allowed_values": "allowedValues",
        "assigned_value": "assignedValue",
        "description": "description",
        "max": "max",
        "min": "min",
        "unit": "unit",
    },
)
class SignalCatalogActuatorProps:
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        assigned_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param assigned_value: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb028a7a836965238438d5a3620a73f1af8f83ec2b256b44ee2b382b768c3ac8)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_type": data_type,
            "fully_qualified_name": fully_qualified_name,
        }
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if assigned_value is not None:
            self._values["assigned_value"] = assigned_value
        if description is not None:
            self._values["description"] = description
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def data_type(self) -> builtins.str:
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assigned_value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("assigned_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogActuatorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogAttributeProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "fully_qualified_name": "fullyQualifiedName",
        "allowed_values": "allowedValues",
        "assigned_value": "assignedValue",
        "default_value": "defaultValue",
        "description": "description",
        "max": "max",
        "min": "min",
        "unit": "unit",
    },
)
class SignalCatalogAttributeProps:
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        assigned_value: typing.Optional[builtins.str] = None,
        default_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param assigned_value: 
        :param default_value: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90edaf1ba3cd065b632cac7dd5edcd86489576eeb4ee306719bade061f9934e)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument assigned_value", value=assigned_value, expected_type=type_hints["assigned_value"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_type": data_type,
            "fully_qualified_name": fully_qualified_name,
        }
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if assigned_value is not None:
            self._values["assigned_value"] = assigned_value
        if default_value is not None:
            self._values["default_value"] = default_value
        if description is not None:
            self._values["description"] = description
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def data_type(self) -> builtins.str:
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def assigned_value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("assigned_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogAttributeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogBranchProps",
    jsii_struct_bases=[],
    name_mapping={
        "fully_qualified_name": "fullyQualifiedName",
        "description": "description",
    },
)
class SignalCatalogBranchProps:
    def __init__(
        self,
        *,
        fully_qualified_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fully_qualified_name: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0532a336fb5f4e2c7e7419e977aa0d9333aa5163b0675bdff31cb2863435b371)
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fully_qualified_name": fully_qualified_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogBranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SignalCatalogNode(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogNode",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="node")
    def _node(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "node"))

    @_node.setter
    def _node(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c708ca33b3bf1801961c48bc7a9146b5dc1857e835e5dfa9382cb8d7d8ddb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "node", value)


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "deregister": "deregister",
        "description": "description",
        "name": "name",
        "nodes": "nodes",
        "vss_file": "vssFile",
        "vss_generate_prefix_branch": "vssGeneratePrefixBranch",
        "vss_prefix": "vssPrefix",
    },
)
class SignalCatalogProps:
    def __init__(
        self,
        *,
        deregister: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Sequence[SignalCatalogNode]] = None,
        vss_file: typing.Optional[builtins.str] = None,
        vss_generate_prefix_branch: typing.Optional[builtins.bool] = None,
        vss_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deregister: Deregister FleetWise on stack deletion. If set to 'true', FleetWise will be deregistered from the Timestream destination. Default: - false
        :param description: Description of the Signal Catalog. If not provided no description is set. Default: - None
        :param name: Name of the Signal Catalog. If not provided, default value is used. Default: - default
        :param nodes: An array of signal nodes. Nodes are a general abstraction of a signal. A node can be specified as an actuator, attribute, branch, or sensor. See ``SignalCatalogBranch``, ``SignalCatalogSensor``, ``SignalCatalogActuator``, or ``SignalCatalogAttribute`` for creating nodes. Default: - []
        :param vss_file: A YAML file that conforms to the `Vehicle Signal Specification format <https://covesa.github.io/vehicle_signal_specification/>`_ and contains a list of signals. If provided, the contents of the file, along with the ``prefix`` property will be appended after any ``SignalCatalogNode`` objects provided. Default: - None
        :param vss_generate_prefix_branch: If set to true, this will parse the vssPrefix into branch nodes. For instance if ``OBD.MyData`` was provided, the ``OBD.MyData`` will be parsed into branch nodes of ``OBD`` and ``OBD.MyData``. By default this is set to true. If you define branches in another way such as via ``SignalCatalogNode``, set this to false to suppress creation of branch nodes. Default: - true
        :param vss_prefix: A prefix to prepend to the fully qualified names found in the VSS file. The format of the prefix is in dotted notation, and will be the prepended to all signal names. For instance, with the prefix of ``OBD.MyData`` and signal names of ``PidA`` and ``PidB`` will be combined to create ``OBD.MyData.PidA`` and ``OBD.MyData.PidB``. Default: - None

        :summary: The properties for the SignalCatalog construct.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b3e4a975371f170886dc9fc98615bdb72232529cf0bbc8b1f35caae1cff47d)
            check_type(argname="argument deregister", value=deregister, expected_type=type_hints["deregister"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
            check_type(argname="argument vss_file", value=vss_file, expected_type=type_hints["vss_file"])
            check_type(argname="argument vss_generate_prefix_branch", value=vss_generate_prefix_branch, expected_type=type_hints["vss_generate_prefix_branch"])
            check_type(argname="argument vss_prefix", value=vss_prefix, expected_type=type_hints["vss_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deregister is not None:
            self._values["deregister"] = deregister
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if nodes is not None:
            self._values["nodes"] = nodes
        if vss_file is not None:
            self._values["vss_file"] = vss_file
        if vss_generate_prefix_branch is not None:
            self._values["vss_generate_prefix_branch"] = vss_generate_prefix_branch
        if vss_prefix is not None:
            self._values["vss_prefix"] = vss_prefix

    @builtins.property
    def deregister(self) -> typing.Optional[builtins.bool]:
        '''Deregister FleetWise on stack deletion.

        If set to 'true',  FleetWise will be deregistered from the Timestream
        destination.

        :default: - false
        '''
        result = self._values.get("deregister")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of the Signal Catalog.

        If not provided no description is set.

        :default: - None
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the Signal Catalog.

        If not provided, default value is used.

        :default: - default
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List[SignalCatalogNode]]:
        '''An array of signal nodes.

        Nodes are a general abstraction of a signal.
        A node can be specified as an actuator, attribute, branch, or sensor. See ``SignalCatalogBranch``,
        ``SignalCatalogSensor``, ``SignalCatalogActuator``, or ``SignalCatalogAttribute`` for creating nodes.

        :default: - []
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List[SignalCatalogNode]], result)

    @builtins.property
    def vss_file(self) -> typing.Optional[builtins.str]:
        '''A YAML file that conforms to the `Vehicle Signal Specification format <https://covesa.github.io/vehicle_signal_specification/>`_ and contains a list of signals. If provided, the contents of the file, along with the ``prefix`` property will be appended after any ``SignalCatalogNode`` objects provided.

        :default: - None
        '''
        result = self._values.get("vss_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vss_generate_prefix_branch(self) -> typing.Optional[builtins.bool]:
        '''If set to true, this will parse the vssPrefix into branch nodes.

        For instance if ``OBD.MyData`` was
        provided,  the ``OBD.MyData`` will be parsed into branch nodes of ``OBD`` and ``OBD.MyData``. By default
        this is set to true. If you define branches in another way such as via ``SignalCatalogNode``, set this
        to false to suppress creation of branch nodes.

        :default: - true
        '''
        result = self._values.get("vss_generate_prefix_branch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vss_prefix(self) -> typing.Optional[builtins.str]:
        '''A prefix to prepend to the fully qualified names found in the VSS file.

        The format of the prefix
        is in dotted notation, and will be the prepended to all signal names.

        For instance, with the prefix of ``OBD.MyData`` and signal names of ``PidA`` and ``PidB`` will be combined
        to create ``OBD.MyData.PidA`` and ``OBD.MyData.PidB``.

        :default: - None
        '''
        result = self._values.get("vss_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SignalCatalogSensor(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogSensor",
):
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        props = SignalCatalogSensorProps(
            data_type=data_type,
            fully_qualified_name=fully_qualified_name,
            allowed_values=allowed_values,
            description=description,
            max=max,
            min=min,
            unit=unit,
        )

        jsii.create(self.__class__, self, [props])


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogSensorProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_type": "dataType",
        "fully_qualified_name": "fullyQualifiedName",
        "allowed_values": "allowedValues",
        "description": "description",
        "max": "max",
        "min": "min",
        "unit": "unit",
    },
)
class SignalCatalogSensorProps:
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b02888c5f12fc619c5cff71b5edb8dd0a7d726db66b1f046db9c46acee2dc4)
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument fully_qualified_name", value=fully_qualified_name, expected_type=type_hints["fully_qualified_name"])
            check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
            check_type(argname="argument min", value=min, expected_type=type_hints["min"])
            check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_type": data_type,
            "fully_qualified_name": fully_qualified_name,
        }
        if allowed_values is not None:
            self._values["allowed_values"] = allowed_values
        if description is not None:
            self._values["description"] = description
        if max is not None:
            self._values["max"] = max
        if min is not None:
            self._values["min"] = min
        if unit is not None:
            self._values["unit"] = unit

    @builtins.property
    def data_type(self) -> builtins.str:
        result = self._values.get("data_type")
        assert result is not None, "Required property 'data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fully_qualified_name(self) -> builtins.str:
        result = self._values.get("fully_qualified_name")
        assert result is not None, "Required property 'fully_qualified_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_values(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("allowed_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("unit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SignalCatalogSensorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TimeBasedCollectionScheme(
    CollectionScheme,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.TimeBasedCollectionScheme",
):
    def __init__(self, period: _aws_cdk_ceddda9d.Duration) -> None:
        '''
        :param period: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c554a7540ac15920c809981922b55ac6bb20a50dfff2666ef4a5fd626e1532b)
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        jsii.create(self.__class__, self, [period])


class Vehicle(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.Vehicle",
):
    '''The vehicle of a specific type from which IoT FleetWise collect signals.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        create_iot_thing: builtins.bool,
        vehicle_model: "VehicleModel",
        vehicle_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param create_iot_thing: 
        :param vehicle_model: 
        :param vehicle_name: 
        :param attributes: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa7363b99b06a663f4dcad569dad44c9d5514a10b26092496e3786ad9762abd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VehicleProps(
            create_iot_thing=create_iot_thing,
            vehicle_model=vehicle_model,
            vehicle_name=vehicle_name,
            attributes=attributes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="vehicleModel")
    def vehicle_model(self) -> "VehicleModel":
        return typing.cast("VehicleModel", jsii.get(self, "vehicleModel"))

    @builtins.property
    @jsii.member(jsii_name="vehicleName")
    def vehicle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vehicleName"))

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArn"))

    @builtins.property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateId"))

    @builtins.property
    @jsii.member(jsii_name="certificatePem")
    def certificate_pem(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificatePem"))

    @builtins.property
    @jsii.member(jsii_name="endpointAddress")
    def endpoint_address(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointAddress"))

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))


class VehicleInterface(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleInterface",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="intf")
    def _intf(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "intf"))

    @_intf.setter
    def _intf(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eaa38dea094fa1020859cd423a82076186450ac31f13aabc7c7d5fc3aa61c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intf", value)


class VehicleModel(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleModel",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        network_interfaces: typing.Sequence[VehicleInterface],
        signal_catalog: SignalCatalog,
        description: typing.Optional[builtins.str] = None,
        network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
        signals: typing.Optional[typing.Sequence["VehicleSignal"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: 
        :param network_interfaces: 
        :param signal_catalog: 
        :param description: 
        :param network_file_definitions: 
        :param signals: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f826871f94a3224f8096bdece761d09b92cc2232872843ae436564e616652485)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VehicleModelProps(
            name=name,
            network_interfaces=network_interfaces,
            signal_catalog=signal_catalog,
            description=description,
            network_file_definitions=network_file_definitions,
            signals=signals,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="signalCatalog")
    def signal_catalog(self) -> SignalCatalog:
        return typing.cast(SignalCatalog, jsii.get(self, "signalCatalog"))


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.VehicleModelProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "network_interfaces": "networkInterfaces",
        "signal_catalog": "signalCatalog",
        "description": "description",
        "network_file_definitions": "networkFileDefinitions",
        "signals": "signals",
    },
)
class VehicleModelProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        network_interfaces: typing.Sequence[VehicleInterface],
        signal_catalog: SignalCatalog,
        description: typing.Optional[builtins.str] = None,
        network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
        signals: typing.Optional[typing.Sequence["VehicleSignal"]] = None,
    ) -> None:
        '''
        :param name: 
        :param network_interfaces: 
        :param signal_catalog: 
        :param description: 
        :param network_file_definitions: 
        :param signals: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb2914835ea9b2973cef66a80e9c1bde35f01ef5004639fa7ca95ee74ecce02)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument signal_catalog", value=signal_catalog, expected_type=type_hints["signal_catalog"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument network_file_definitions", value=network_file_definitions, expected_type=type_hints["network_file_definitions"])
            check_type(argname="argument signals", value=signals, expected_type=type_hints["signals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_interfaces": network_interfaces,
            "signal_catalog": signal_catalog,
        }
        if description is not None:
            self._values["description"] = description
        if network_file_definitions is not None:
            self._values["network_file_definitions"] = network_file_definitions
        if signals is not None:
            self._values["signals"] = signals

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_interfaces(self) -> typing.List[VehicleInterface]:
        result = self._values.get("network_interfaces")
        assert result is not None, "Required property 'network_interfaces' is missing"
        return typing.cast(typing.List[VehicleInterface], result)

    @builtins.property
    def signal_catalog(self) -> SignalCatalog:
        result = self._values.get("signal_catalog")
        assert result is not None, "Required property 'signal_catalog' is missing"
        return typing.cast(SignalCatalog, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_file_definitions(
        self,
    ) -> typing.Optional[typing.List[NetworkFileDefinition]]:
        result = self._values.get("network_file_definitions")
        return typing.cast(typing.Optional[typing.List[NetworkFileDefinition]], result)

    @builtins.property
    def signals(self) -> typing.Optional[typing.List["VehicleSignal"]]:
        result = self._values.get("signals")
        return typing.cast(typing.Optional[typing.List["VehicleSignal"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VehicleModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-aws-iotfleetwise.VehicleProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_iot_thing": "createIotThing",
        "vehicle_model": "vehicleModel",
        "vehicle_name": "vehicleName",
        "attributes": "attributes",
    },
)
class VehicleProps:
    def __init__(
        self,
        *,
        create_iot_thing: builtins.bool,
        vehicle_model: VehicleModel,
        vehicle_name: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Interface.

        :param create_iot_thing: 
        :param vehicle_model: 
        :param vehicle_name: 
        :param attributes: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb62247adb507be5e977ad2ca77257552c72649e1e686d3532508566128370dd)
            check_type(argname="argument create_iot_thing", value=create_iot_thing, expected_type=type_hints["create_iot_thing"])
            check_type(argname="argument vehicle_model", value=vehicle_model, expected_type=type_hints["vehicle_model"])
            check_type(argname="argument vehicle_name", value=vehicle_name, expected_type=type_hints["vehicle_name"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "create_iot_thing": create_iot_thing,
            "vehicle_model": vehicle_model,
            "vehicle_name": vehicle_name,
        }
        if attributes is not None:
            self._values["attributes"] = attributes

    @builtins.property
    def create_iot_thing(self) -> builtins.bool:
        result = self._values.get("create_iot_thing")
        assert result is not None, "Required property 'create_iot_thing' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def vehicle_model(self) -> VehicleModel:
        result = self._values.get("vehicle_model")
        assert result is not None, "Required property 'vehicle_model' is missing"
        return typing.cast(VehicleModel, result)

    @builtins.property
    def vehicle_name(self) -> builtins.str:
        result = self._values.get("vehicle_name")
        assert result is not None, "Required property 'vehicle_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VehicleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VehicleSignal(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.VehicleSignal",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.invoke(self, "toObject", []))

    @builtins.property
    @jsii.member(jsii_name="signal")
    def _signal(self) -> typing.Mapping[typing.Any, typing.Any]:
        return typing.cast(typing.Mapping[typing.Any, typing.Any], jsii.get(self, "signal"))

    @_signal.setter
    def _signal(self, value: typing.Mapping[typing.Any, typing.Any]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e389e87bc32dd1cfa06c188de326653918b48780b61349eea19b70d635f950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "signal", value)


class AttributeVehicleSignal(
    VehicleSignal,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.AttributeVehicleSignal",
):
    def __init__(self, *, fully_qualified_name: builtins.str) -> None:
        '''
        :param fully_qualified_name: 
        '''
        props = AttributeVehicleSignalProps(fully_qualified_name=fully_qualified_name)

        jsii.create(self.__class__, self, [props])


class CanDefinition(
    NetworkFileDefinition,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanDefinition",
):
    def __init__(
        self,
        network_interface: builtins.str,
        signals_map: typing.Mapping[builtins.str, builtins.str],
        can_dbc_files: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param network_interface: -
        :param signals_map: -
        :param can_dbc_files: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285909d515a9b553b7ee69ea1d231aed69b41197f5c8d3fa563032b5222fb9bc)
            check_type(argname="argument network_interface", value=network_interface, expected_type=type_hints["network_interface"])
            check_type(argname="argument signals_map", value=signals_map, expected_type=type_hints["signals_map"])
            check_type(argname="argument can_dbc_files", value=can_dbc_files, expected_type=type_hints["can_dbc_files"])
        jsii.create(self.__class__, self, [network_interface, signals_map, can_dbc_files])


class CanVehicleInterface(
    VehicleInterface,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleInterface",
):
    def __init__(
        self,
        *,
        interface_id: builtins.str,
        name: builtins.str,
        protocol_name: typing.Optional[builtins.str] = None,
        protocol_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interface_id: 
        :param name: 
        :param protocol_name: 
        :param protocol_version: 
        '''
        props = CanVehicleInterfaceProps(
            interface_id=interface_id,
            name=name,
            protocol_name=protocol_name,
            protocol_version=protocol_version,
        )

        jsii.create(self.__class__, self, [props])


class CanVehicleSignal(
    VehicleSignal,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.CanVehicleSignal",
):
    def __init__(
        self,
        *,
        factor: jsii.Number,
        fully_qualified_name: builtins.str,
        interface_id: builtins.str,
        is_big_endian: builtins.bool,
        is_signed: builtins.bool,
        length: jsii.Number,
        message_id: jsii.Number,
        offset: jsii.Number,
        start_bit: jsii.Number,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param factor: 
        :param fully_qualified_name: 
        :param interface_id: 
        :param is_big_endian: 
        :param is_signed: 
        :param length: 
        :param message_id: 
        :param offset: 
        :param start_bit: 
        :param name: 
        '''
        props = CanVehicleSignalProps(
            factor=factor,
            fully_qualified_name=fully_qualified_name,
            interface_id=interface_id,
            is_big_endian=is_big_endian,
            is_signed=is_signed,
            length=length,
            message_id=message_id,
            offset=offset,
            start_bit=start_bit,
            name=name,
        )

        jsii.create(self.__class__, self, [props])


class SignalCatalogActuator(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogActuator",
):
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        assigned_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param assigned_value: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        props = SignalCatalogActuatorProps(
            data_type=data_type,
            fully_qualified_name=fully_qualified_name,
            allowed_values=allowed_values,
            assigned_value=assigned_value,
            description=description,
            max=max,
            min=min,
            unit=unit,
        )

        jsii.create(self.__class__, self, [props])


class SignalCatalogAttribute(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogAttribute",
):
    def __init__(
        self,
        *,
        data_type: builtins.str,
        fully_qualified_name: builtins.str,
        allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        assigned_value: typing.Optional[builtins.str] = None,
        default_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        max: typing.Optional[jsii.Number] = None,
        min: typing.Optional[jsii.Number] = None,
        unit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_type: 
        :param fully_qualified_name: 
        :param allowed_values: 
        :param assigned_value: 
        :param default_value: 
        :param description: 
        :param max: 
        :param min: 
        :param unit: 
        '''
        props = SignalCatalogAttributeProps(
            data_type=data_type,
            fully_qualified_name=fully_qualified_name,
            allowed_values=allowed_values,
            assigned_value=assigned_value,
            default_value=default_value,
            description=description,
            max=max,
            min=min,
            unit=unit,
        )

        jsii.create(self.__class__, self, [props])


class SignalCatalogBranch(
    SignalCatalogNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-aws-iotfleetwise.SignalCatalogBranch",
):
    def __init__(
        self,
        *,
        fully_qualified_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fully_qualified_name: 
        :param description: 
        '''
        props = SignalCatalogBranchProps(
            fully_qualified_name=fully_qualified_name, description=description
        )

        jsii.create(self.__class__, self, [props])


__all__ = [
    "AttributeVehicleSignal",
    "AttributeVehicleSignalProps",
    "Campaign",
    "CampaignProps",
    "CampaignSignal",
    "CanDefinition",
    "CanVehicleInterface",
    "CanVehicleInterfaceProps",
    "CanVehicleSignal",
    "CanVehicleSignalProps",
    "CollectionScheme",
    "Fleet",
    "FleetProps",
    "Logging",
    "LoggingProps",
    "NetworkFileDefinition",
    "SignalCatalog",
    "SignalCatalogActuator",
    "SignalCatalogActuatorProps",
    "SignalCatalogAttribute",
    "SignalCatalogAttributeProps",
    "SignalCatalogBranch",
    "SignalCatalogBranchProps",
    "SignalCatalogNode",
    "SignalCatalogProps",
    "SignalCatalogSensor",
    "SignalCatalogSensorProps",
    "TimeBasedCollectionScheme",
    "Vehicle",
    "VehicleInterface",
    "VehicleModel",
    "VehicleModelProps",
    "VehicleProps",
    "VehicleSignal",
]

publication.publish()

def _typecheckingstub__269cf8afd158afc9424e66958229160bebdbd3fdc0c9ec2880c4ba6ff3af2754(
    *,
    fully_qualified_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a25462d60fb15d2ea409daddf7579264c21c71256d7e5097a8818840df754d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    campaign_s3arn: builtins.str,
    collection_scheme: CollectionScheme,
    fw_timestream_role: builtins.str,
    name: builtins.str,
    signals: typing.Sequence[CampaignSignal],
    target: Vehicle,
    timestream_arn: builtins.str,
    auto_approve: typing.Optional[builtins.bool] = None,
    use_s3: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a213d12d4f0017d8131228977cf0298662f687e10faedcf43f07ed71f9f22b36(
    *,
    campaign_s3arn: builtins.str,
    collection_scheme: CollectionScheme,
    fw_timestream_role: builtins.str,
    name: builtins.str,
    signals: typing.Sequence[CampaignSignal],
    target: Vehicle,
    timestream_arn: builtins.str,
    auto_approve: typing.Optional[builtins.bool] = None,
    use_s3: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc8f60e5caf188657a2be99493d6c6cca2e07ce9a7a18a134da9ae36b96b8ee(
    name: builtins.str,
    max_sample_count: typing.Optional[jsii.Number] = None,
    minimum_sampling_interval: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476577cef92a8fa770b9597accf9e1ad6477f591ce694f7e174f08b738fccee6(
    *,
    interface_id: builtins.str,
    name: builtins.str,
    protocol_name: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83539059a704ff8bc42ab147130cf7bfdca4648e4ddfeeb24056b3218b2f25e6(
    *,
    factor: jsii.Number,
    fully_qualified_name: builtins.str,
    interface_id: builtins.str,
    is_big_endian: builtins.bool,
    is_signed: builtins.bool,
    length: jsii.Number,
    message_id: jsii.Number,
    offset: jsii.Number,
    start_bit: jsii.Number,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62c607c503ea1f069076192828254db6442bc977ac1021fd615ae37bcefbaa7(
    value: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a942dc531b4428a9bae4f62d79425d027063799bb2c04c6246ffce8d3d67099(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    fleet_id: builtins.str,
    signal_catalog: SignalCatalog,
    description: typing.Optional[builtins.str] = None,
    vehicles: typing.Optional[typing.Sequence[Vehicle]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e5ee4932a72282d0ddd688f14f3920d9b916b8bdcb6e08d8a47c67b5f3bb80(
    *,
    fleet_id: builtins.str,
    signal_catalog: SignalCatalog,
    description: typing.Optional[builtins.str] = None,
    vehicles: typing.Optional[typing.Sequence[Vehicle]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb677f859fffb46727a72afd2bc25ca9d39bd0c6f2a5fc1867741f792db9ea2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    enable_logging: builtins.str,
    log_group_name: builtins.str,
    keep_log_group: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c608d0ebf721a940ef1739636fd3712fb5e4e16c021bf87c058d93fd289017a(
    *,
    enable_logging: builtins.str,
    log_group_name: builtins.str,
    keep_log_group: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aff3fc7963ae067809a85a81a89d183e26d9987949bacbc88ea80a52c4a3058(
    value: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22558683b7f3a3144e5c43c42cacdbb2432fc40b9a2310c13f631b3e9aa6cf16(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    deregister: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[typing.Sequence[SignalCatalogNode]] = None,
    vss_file: typing.Optional[builtins.str] = None,
    vss_generate_prefix_branch: typing.Optional[builtins.bool] = None,
    vss_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb028a7a836965238438d5a3620a73f1af8f83ec2b256b44ee2b382b768c3ac8(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90edaf1ba3cd065b632cac7dd5edcd86489576eeb4ee306719bade061f9934e(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    assigned_value: typing.Optional[builtins.str] = None,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0532a336fb5f4e2c7e7419e977aa0d9333aa5163b0675bdff31cb2863435b371(
    *,
    fully_qualified_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c708ca33b3bf1801961c48bc7a9146b5dc1857e835e5dfa9382cb8d7d8ddb0(
    value: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b3e4a975371f170886dc9fc98615bdb72232529cf0bbc8b1f35caae1cff47d(
    *,
    deregister: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    nodes: typing.Optional[typing.Sequence[SignalCatalogNode]] = None,
    vss_file: typing.Optional[builtins.str] = None,
    vss_generate_prefix_branch: typing.Optional[builtins.bool] = None,
    vss_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b02888c5f12fc619c5cff71b5edb8dd0a7d726db66b1f046db9c46acee2dc4(
    *,
    data_type: builtins.str,
    fully_qualified_name: builtins.str,
    allowed_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    max: typing.Optional[jsii.Number] = None,
    min: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c554a7540ac15920c809981922b55ac6bb20a50dfff2666ef4a5fd626e1532b(
    period: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa7363b99b06a663f4dcad569dad44c9d5514a10b26092496e3786ad9762abd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    create_iot_thing: builtins.bool,
    vehicle_model: VehicleModel,
    vehicle_name: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaa38dea094fa1020859cd423a82076186450ac31f13aabc7c7d5fc3aa61c9f(
    value: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f826871f94a3224f8096bdece761d09b92cc2232872843ae436564e616652485(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    network_interfaces: typing.Sequence[VehicleInterface],
    signal_catalog: SignalCatalog,
    description: typing.Optional[builtins.str] = None,
    network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
    signals: typing.Optional[typing.Sequence[VehicleSignal]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb2914835ea9b2973cef66a80e9c1bde35f01ef5004639fa7ca95ee74ecce02(
    *,
    name: builtins.str,
    network_interfaces: typing.Sequence[VehicleInterface],
    signal_catalog: SignalCatalog,
    description: typing.Optional[builtins.str] = None,
    network_file_definitions: typing.Optional[typing.Sequence[NetworkFileDefinition]] = None,
    signals: typing.Optional[typing.Sequence[VehicleSignal]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb62247adb507be5e977ad2ca77257552c72649e1e686d3532508566128370dd(
    *,
    create_iot_thing: builtins.bool,
    vehicle_model: VehicleModel,
    vehicle_name: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e389e87bc32dd1cfa06c188de326653918b48780b61349eea19b70d635f950(
    value: typing.Mapping[typing.Any, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285909d515a9b553b7ee69ea1d231aed69b41197f5c8d3fa563032b5222fb9bc(
    network_interface: builtins.str,
    signals_map: typing.Mapping[builtins.str, builtins.str],
    can_dbc_files: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
