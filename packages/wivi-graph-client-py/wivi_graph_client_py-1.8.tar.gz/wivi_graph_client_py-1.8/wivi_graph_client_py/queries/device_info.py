class Device_Info_Query:
    get_device_info_query = """
        query GetDeviceInfo($input: DeviceInfoFilterInput) {
            deviceInfo(input: $input) {
                vehicleId
                deviceInfoData {
                    name
                    data {
                        time
                        svalue
                        value
                    }
                }
            }
        }
    """
