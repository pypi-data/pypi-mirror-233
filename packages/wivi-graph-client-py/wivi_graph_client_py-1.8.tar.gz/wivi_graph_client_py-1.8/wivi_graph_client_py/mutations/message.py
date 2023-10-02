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
