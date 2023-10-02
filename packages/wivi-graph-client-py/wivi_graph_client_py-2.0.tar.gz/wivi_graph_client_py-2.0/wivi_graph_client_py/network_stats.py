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
