class Message_Query:
    get_message_query = """
        query GetMessages($input: MessageFilterArgs) {
            message(input: $input) {
                id
                arbId
                name
                networkId
                ecuId
                uploadId
            }
        }
    """
