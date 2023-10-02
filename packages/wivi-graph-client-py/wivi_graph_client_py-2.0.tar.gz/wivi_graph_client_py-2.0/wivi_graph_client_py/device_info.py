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

class Device_Info_Mutation:
    create_device_info_mutation = '''
        mutation CreateDeviceInfo($input: CreateDeviceInfoInput) {
            createDeviceInfo(input: $input) {
                configurationId
            }
        }
    '''

    delete_device_info_mutation = '''
        mutation DeleteDeviceInfo($input: DeleteDeviceInfoInput) {
            deleteDeviceInfo(input: $input) {
                configurations
        }
    '''
