class Signals_Mutation:
    upsert_signal_data_mutation = """
        mutation UpsertSignalData($input: UpsertSignalDataArgs) {
            upsertSignalData(input: $input) {
                id
                name
                unit
                paramType
                configurationId
                messageId
                signalData {
                    value
                    signalType
                    time
                    signalId
                    stateId
                    svalue
                }
            }
        }
    """

    delete_signal_data_mutation = """
        mutation DeleteSignalData($input: DeleteSignalDataInput) {
            deleteSignalData(input: $input) {
               configurations
            }
        }
    """
