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
