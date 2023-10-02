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