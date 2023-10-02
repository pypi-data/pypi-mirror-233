class Formula_Query:
    load_formula_query = """
        query LoadFormula($input: LoadFormulaArgs) {
            formula(input: $input) {
                id
                name
                source
                unit
                time
                formula
                fun
            }
        }
    """

    calculate_formula_query = '''
        query CalculateFormula($input: CalculateFormulaArgs) {
            calculateFormula(input: $input) {
                vehicleId
                data {
                    value
                    time
                }
            }
        }
    '''
