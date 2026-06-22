from schema import LegalResponse

obj = LegalResponse(
    answer="Test",
    relevant_law="Consumer Protection Act",
    source="consumer.pdf",
    possible_actions=[
        "File complaint",
        "Contact authority"
    ]
)

print(obj)