class Signals_Query:
    get_signals_query = """
        query GetSignals($input: SignalFilterArgs) {
            signal(input: $input) {
                id
                name
                unit
                paramType
                configurationId
                messageId
            }
        }
    """

    get_signals_data_query = """
        query GetSignalData($input: SignalDataFilterArgs) {
            signalData(input: $input) {
                vehicleId
                data {
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

