from client import GraphQL_Client

if __name__ == "__main__":
    endpoint = "http://0.0.0.0:8080/graphql"

    client = GraphQL_Client(endpoint)
    variables = {
        "input": {
            "deviceId": 12,
            "fleetId": 15,
            "organizationId": 13,
            "vehicleId": 14
        }
    }
    response = client.create_configuration(variables)

    variables = {
        "input": {
            "vehicleId": 14,
            "fleetId": 15,
            "organizationId": 13,
            "deviceId": 12
        }
    }
    response = client.get_configuration(variables)

    # variables = {
    #     "input": {
    #         "arbId": "12",
    #         "name": "message_ax",
    #         "networkId": "100",
    #         "ecuName": "ecu_12_ax",
    #         "ecuId": "14",
    #         "requestCode": "NONE",
    #         "uploadId": 98121
    #     }
    # }
    # response = client.create_message(variables)

    variables = {
        "input": {
            "configurationId": 4,
            "name": "signal_bx",
            "unit": "m/s",
            "paramType": "ENCODED",
            "messageId": 13,
            "signalType": "DID",
            "data": [
                {
                    "value": 1.9,
                    "time": "2023-09-25T00:00:00Z",
                    "stateId": 213,
                    "svalue": "1.9 m/s"
                },
                {
                    "value": 2.2,
                    "time": "2023-09-25T01:00:00Z",
                    "stateId": 413,
                    "svalue": "2.2 m/s"
                }
            ]
        }
    }
    response = client.upsert_signal_data(variables)