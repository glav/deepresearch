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
