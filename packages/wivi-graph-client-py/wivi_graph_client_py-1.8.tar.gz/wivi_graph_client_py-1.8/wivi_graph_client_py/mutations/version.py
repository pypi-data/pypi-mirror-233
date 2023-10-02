class Version_Mutation:
    upsert_version_mutation = '''
        mutation UpsertVersion($input: UpsertVersionInfoInput) {
            upsertVersionInfo(input: $input) {
                configurationId
            }
        }
    '''

    delete_version_mutation = '''
        mutation DeleteVersion($input: DeleteVersionInfoInput) {
            deleteVersionInfo(input: $input) {
                configurations
            }
        }
    '''