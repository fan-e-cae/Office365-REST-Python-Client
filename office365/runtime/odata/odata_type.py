import datetime
import uuid


class ODataType(object):

    standard_types = {
        bool: "Edm.Boolean",
        int: "Edm.Int32",
        str: "Edm.String",
        datetime.datetime: "Edm.DateTimeOffset",
        uuid.UUID: "Edm.Guid"
    }
    """Primitive OData data type mapping"""

    def __init__(self):
        self.name = None
        self.namespace = None
        self.baseType = None
        self.properties = {}
        self.methods = {}

    @staticmethod
    def resolve_type(client_type):
        """
        Resolve OData type name

        :param str or int or bool or uuid or ClientValue or list[str or int or bool or uuid] client_type: Client value
        """
        from office365.runtime.client_value import ClientValue
        from office365.runtime.client_value_collection import ClientValueCollection

        collection = False
        if isinstance(client_type, list):
            collection = True
            resolved_name = ODataType.standard_types.get(type(client_type[0]), None)
        elif isinstance(client_type, ClientValue):
            if isinstance(client_type, ClientValueCollection):
                collection = True
                resolved_name = client_type.item_type_name
            else:
                resolved_name = client_type.entity_type_name
        else:
            resolved_name = ODataType.standard_types.get(type(client_type), None)

        if resolved_name:
            return "Collection({0})".format(resolved_name) if collection else resolved_name
        else:
            return None

    def add_property(self, prop_schema):
        """
        :type prop_schema:  office365.runtime.odata.odata_property.ODataProperty
        """
        alias = prop_schema.name
        # if type_schema['state'] == 'detached':
        #    prop_schema['state'] = 'detached'
        # else:
        #    prop_schema['state'] = 'attached'
        # type_alias = type_schema['name']
        self.properties[alias] = prop_schema
