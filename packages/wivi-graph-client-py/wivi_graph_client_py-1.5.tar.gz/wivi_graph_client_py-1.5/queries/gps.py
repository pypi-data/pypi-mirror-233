class GPS_Query:
    get_gps_query = """
        query GetGPSData($input: GPSDataFilterArgs) {
            gpsData(input: $input) {
                vehicleId
                gpsData {
                    latitude
                    longitude
                    accuracy
                    altitude
                    time
                }
            }
        }
    """
