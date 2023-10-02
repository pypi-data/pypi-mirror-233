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

class GPS_Mutation:
    upsert_gps_mutation = """
        mutation UpsertGPSData($input: UpsertGpsDataInput) {
            upsertGpsData(input: $input) {
                configurations
            }
        }
    """

    delete_gps_mutation = '''
        mutation DeleteGPSData($input: DeleteGPSDataInput) {
            deleteGpsData(input: $input) {
               configurations
            }
        }
    '''
