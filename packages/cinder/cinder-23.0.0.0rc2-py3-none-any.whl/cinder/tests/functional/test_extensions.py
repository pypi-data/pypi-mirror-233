# Copyright 2011 Justin Santa Barbara
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from http import client as http_client

import iso8601
from oslo_config import cfg
from oslo_serialization import jsonutils
import webob

from cinder.api import extensions
from cinder.api.v3 import router
from cinder.tests.functional import functional_helpers


NS = "{http://docs.openstack.org/common/api/v1.0}"
CONF = cfg.CONF


class ExtensionTestCase(functional_helpers._FunctionalTestBase):
    def _get_flags(self):
        f = super(ExtensionTestCase, self)._get_flags()
        f['osapi_volume_extension'] = {'v': CONF.osapi_volume_extension[:]}
        f['osapi_volume_extension']['v'].append(
            'cinder.tests.functional.api.foxinsocks.Foxinsocks')
        return f


class ExtensionsTest(ExtensionTestCase):
    def test_get_foxnsocks(self):
        """Simple check that fox-n-socks works."""
        response = self.api.api_request('/foxnsocks')
        foxnsocks = response.text
        self.assertEqual('Try to say this Mr. Knox, sir...', foxnsocks)


class ExtensionControllerTest(ExtensionTestCase):

    def setUp(self):
        super(ExtensionControllerTest, self).setUp()
        self.ext_list = ["TypesManage", "TypesExtraSpecs", ]
        self.ext_list.sort()

    def test_list_extensions_json(self):
        app = router.APIRouter()
        request = webob.Request.blank("/fake/extensions")
        response = request.get_response(app)
        self.assertEqual(http_client.OK, response.status_int)

        # Make sure we have all the extensions, extra extensions being OK.
        data = jsonutils.loads(response.body)
        names = [str(x['name']) for x in data['extensions']
                 if str(x['name']) in self.ext_list]
        names.sort()
        self.assertEqual(self.ext_list, names)

        # Ensure all the timestamps are valid according to iso8601
        for ext in data['extensions']:
            iso8601.parse_date(ext['updated'])

        # Make sure that at least Fox in Sox is correct.
        (fox_ext, ) = [
            x for x in data['extensions'] if x['alias'] == 'FOXNSOX']
        self.assertEqual(
            {'name': 'Fox In Socks',
             'updated': '2011-01-22T13:25:27-06:00',
             'description': 'The Fox In Socks Extension.',
             'alias': 'FOXNSOX',
             'links': []},
            fox_ext)

        for ext in data['extensions']:
            url = '/fake/extensions/%s' % ext['alias']
            request = webob.Request.blank(url)
            response = request.get_response(app)
            output = jsonutils.loads(response.body)
            self.assertEqual(ext['alias'], output['extension']['alias'])

    def test_get_extension_json(self):
        app = router.APIRouter()
        request = webob.Request.blank("/fake/extensions/FOXNSOX")
        response = request.get_response(app)
        self.assertEqual(http_client.OK, response.status_int)

        data = jsonutils.loads(response.body)
        self.assertEqual(
            {"name": "Fox In Socks",
             "updated": "2011-01-22T13:25:27-06:00",
             "description": "The Fox In Socks Extension.",
             "alias": "FOXNSOX",
             "links": []}, data['extension'])

    def test_get_non_existing_extension_json(self):
        app = router.APIRouter()
        request = webob.Request.blank("/fake/extensions/4")
        response = request.get_response(app)
        self.assertEqual(http_client.NOT_FOUND, response.status_int)


class StubExtensionManager(object):
    """Provides access to Tweedle Beetles."""

    name = "Tweedle Beetle Extension"
    alias = "TWDLBETL"

    def __init__(self, resource_ext=None, action_ext=None, request_ext=None,
                 controller_ext=None):
        self.resource_ext = resource_ext
        self.controller_ext = controller_ext
        self.extra_resource_ext = None

    def get_resources(self):
        resource_exts = []
        if self.resource_ext:
            resource_exts.append(self.resource_ext)
        if self.extra_resource_ext:
            resource_exts.append(self.extra_resource_ext)
        return resource_exts

    def get_controller_extensions(self):
        controller_extensions = []
        if self.controller_ext:
            controller_extensions.append(self.controller_ext)
        return controller_extensions


class ExtensionControllerIdFormatTest(ExtensionTestCase):

    def _bounce_id(self, test_id):

        class BounceController(object):
            def show(self, req, id):
                return id
        res_ext = extensions.ResourceExtension('bounce',
                                               BounceController())
        manager = StubExtensionManager(res_ext)
        app = router.APIRouter(manager)
        request = webob.Request.blank("/fake/bounce/%s" % test_id)
        response = request.get_response(app)
        return response.body

    def test_id_with_json_format(self):
        result = self._bounce_id('foo.json')
        self.assertEqual(b'foo', result)

    def test_id_with_bad_format(self):
        result = self._bounce_id('foo.bad')
        self.assertEqual(b'foo.bad', result)
