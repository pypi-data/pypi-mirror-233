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

class Message_Mutation:
    create_message_mutation = """
        mutation CreateNewMessage($input: CreateMessageInput) {
            createMessage(input: $input) {
                id
                arbId
                name
                networkId
                ecuId
                uploadId
            }
        }
    """
