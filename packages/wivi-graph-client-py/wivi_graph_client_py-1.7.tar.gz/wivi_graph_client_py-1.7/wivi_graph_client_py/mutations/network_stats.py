class Network_Stats_Mutation:
    create_network_stats_mutation = """
        mutation CreateNetworkStats($input: CreateNetworkStatsInput) {
            createNetworkStats(input: $input) {
                id
                name
                vehicleId
                uploadId
                totalMessages
                matchedMessages
                unmatchedMessages
                errorMessages
                longMessageParts
                minTime
                maxTime
                rate
            }
        }
    """
