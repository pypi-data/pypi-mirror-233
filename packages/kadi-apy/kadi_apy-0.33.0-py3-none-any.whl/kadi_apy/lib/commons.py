# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from kadi_apy.lib.helper import chunked_response


class PermissionMixin:
    """Mixin for adding, changing and removing a user role and a group role."""

    def add_user(self, user_id, role_name):
        """Add a user role.

        :param user_id: The ID of the user to add.
        :type user_id: int
        :param role_name: Role of the User.
        :type role_name: str
        :return: The Response object.

        """
        endpoint = f"{self.base_path}/{self.id}/roles/users"
        data = {"role": {"name": role_name}, "user": {"id": user_id}}

        return self._post(endpoint, json=data)

    def change_user_role(self, user_id, role_name):
        """Change user role.

        :param user_id: The ID of the user whose role should be changed.
        :type user_id: int
        :param role_name: Name of the new role.
        :type role_name: str
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users/{user_id}"
        data = {"name": role_name}
        return self._patch(endpoint, json=data)

    def remove_user(self, user_id):
        """Remove a user role.

        :param user_id: The ID of the user to remove.
        :type user_id: int
        :return: The response object.
        """
        endpoint = f"{self.base_path}/{self.id}/roles/users/{user_id}"
        return self._delete(endpoint, json=None)

    def add_group_role(self, group_id, role_name):
        """Add a group role.

        :param group_id: The ID of the group to add.
        :type group_id: int
        :param role_name: Role of the group.
        :type role_name: str
        :return: The response object.
        """
        endpoint = f"{self.base_path}/{self.id}/roles/groups"
        data = {"role": {"name": role_name}, "group": {"id": group_id}}

        return self._post(endpoint, json=data)

    def change_group_role(self, group_id, role_name):
        """Change group role.

        :param group_id: The ID of the group whose role should be changed.
        :type group_id: int
        :param role_name: Name of the new role.
        :type role_name: str
        :return: The response object.
        """
        endpoint = f"{self.base_path}/{self.id}/roles/groups/{group_id}"
        data = {"name": role_name}

        return self._patch(endpoint, json=data)

    def remove_group_role(self, group_id):
        """Remove a group role.

        :param group_id: The ID of the group to remove.
        :type group_id: int
        :return: The response object.
        """
        endpoint = f"{self.base_path}/{self.id}/roles/groups/{group_id}"
        return self._delete(endpoint, json=None)


def add_collection_link(item, collection_id):
    """Add a collection."""
    endpoint = f"{item.base_path}/{item.id}/collections"
    data = {"id": collection_id}

    return item._post(endpoint, json=data)


def remove_collection_link(item, collection_id):
    """Remove a collection."""
    endpoint = f"{item.base_path}/{item.id}/collections/{collection_id}"
    return item._delete(endpoint, json=None)


def add_record_link(item, record_id):
    """Add a record."""
    endpoint = f"{item.base_path}/{item.id}/records"
    data = {"id": record_id}

    return item._post(endpoint, json=data)


def remove_record_link(item, record_id):
    """Remove a record."""
    endpoint = f"{item.base_path}/{item.id}/records/{record_id}"
    return item._delete(endpoint, json=None)


def get_tags(item):
    """Get tags."""
    return item.meta["tags"]


def check_tag(item, tag):
    """Check if a certain tag is already present."""
    return tag.lower() in item.get_tags()


def add_tag(item, tag):
    """Add a tag."""
    endpoint = f"{item.base_path}/{item.id}"
    tags = item.get_tags()

    return item._patch(endpoint, json={"tags": tags + [tag.lower()]})


def remove_tag(item, tag):
    """Remove a tag."""
    endpoint = f"{item.base_path}/{item.id}"

    tag = tag.lower()
    tags = [t for t in item.get_tags() if t != tag]

    return item._patch(endpoint, json={"tags": tags})


def set_attribute(item, attribute, value):
    """Set attribute."""
    endpoint = f"{item.base_path}/{item.id}"
    attribute = {attribute: value}

    return item._patch(endpoint, json=attribute)


def export(item, path, export_type="json", pipe=False, **params):
    """Export a resource using a specific export type."""
    response = item._get(
        f"{item.base_path}/{item.id}/export/{export_type}", params=params, stream=True
    )

    if not pipe and response.status_code == 200:
        chunked_response(path, response)

    return response
