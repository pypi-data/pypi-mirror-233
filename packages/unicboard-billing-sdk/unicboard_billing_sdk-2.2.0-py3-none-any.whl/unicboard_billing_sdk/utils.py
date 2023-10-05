from typing import Dict, Any

from unicboard_billing_sdk.response_models import GetDeviceValueResponse, GetDeviceChannelValuePayloadResponse, \
    GetDeviceListInfoPayloadResponse, DataGatewayNetworkResponseModel, DeviceChannelResponseModel, NetworkResponseModel, \
    ProtokolResponseModel, DataGatewayResponseModel, DeviceManufacturerResponseModel, DeviceModificationResponseModel, \
    DeviceModificationTypeResponseModel, DeviceMeteringType, GetDeviceInfoResponse, GetDeviceListInfoResponse, \
    DeviceMeterResponseModel, GetDeviceBatteryLevelResponse, GetDeviceListBatteryLevelPayloadResponse, \
    GetDeviceListClockPayloadResponse, GetDeviceListEventPayloadResponse, GetDeviceListProfilePayloadResponse, \
    GetDeviceListTemperaturePayloadResponse, GetDeviceClockResponse, GetDeviceEventResponse, GetDeviceProfileResponse, \
    GetDeviceTemperatureResponse


def get_device_info_payload_structure(payload: Dict[str, Any]) -> GetDeviceListInfoPayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListInfoPayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListInfoPayloadResponse: Device information
    """
    data_gateway_network_device = payload.pop('data_gateway_network_device')
    network = data_gateway_network_device.pop('network')
    data_gateway = network.pop('data_gateway')
    protocol = data_gateway_network_device.pop('protocol')
    device_channels = payload.pop('device_channel')
    device_manufacturer = payload.pop('device_manufacturer')
    device_modification = payload.pop('device_modification')
    device_modification_type = device_modification.pop('device_modification_type')
    device_metering_type = device_modification_type.pop('device_metering_type')
    return GetDeviceListInfoPayloadResponse(
        date_produced=payload.get('date_produced', None),
        firmware_version=payload.get('firmware_version', None),
        hardware_version=payload.get('hardware_version', None),
        id=payload['id'],
        manufacturer_serial_number=payload['manufacturer_serial_number'],
        data_gateway_network_device=DataGatewayNetworkResponseModel(
            mac=data_gateway_network_device['mac'],
            network=NetworkResponseModel(
                name=network['name'],
                type_network=network['type_network'],
                data_gateway=DataGatewayResponseModel(
                    name=data_gateway['name'],
                ),
            ),
            protocol=ProtokolResponseModel(
                name=protocol['name'],
            ),
        ),
        device_channel=[DeviceChannelResponseModel(
            inactivity_limit=device_channel['inactivity_limit'],
            last_date_event_no_data=device_channel['last_date_event_no_data'],
            serial_number=device_channel['serial_number'],
            device_meters=[DeviceMeterResponseModel(
                last_value=device_meter.get('last_value', None),
                last_value_date=device_meter.get('last_value_date', None),
                unit_multiplier=device_meter['unit_multiplier'],
                value_multiplier=device_meter['value_multiplier'],
            ) for device_meter in device_channel['device_meter']],
        ) for device_channel in device_channels],
        device_manufacturer=DeviceManufacturerResponseModel(
            name=device_manufacturer['name'],
        ),
        device_modification=DeviceModificationResponseModel(
            name=device_modification['name'],
            device_modification_type=DeviceModificationTypeResponseModel(
                name_en=device_modification_type['name_en'],
                name_ru=device_modification_type['name_ru'],
                sys_name=device_modification_type['sys_name'],
                type=device_modification_type['type'],
                device_metering_type=DeviceMeteringType(
                    name_en=device_metering_type['name_en'],
                    name_ru=device_metering_type['name_ru'],
                    sys_name=device_metering_type['sys_name'],
                ),
            ),
        ),
    )


def get_device_value_payload_structure(payload: Dict[str, Any]) -> GetDeviceChannelValuePayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceChannelValuePayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceChannelValuePayloadResponse: Device value information
    """

    return GetDeviceChannelValuePayloadResponse(
            channel_number=payload['channel_number'],
            date=payload['date'],
            date_created=payload['date_created'],
            device_id=payload['device_id'],
            value=payload['value'],
            value_raw=payload.get('value_raw', None),
            value_type=payload['value_type'],
            kind=payload['kind'],
            tariff_number=payload['tariff_number'],
            journal_data_type=payload['journal_data_type'],
            meter_id=payload['meter_id'],
            last_value=payload.get('last_value', None),
            last_value_date=payload.get('last_value_date', None),
        )


