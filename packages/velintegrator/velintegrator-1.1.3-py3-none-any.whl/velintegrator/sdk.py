from requests import request
from json import JSONDecodeError
from velilogger import logger


class Integrator:
    absolute_url = None
    secret_key = None
    headers = {}
    service = None

    def __init__(self, model=None):
        self.data = self.set_data(model)

    def validate_response(self, response):
        if response.status_code not in [200, 201, 204]:
            response_content = "Invalid response, status code: " + str(response.status_code) + " " + \
                               str(response.json())
            logger.error(f"{self.service} {response.url} response : {response_content}")
            return response_content
        try:
            response_content = response.json().get('id', response.json())
        except JSONDecodeError:
            response_content = f"Response content: {response.content}, Response: {response}"
        logger.info(f"{self.service} {response.url} response : {response_content}")
        return response_content

    def set_data(self, model):
        return model.dict() if model else None

    def test(self):
        print(self.data)
        return self.data


class CrudIntegrator(Integrator):
    object_types = {}
    secret_key = None
    absolute_url = None
    data_constraints = {}

    def __init__(self, object_type, model=None):
        self.object_type: str = object_type
        super().__init__(model)
        self.validate_object()

    def create_object(self, object_id, extra_headers: dict = {}):
        if not self.validate_data():
            return
        self.headers.update(extra_headers)
        endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}"
        response = request("POST", endpoint, json=self.data, headers=self.headers)
        crud_model = self.object_types[self.object_type]['model']
        validated_response = self.validate_response(response)
        if response.status_code == 201:
            fields = crud_model._meta.fields
            crud_object_dict = {field.name: self.data[field.name] if field.name in self.data else '' for field in
                                fields}
            crud_object_dict['id'] = int(validated_response)
            crud_object_dict['object_id'] = object_id
            crud_model.objects.create(**crud_object_dict)
        return validated_response

    def update_object(self, object_id: int, extra_headers: dict = {}):
        self.headers.update(extra_headers)
        crud_model = self.object_types[self.object_type]['model']
        try:
            crud_object = crud_model.objects.get(object_id=object_id)
            endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}/{crud_object.id}"
            response = request("PATCH", endpoint, json=self.data, headers=self.headers)
            return self.validate_response(response)
        except crud_model.DoesNotExist:
            logger.error(f"{self.service} Internal Error - response : {object_id} does not exist in {crud_model}")
            return

    def delete_object(self, object_id: int = None, extra_headers: dict = {}):
        self.headers.update(extra_headers)
        crud_model = self.object_types[self.object_type]['model']
        try:
            crud_object = crud_model.objects.get(object_id=object_id)
            endpoint = f"{self.absolute_url}/{self.object_types[self.object_type]['endpoint']}/{crud_object.id}"
            response = request("DELETE", endpoint, headers=self.headers)
            crud_object.delete()
            return self.validate_response(response)
        except crud_model.DoesNotExist:
            logger.error(f"{self.service} Internal Error - response : {object_id} does not exist in {crud_model}")
            return

    def validate_object(self):
        if self.object_type not in self.object_types:
            raise ValueError(
                f"Invalid object type: {self.object_type}. "
                f"Supported object types are: {list(self.object_types.keys())}")

    def validate_data(self):
        if self.object_type in self.data_constraints:
            object_query_permission = self.data_constraints[self.object_type]
            for key, value in object_query_permission.items():
                if self.data[key] in value:
                    return False
        return True
