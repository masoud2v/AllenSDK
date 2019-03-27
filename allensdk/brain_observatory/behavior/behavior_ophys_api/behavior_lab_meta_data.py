from datetime import datetime
from dateutil.tz import tzlocal
from marshmallow import Schema, fields
import os

from pynwb import get_type_map, TimeSeries, NWBFile, register_class, docval, load_namespaces, popargs
from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec
from pynwb.file import LabMetaData

TYPE_DICT = {fields.Float: 'float'}

class OphysBehaviorMetaDataSchema(Schema):
    """ base schema for all timeseries
    """

    a = fields.Float(
        doc='The time of the experiment (in seconds) when this observation or event occured',
        required=True,
    )


attributes = []
for name, val in OphysBehaviorMetaDataSchema().fields.items():
    nwb_attribute_spec = NWBAttributeSpec(name=name, dtype=TYPE_DICT[type(val)], doc=val.metadata['doc'])
    attributes.append(nwb_attribute_spec)

# import sys
# sys.exit(0)

prefix = 'AIBS_ophys_behavior'
lab_metadata_schema_loc = '/home/nicholasc/projects/allensdk'
extension_doc = 'AIBS Visual Behavior ophys lab metadata extension'

ext_source = '%s_extension.yaml' % prefix
ns_path = '%s_namespace.yaml' % prefix

ns_builder = NWBNamespaceBuilder(extension_doc, prefix)
metadata_ext_group_spec = NWBGroupSpec(
    neurodata_type_def='OphysBehaviorMetaData',
    neurodata_type_inc='LabMetaData',
    doc=extension_doc,
    attributes=attributes)
ns_builder.add_spec(ext_source, metadata_ext_group_spec)
ns_builder.export(ns_path, outdir=lab_metadata_schema_loc)
ns_abs_path = os.path.join(lab_metadata_schema_loc, ns_path)
load_namespaces(ns_abs_path)


@register_class('OphysBehaviorMetaData', prefix)
class OphysBehaviorMetaData(LabMetaData):
    __nwbfields__ = ('test_attr',)

    @docval({'name': 'name', 'type': str, 'doc': 'name'},
            {'name': 'test_attr', 'type': float, 'doc': 'test attribute'})
    def __init__(self, **kwargs):
        test_attr = popargs('test_attr', kwargs)
        super(OphysBehaviorMetaData, self).__init__(**kwargs)
        self.test_attr = test_attr


if __name__ == "__main__":

    nwbfile = NWBFile("a file with header data", "NB123A", datetime(2017, 5, 1, 12, 0, 0, tzinfo=tzlocal()))
    nwbfile.add_lab_meta_data(OphysBehaviorMetaData(name='a', test_attr=5.))

    print(nwbfile)
