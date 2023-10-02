import requests
from graphql import parse, print_ast
from mutations.configuration import Configuration_Mutation
from queries.configuration import Configuration_Query
from mutations.device_info import Device_Info_Mutation
from queries.device_info import Device_Info_Query
from queries.dtc import Dtc_Query
from mutations.dtc import Dtc_Mutation
from queries.ecu import Ecu_Query
from mutations.formula import Formula_Mutation
from queries.formula import Formula_Query
from mutations.gps import GPS_Mutation
from queries.gps import GPS_Query
from mutations.message import Message_Mutation
from queries.message import Message_Query
from mutations.network_stats import Network_Stats_Mutation
from queries.network_stats import Network_Stats_Query
from queries.network import Network_Query
from queries.signal import Signals_Query
from mutations.signal import Signals_Mutation
from mutations.version import Version_Mutation
from queries.version import Version_Query


class GraphQL_Client:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def execute(self, query, variables=None):
        request_data = {"query": print_ast(parse(query)), "variables": variables}
        response = requests.post(self.endpoint, json=request_data)
        response = response.json()
        if "errors" in response:
            print("GraphQL request had errors:", response["errors"])
            return {
                "data": None,
                "errors": response["errors"]
            }
        else:
            data = response["data"]
            print("Data", data)
            return {
                "data": data
            }

    # Configuration Functions:
    def create_configuration(self, variables=None):
        mutation = Configuration_Mutation.create_configuration_mutation
        return self.execute(mutation, variables)

    def get_configuration(self, variables=None):
        query = Configuration_Query.get_configuration_query
        return self.execute(query, variables)

    # Device Info Functions:
    def create_device_info(self, variables=None):
        mutation = Device_Info_Mutation.create_device_info_mutation
        return self.execute(mutation, variables)

    def delete_device_info(self, variables=None):
        mutation = Device_Info_Mutation.delete_device_info_mutation
        return self.execute(mutation, variables)

    def get_device_info(self, variables=None):
        query = Device_Info_Query.get_device_info_query
        return self.execute(query, variables)

    # DTC Functions:
    def create_dtc(self, variables=None):
        mutation = Dtc_Mutation.upsert_dtc_mutation
        return self.execute(mutation, variables)

    def delete_dtc(self, variables=None):
        mutation = Dtc_Mutation.delete_dtc_mutation
        return self.execute(mutation, variables)

    def get_dtc(self, variables=None):
        query = Dtc_Query.get_dtc_query
        return self.execute(query, variables)

    # ECU Functions:
    def get_ecu(self, variables=None):
        query = Ecu_Query.get_ecu_query
        return self.execute(query, variables)

    # Formula Functions:
    def upsert_formula(self, variables=None):
        mutation = Formula_Mutation.upsert_formula_mutation
        return self.execute(mutation, variables)

    def upsert_formula_constant(self, variables=None):
        mutation = Formula_Mutation.upsert_formula_constant_mutation
        return self.execute(mutation, variables)

    def load_formula(self, variables=None):
        query = Formula_Query.load_formula_query
        return self.execute(query, variables)

    def calculate_formula(self, variables=None):
        query = Formula_Query.calculate_formula_query
        return self.execute(query, variables)

    # GPS Functions
    def upsert_gps(self, variables=None):
        mutation = GPS_Mutation.upsert_gps_mutation
        return self.execute(mutation, variables)

    def delete_gps(self, variables=None):
        mutation = GPS_Mutation.delete_gps_mutation
        return self.execute(mutation, variables)

    def get_gps(self, variables=None):
        query = GPS_Query.get_gps_query
        return self.execute(query, variables)

    # Message Functions
    def create_message(self, variables=None):
        mutation = Message_Mutation.create_message_mutation
        return self.execute(mutation, variables)

    def get_message(self, variables=None):
        query = Message_Query.get_message_query
        return self.execute(query, variables)

    # Network Stats Functions
    def create_network_stats(self, variables=None):
        mutation = Network_Stats_Mutation.create_network_stats_mutation
        return self.execute(mutation, variables)

    def get_network_stats(self, variables=None):
        query = Network_Stats_Query.get_network_stats_query
        return self.execute(query, variables)

    # Network Functions
    def get_network(self, variables=None):
        query = Network_Query.get_network_query
        return self.execute(query, variables)

    # Signal Functions
    def upsert_signal_data(self, variables=None):
        mutation = Signals_Mutation.upsert_signal_data_mutation
        return self.execute(mutation, variables)

    def delete_signal_data(self, variables=None):
        mutation = Signals_Mutation.delete_signal_data_mutation
        return self.execute(mutation, variables)

    def get_signals(self, variables=None):
        query = Signals_Query.get_signals_query
        return self.execute(query, variables)

    def get_signal_data(self, variables=None):
        query = Signals_Query.get_signals_data_query
        return self.execute(query, variables)

    # Version Functions
    def upsert_version(self, variables=None):
        mutation = Version_Mutation.upsert_version_mutation
        return self.execute(mutation, variables)

    def delete_version(self, variables=None):
        mutation = Version_Mutation.delete_version_mutation
        return self.execute(mutation, variables)

    def get_version(self, variables=None):
        query = Version_Query.get_version_query
        return self.execute(query, variables)
