# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""BIG-IP® system failover module

REST URI
    ``http://localhost/mgmt/tm/shared/license``

GUI Path
    ``System --> License``

REST Kind
    ``tm:shared:licensing:*``
"""

from f5.bigip.resource import PathElement
from f5.bigip.resource import UnnamedResource
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedOperation


class Licensing(PathElement):
    """BIG-IP® licensing stats and states.

    Licensing objects themselves do not support any methods and are just
    containers for lower level objects.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, shared):
        super(Licensing, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Activation,
            Registration,
        ]
        self._meta_data['attribute_registry'] = {
            'tm:shared:licensing:activation:activatelicenseresponse':
                Activation,
            'tm:shared:licensing:registration:registrationlicenseresponse':
                Registration,
        }


class Activation(Resource):
    """BIG-IP® license activation status

    Activation state objects only support GET/POST/PUT HTTP methods.
    To start the license activation process use create() method on a resource.
    To modify the started license activation process use update() method on a resource.


    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, licensing):
        super(Activation, self).__init__(licensing)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:shared:licensing:activation:activatelicenseresponse'
        self._meta_data['required_creation_parameters'] = {'baseRegKey'}

    def create(self, **kwargs):
        requests_params = self._handle_requests_params(kwargs)
        self._check_create_parameters(**kwargs)
        kwargs = self._check_for_python_keywords(kwargs)

        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri'] + 'activation/'
        session = self._meta_data['bigip']._meta_data['icr_session']

        kwargs = self._prepare_request_json(kwargs)

        # Invoke the REST operation on the device.
        response = session.post(_create_uri, json=kwargs, **requests_params)

        # Make new instance of self
        result = self._produce_instance(response)
        return result

    def load(self, **kwargs):
        newinst = self._stamp_out_core()
        newinst._refresh(**kwargs)
        return newinst

    def modify(self, **kwargs):
        """Modify is not supported for License Registration

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for License Registration

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Registration(UnnamedResource):
    """BIG-IP® license registration

    Registration endpoint only supports GET/PUT/DELETE HTTP methods.

    To revoke device license use delete() method on the loaded object.
    To activate license manually use update() method on the loaded object.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, licensing):
        super(Registration, self).__init__(licensing)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:shared:licensing:activation:activatelicenseresponse'
        self._meta_data['read_only_attributes'] = ['generation', 'lastUpdateMicros']

    def delete(self, **kwargs):
        requests_params = self._handle_requests_params(kwargs)
        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Check the generation for match before delete
        force = self._check_force_arg(kwargs.pop('force', True))
        if not force:
            self._check_generation()

        response = session.delete(delete_uri, **requests_params)
        if response.status_code == 200:
            self.__dict__ = {'deleted': True}

    def modify(self, **kwargs):
        """Modify is not supported for License Registration

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )
