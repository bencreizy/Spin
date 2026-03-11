def generate_fractured_xml_response(target_id: str, injection_node: str):
    """
    Universal XML Fracture: Forces Array Coercion God Mode.
    Injects a complex node into the ID field to break logic containment.
    """
    xml_structure = f'''
<Subject>
    <NameID>
        {target_id}
        <{injection_node}>{target_id}</{injection_node}>
    </NameID>
</Subject>
'''
    return xml_structure