class Version_Query:
    get_version_query = """
        query GetVersions($input: VersionInfoFilter) {
            versionInfo(input: $input) {
                vehicleId
                versionInfo {
                    name
                    time
                    value
                }
            }
        }
    """
