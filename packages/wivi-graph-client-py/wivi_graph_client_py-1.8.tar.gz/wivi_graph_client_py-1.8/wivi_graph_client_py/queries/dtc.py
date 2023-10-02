class Dtc_Query:
    get_dtc_query = """
        query GetDtcData($input: DtcDataFilterArgs) {
            dtcData(input: $input) {
                vehicleId
                dtcs {
                    code
                    status
                    message {
                        id
                        name
                    }
                    failure
                    time
                    count
                }
            }
        }
    """