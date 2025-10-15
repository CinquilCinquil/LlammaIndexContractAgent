import ast
from llama_index.core.tools import FunctionTool
from data_validation import validate_contract_json
from pydantic import ValidationError
from typing import Annotated, Tuple, Union

def make_save_to_file_tool():
    def save_to_file_tool(content : Annotated[str, "The content to write on the file"],
    ) -> str:
        """Useful for writting and saving something on a file"""
        print("SAVE FILE TOOL USED")
        with open("model_output.txt", 'w') as file:
            file.write(content)

    return FunctionTool.from_defaults(save_to_file_tool)

def make_load_file_tool(embeddingManager):

    def load_file_tool( 
        filepath : Annotated[str, "The path of the file"]
        ) -> bool:
        """Useful for loading files. Returns whether the loading was successful."""
        print("LOAD FILE TOOL USED")
        return embeddingManager.insert(filepath)

    return FunctionTool.from_defaults(load_file_tool)

def make_query_tool(llm, embeddingManager):

    def query_tool(query : Annotated[str, "The query regarding a loaded document"]) -> str:
        """
        Use this tool only once per query for analyzing/searching/parsing/looking the document database.
        DO NOT REPEAT unless asked for a different question.
        """
        print("QUERY FILES TOOL USED")
        
        # make a query engine from the current index
        query_engine = embeddingManager.query_engine(llm)
        response = query_engine.query(query)
        return response
    
    return FunctionTool.from_defaults(query_tool)

def make_update_contract(contractStorage):
    def update_contract(
            contract_id : Annotated[int, "The Contract Id"],
            new_json : Annotated[str, "The full updated json (as a python dict) with the contract information"],
            is_complete : Annotated[bool, "Whether all the json fields are filled with information about the contract"]
    ) -> Union[str, None]:
        """
        Useful for updating a contract json on the system.
        """
        new_json = ast.literal_eval(new_json)
        print("UPDATE CONTRACT TOOL USED", contract_id, is_complete)
        print(new_json)
        try:
            validate_contract_json(new_json)
            contractStorage.updateContract(contract_id, new_json, is_complete)
            print("UPDATE SUCCESSFUL")
        except ValidationError as e:
            print("UPDATE ERROR: Json was not complete.")
            return repr(e)
    
    return FunctionTool.from_defaults(update_contract)

def make_add_contract(contractStorage):
    def add_contract(
        contract_json : Annotated[str, "The complete json (as a python dict) with the contract information"],
        is_complete : Annotated[bool, "Whether all the json fields are filled with information about the contract"]
    ) -> Union[int, str]:
        """
        Useful for registering a contract json on the system. Returns the Contract Id (int) or an error message (str).
        Error messages happen when the argument 'contract_json' was not complete with all required fields (filled with values or not).
        """
        contract_json = ast.literal_eval(contract_json)
        print("ADD CONTRACT TOOL USED", is_complete)
        print(contract_json)

        try:
            validate_contract_json(contract_json)

            contract_id = contractStorage.addContract(contract_json, is_complete)
            print("NEW CONTRACT ID: ", contract_id)
            return contract_id
        except ValidationError as e:
            print("ERROR: Json was not complete.")
            return repr(e)

    return FunctionTool.from_defaults(add_contract)

def make_get_contract(contractStorage):
    def get_contract(
        contract_id : Annotated[int, "The Contract Id"]
    ) -> Tuple[str, bool]:
        print("GET CONTRACT TOOL USED", contract_id)
        """
        Useful for retrieving a contract json from the system. Returns the Contract Json and a bool indicating if its complete
        """
        print(contractStorage.getContract(contract_id))
        return contractStorage.getContract(contract_id)
    
    return FunctionTool.from_defaults(get_contract)

def make_tools(llm, embeddingManager, contractStorage):
    tools = [
        make_load_file_tool(embeddingManager),
        make_query_tool(llm, embeddingManager),
        make_add_contract(contractStorage),
        make_update_contract(contractStorage),
        make_get_contract(contractStorage),
        make_save_to_file_tool()
    ]

    return tools