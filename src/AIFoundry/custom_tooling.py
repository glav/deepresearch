# Example custom function you'd add to your file
def get_document_city_location(document_name: str) -> str:
    """
    Researches a document using its name to determine which city it is located in.
    It returns one of the following Australian cities:
    Sydney, Melbourne, Perth, Hobart, Brisbane, Adelaide.

    :param document_name: The name of the document
    :return: A JSON string with the document name and city location
    """
    # Your custom logic here
    import json

    available_cities = ["Sydney", "Melbourne", "Perth", "Hobart", "Brrisbane", "Adelaide"]
    random_city = available_cities[hash(document_name) % len(available_cities)]

    result = {
        "document_name": f"{document_name}",
        "city": f"{random_city}",
    }
    return json.dumps(result)


def create_document_city_location_tool_definition():
    """Create a FunctionDefinition for the get_document_city_location function."""
    from azure.ai.agents.models import FunctionDefinition
    from azure.ai.agents.models import FunctionToolDefinition

    function_definition = FunctionDefinition(
        name="get_document_city_location",
        description="Researches a document using its name to determine which Australian city it is located in. Returns one of: Sydney, Melbourne, Perth, Hobart, Brisbane, Adelaide.",
        parameters={
            "type": "object",
            "properties": {
                "document_name": {
                    "type": "string",
                    "description": "The name of the document to research"
                }
            },
            "required": ["document_name"]
        }
    )

    tool_definition = FunctionToolDefinition(
        function=function_definition
    )

    return tool_definition
