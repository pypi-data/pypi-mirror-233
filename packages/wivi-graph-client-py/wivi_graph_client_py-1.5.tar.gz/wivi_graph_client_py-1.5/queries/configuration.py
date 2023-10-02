class Configuration_Query:
    get_configuration_query = """
        query GetConfigurations($input: ConfigurationFilterInput) {
            configuration(input: $input) {
                id
                deviceId
                fleetId
                organizationId
                vehicleId
                signals {
                    name
                }
                ecus {
                    name
                }
                messages {
                    name
                }
                network {
                    name
                }
            }
        }
    """
