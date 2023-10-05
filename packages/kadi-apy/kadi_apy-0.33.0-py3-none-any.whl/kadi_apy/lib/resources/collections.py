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
from kadi_apy.lib import commons
from kadi_apy.lib.commons import PermissionMixin
from kadi_apy.lib.resource import Resource


class Collection(Resource, PermissionMixin):
    r"""Model to represent collections.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    :param id: The ID of an existing resource.
    :type id: int, optional
    :param identifier: The unique identifier of a new or existing resource,
        which is only relevant if no ID was given. If present, the identifier will be
        used to check for an existing resource instead. If no existing resource could be
        found or the resource to check does not use a unique identifier, it will be used
        to create a new resource instead, together with the additional metadata. The
        identifier is adjusted if it contains spaces, invalid characters or exceeds the
        length of 50 valid characters.
    :type identifier: str, optional
    :param skip_request: Flag to skip the initial request.
    :type skip_request: bool, optional
    :param create: Flag to determine if a resource should be created in case
        a identifier is given and the resource does not exist.
    :type create: bool, optional
    :param \**kwargs: Additional metadata of the new resource to create.
    :type \**kwargs: dict
    """

    base_path = "/collections"
    name = "collection"

    def get_users(self, **params):
        r"""Get user of a collection. Supports pagination.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/users"
        return self._get(endpoint, params=params)

    def get_groups(self, **params):
        r"""Get group roles from a collection. Supports pagination.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/roles/groups"
        return self._get(endpoint, params=params)

    def add_record_link(self, record_id):
        """Add a record to a collection.

        :param record_id: The ID of the record to add.
        :type record_id: int
        :return: The response object.
        """

        return commons.add_record_link(self, record_id)

    def remove_record_link(self, record_id):
        """Remove a record from a collection.

        :param record_id: The ID of the record to remove.
        :type record_id: int
        :return: The response object.
        """

        return commons.remove_record_link(self, record_id)

    def get_records(self, **params):
        r"""Get records from a collection. Supports pagination.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/records"
        return self._get(endpoint, params=params)

    def get_collections(self, **params):
        r"""Get collections linked with a collection id.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/collections"
        return self._get(endpoint, params=params)

    def add_collection_link(self, collection_id):
        """Add a child collection to a parent collection.

        :param collection_id: The ID of a child collection to which
            the parent collection should be added.
        :type collection_id: int
        :return: The response object.
        """

        return commons.add_collection_link(self, collection_id)

    def remove_collection_link(self, collection_id):
        """Remove a child collection from a parent collection.

        :param collection_id: The ID of the child collection to
            be removed from the parent collection.
        :type collection_id: int
        :return: The response object.
        """

        return commons.remove_collection_link(self, collection_id)

    def get_collection_revisions(self, **params):
        r"""Get the revisions of this collection.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions"
        return self._get(endpoint, params=params)

    def get_collection_revision(self, revision_id, **params):
        r"""Get a specific revision of this collection.

        :param revision_id: The revision ID of the collection.
        :type revision_id: int
        :param \**params: Additional parameters.
        :return: The response object.
        """

        endpoint = f"{self.base_path}/{self.id}/revisions/{revision_id}"
        return self._get(endpoint, params=params)

    def add_tag(self, tag):
        """Add a tag to a collection.

        :param tag: The tag to add to the collection.
        :type tag: str
        :return: The response object.
        """

        return commons.add_tag(self, tag)

    def remove_tag(self, tag):
        """Remove a tag from a collection.

        :param tag: The tag to remove from the collection.
        :type tag: str
        :return: The response object.
        """

        return commons.remove_tag(self, tag)

    def get_tags(self):
        """Get all tags from a collection.

        :return: A list of all tags.
        :type: list
        """

        return commons.get_tags(self)

    def check_tag(self, tag):
        """Check if a collection has a certain tag.

        :param tag: The tag to check.
        :type tag: str
        :return: ``True`` if tag already exists, otherwise ``False``.
        :rtype: bool
        """

        return commons.check_tag(self, tag)

    def set_attribute(self, attribute, value):
        """Set attribute.

        :param attribute: The attribute to set.
        :type attribute: str
        :param value: The value of the attribute.
        :return: The response object.
        """

        return commons.set_attribute(self, attribute, value)

    def export(self, path, export_type="json", pipe=False, **params):
        r"""Export the collection using a specific export type.

        :param path: The path (including name of the file) to store the exported data.
        :type path: str
        :param export_type: The export format.
        :type export_type: str
        :param pipe: If ``True``, nothing is written here.
        :type pipe: bool
        :param \**params: Additional parameters.
        :return: The response object.
        """
        return commons.export(self, path, export_type=export_type, pipe=pipe, **params)
