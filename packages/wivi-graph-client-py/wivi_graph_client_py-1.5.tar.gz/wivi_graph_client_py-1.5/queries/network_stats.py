class Network_Stats_Query:
    get_network_stats_query = """
        query GetNetworkStats($input: NetworkStatsFilter) {
            networkStats(input: $input) {
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
