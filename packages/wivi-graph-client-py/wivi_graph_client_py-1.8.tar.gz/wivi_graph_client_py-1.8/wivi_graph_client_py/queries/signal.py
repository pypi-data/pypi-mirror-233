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
