from enum import Enum

class ContractState(Enum):
    Incomplete = 0
    Complete = 1

class ContractStorage:
    """
        This class manages intermediary
        versions of contract json's stored during execution.
    """
    def __init__(self):
        self.current_contract = None
        self.contract_state = {}
        self.contracts = {}
        self.current_id = 0

    def setCurrentContract(self, contract, id):
        self.current_contract = id
        self.contracts[id] = contract
        self.contract_state[id] = ContractState.Incomplete

    def setComplete(self, id):
        self.contract_state[id] = ContractState.Complete

    def addContract(self, contract, is_complete):
        self.contracts[self.nextId()] = contract
        self.contract_state[self.current_id] = ContractState.Complete if is_complete else ContractState.Incomplete
        return self.current_id

    def updateContract(self, contract_id, new_json, is_complete):
        self.contracts[contract_id] = new_json
        self.contract_state[contract_id] = ContractState.Complete if is_complete else ContractState.Incomplete

    def getContract(self, contract_id):
        return (self.contracts[contract_id], self.contract_state[contract_id] == ContractState.Complete)

    def nextId(self):
        self.current_id += 1
        return self.current_id