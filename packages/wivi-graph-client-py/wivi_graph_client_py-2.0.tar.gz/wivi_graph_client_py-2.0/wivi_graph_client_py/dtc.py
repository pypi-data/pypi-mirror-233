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

class Dtc_Mutation:
    upsert_dtc_mutation = """
        mutation UpsertDtcData($input: UpsertDtcDataInput) {
            upsertDtcData(input: $input) {
                configurationId
                messageId
            }
        }
    """

    delete_dtc_mutation = """
        mutation DeleteDtcData($input: DeleteDtcDataInput) {
            deleteDtcData(input: $input) {
                configurations
            }
        }
    """
