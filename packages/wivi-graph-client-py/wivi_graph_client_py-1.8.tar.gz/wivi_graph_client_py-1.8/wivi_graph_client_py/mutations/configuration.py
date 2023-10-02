class Configuration_Mutation:
    create_configuration_mutation = """
        mutation CreateConfiguration($input: CreateConfigurationInput) {
            createConfiguration(input: $input) {
                id
                deviceId
                fleetId
                organizationId
                vehicleId
            }
        }
    """