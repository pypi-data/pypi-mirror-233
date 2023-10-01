# Copyright (c) 2015 FUJITSU LIMITED
# Copyright (c) 2012 EMC Corporation.
# Copyright (c) 2012 OpenStack Foundation
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
#

"""
FibreChannel Cinder Volume driver for Fujitsu ETERNUS DX S3 series.
"""
from oslo_log import log as logging

from cinder.common import constants
from cinder import exception
from cinder.i18n import _
from cinder import interface
from cinder.volume import driver
from cinder.volume.drivers.fujitsu.eternus_dx import eternus_dx_common
from cinder.zonemanager import utils as fczm_utils

LOG = logging.getLogger(__name__)


@interface.volumedriver
class FJDXFCDriver(driver.FibreChannelDriver):
    """FC Cinder Volume Driver for Fujitsu ETERNUS DX S3 series."""

    # ThirdPartySystems wiki page
    CI_WIKI_NAME = "Fujitsu_ETERNUS_CI"
    VERSION = eternus_dx_common.FJDXCommon.VERSION

    def __init__(self, *args, **kwargs):

        super(FJDXFCDriver, self).__init__(*args, **kwargs)
        self.common = eternus_dx_common.FJDXCommon(
            'fc',
            configuration=self.configuration)
        self.VERSION = self.common.VERSION

    @staticmethod
    def get_driver_options():
        return eternus_dx_common.FJDXCommon.get_driver_options()

    def check_for_setup_error(self):
        if not self.common.pywbemAvailable:
            msg = _('pywbem could not be imported! '
                    'pywbem is necessary for this volume driver.')
            LOG.error(msg)
            raise exception.VolumeBackendAPIException(data=msg)

    def create_volume(self, volume):
        """Create volume."""
        model_update = self.common.create_volume(volume)

        return model_update

    def create_volume_from_snapshot(self, volume, snapshot):
        """Creates a volume from a snapshot."""
        location, metadata = (
            self.common.create_volume_from_snapshot(volume, snapshot))

        v_metadata = self._get_metadata(volume)
        metadata.update(v_metadata)

        return {'provider_location': str(location), 'metadata': metadata}

    def create_cloned_volume(self, volume, src_vref):
        """Create cloned volume."""
        location, metadata = (
            self.common.create_cloned_volume(volume, src_vref))

        v_metadata = self._get_metadata(volume)
        metadata.update(v_metadata)

        return {'provider_location': str(location), 'metadata': metadata}

    def delete_volume(self, volume):
        """Delete volume on ETERNUS."""
        self.common.delete_volume(volume)

    def create_snapshot(self, snapshot):
        """Creates a snapshot."""
        location, metadata = self.common.create_snapshot(snapshot)

        return {'provider_location': str(location)}

    def delete_snapshot(self, snapshot):
        """Deletes a snapshot."""
        self.common.delete_snapshot(snapshot)

    def ensure_export(self, context, volume):
        """Driver entry point to get the export info for an existing volume."""
        return

    def create_export(self, context, volume, connector):
        """Driver entry point to get the export info for a new volume."""
        return

    def remove_export(self, context, volume):
        """Driver entry point to remove an export for a volume."""
        return

    def initialize_connection(self, volume, connector):
        """Allow connection to connector and return connection info."""
        info = self.common.initialize_connection(volume, connector)

        data = info['data']
        init_tgt_map = (
            self.common.build_fc_init_tgt_map(connector, data['target_wwn']))
        data['initiator_target_map'] = init_tgt_map

        info['data'] = data
        fczm_utils.add_fc_zone(info)
        return info

    def terminate_connection(self, volume, connector, **kwargs):
        """Disallow connection from connector."""
        self.common.terminate_connection(volume, connector)

        info = {'driver_volume_type': 'fibre_channel',
                'data': {}}

        if connector:
            attached = self.common.check_attached_volume_in_zone(connector)
            if not attached:
                # No more volumes attached to the host
                init_tgt_map = self.common.build_fc_init_tgt_map(connector)
                info['data'] = {'initiator_target_map': init_tgt_map}
                fczm_utils.remove_fc_zone(info)

        return info

    def get_volume_stats(self, refresh=False):
        """Get volume stats."""
        pool_name = None
        if refresh is True:
            data, pool_name = self.common.update_volume_stats()
            backend_name = self.configuration.safe_get('volume_backend_name')
            data['volume_backend_name'] = backend_name or 'FJDXFCDriver'
            data['storage_protocol'] = constants.FC
            self._stats = data

        LOG.debug('get_volume_stats, '
                  'pool name: %s.', pool_name)
        return self._stats

    def extend_volume(self, volume, new_size):
        """Extend volume."""
        self.common.extend_volume(volume, new_size)

    def _get_metadata(self, volume):
        v_metadata = volume.get('volume_metadata')
        if v_metadata:
            ret = {data['key']: data['value'] for data in v_metadata}
        else:
            ret = volume.get('metadata', {})

        return ret