def get_device_temperature_payload_structure(payload: Dict[str, Any]) -> GetDeviceListTemperaturePayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListTemperaturePayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListTemperaturePayloadResponse: Device value information
    """

    return GetDeviceListTemperaturePayloadResponse(
        device_id=payload['device_id'],
        date=payload['date'],
        value=payload.get('value', None),
    )


def get_device_profile_payload_structure(payload: Dict[str, Any]) -> GetDeviceListProfilePayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListProfilePayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListProfilePayloadResponse: Device value information
    """

    return GetDeviceListProfilePayloadResponse(
        device_id=payload['device_id'],
        date_start=payload['date_start'],
        date_end=payload['date_end'],
        profile_kind=payload['profile_kind'],
        granularity_s=payload['granularity_s'],
        values_count=payload['values_count'],
        values=payload['values'],
    )


def get_device_event_payload_structure(payload: Dict[str, Any]) -> GetDeviceListEventPayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListEventPayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListEventPayloadResponse: Device value information
    """

    return GetDeviceListEventPayloadResponse(
        device_id=payload['device_id'],
        type=payload['type'],
        date=payload['date'],
        value=payload.get('value', None),
        data=payload.get('data', None),
    )


def get_device_clock_payload_structure(payload: Dict[str, Any]) -> GetDeviceListClockPayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListClockPayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListClockPayloadResponse: Device value information
    """

    return GetDeviceListClockPayloadResponse(
        device_id=payload['device_id'],
        clock_id=payload['clock_id'],
        device_clock=payload['device_clock'],
        date=payload['date'],
        device_tz=payload['device_tz'],
        tz_offset_s=payload['tz_offset_s'],
        out_of_sync_s=payload['out_of_sync_s'],
        out_of_sync_type=payload['out_of_sync_type'],
    )


def get_device_battery_level_payload_structure(payload: Dict[str, Any]) -> GetDeviceListBatteryLevelPayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListBatteryLevelPayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListBatteryLevelPayloadResponse: Device value information
    """

    return GetDeviceListBatteryLevelPayloadResponse(
        device_id=payload['device_id'],
        battery_id=payload['battery_id'],
        date=payload['date'],
        value=payload.get('value', None),
    )


def get_device_info_structure(response: Dict[str, Any]) -> GetDeviceInfoResponse:
    """
    It takes a dictionary and returns a GetDeviceInfoResponse object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceInfoResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceInfoResponse(
        errors=response['errors'],
        ok=response['ok'],
        payload=get_device_info_payload_structure(payload)
    )


def get_device_battery_level_structure(response: Dict[str, Any]) -> GetDeviceBatteryLevelResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceBatteryLevelResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_battery_level_payload_structure(item) for item in payload]
    )


def get_device_clock_structure(response: Dict[str, Any]) -> GetDeviceClockResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceClockResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_clock_payload_structure(item) for item in payload]
    )


def get_device_event_structure(response: Dict[str, Any]) -> GetDeviceEventResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceEventResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_event_payload_structure(item) for item in payload]
    )


def get_device_profile_structure(response: Dict[str, Any]) -> GetDeviceProfileResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceProfileResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_profile_payload_structure(item) for item in payload]
    )


def get_device_temperature_structure(response: Dict[str, Any]) -> GetDeviceTemperatureResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceTemperatureResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_temperature_payload_structure(item) for item in payload]
    )


def get_device_list_info_structure(response: Dict[str, Any]) -> GetDeviceListInfoResponse:
    """
    It takes a dictionary and returns a GetDeviceListInfoResponse object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceListInfoResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceListInfoResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_info_payload_structure(item) for item in payload]
    )


def get_device_value_structure(response: Dict[str, Any]) -> GetDeviceValueResponse:
    """
    It takes a dictionary and returns a `GetDeviceValueResponse` object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceValueResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceValueResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_value_payload_structure(item) for item in payload]
    )


