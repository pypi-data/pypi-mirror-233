# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: featureform/proto/metadata.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n featureform/proto/metadata.proto\x12\"featureform.serving.metadata.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\"\x14\n\x04Name\x12\x0c\n\x04name\x18\x01 \x01(\t\"\xbc\x01\n\x0eResourceStatus\x12I\n\x06status\x18\x01 \x01(\x0e\x32\x39.featureform.serving.metadata.proto.ResourceStatus.Status\x12\x15\n\rerror_message\x18\x02 \x01(\t\"H\n\x06Status\x12\r\n\tNO_STATUS\x10\x00\x12\x0b\n\x07\x43REATED\x10\x01\x12\x0b\n\x07PENDING\x10\x02\x12\t\n\x05READY\x10\x03\x12\n\n\x06\x46\x41ILED\x10\x04\"\x98\x01\n\nResourceID\x12\x41\n\x08resource\x18\x01 \x01(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12G\n\rresource_type\x18\x02 \x01(\x0e\x32\x30.featureform.serving.metadata.proto.ResourceType\"\x9b\x01\n\x10SetStatusRequest\x12\x43\n\x0bresource_id\x18\x01 \x01(\x0b\x32..featureform.serving.metadata.proto.ResourceID\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\"n\n\x15ScheduleChangeRequest\x12\x43\n\x0bresource_id\x18\x01 \x01(\x0b\x32..featureform.serving.metadata.proto.ResourceID\x12\x10\n\x08schedule\x18\x02 \x01(\t\",\n\x0bNameVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\"\x07\n\x05\x45mpty\"\x86\x01\n\x07\x46\x65\x61ture\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x17\n\x0f\x64\x65\x66\x61ult_variant\x18\x03 \x01(\t\x12\x10\n\x08variants\x18\x04 \x03(\t\"4\n\x07\x43olumns\x12\x0e\n\x06\x65ntity\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x12\n\n\x02ts\x18\x03 \x01(\t\"\x1f\n\x0ePythonFunction\x12\r\n\x05query\x18\x01 \x01(\x0c\"\"\n\x06Stream\x12\x18\n\x10offline_provider\x18\x01 \x01(\t\"\xfa\x06\n\x0e\x46\x65\x61tureVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12?\n\x06source\x18\x03 \x01(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0e\n\x06\x65ntity\x18\x05 \x01(\t\x12+\n\x07\x63reated\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05owner\x18\x07 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\x12\x10\n\x08provider\x18\t \x01(\t\x12\x42\n\x06status\x18\n \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x45\n\x0ctrainingsets\x18\x0b \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12>\n\x07\x63olumns\x18\x0c \x01(\x0b\x32+.featureform.serving.metadata.proto.ColumnsH\x00\x12\x46\n\x08\x66unction\x18\x11 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.PythonFunctionH\x00\x12<\n\x06stream\x18\x15 \x01(\x0b\x32*.featureform.serving.metadata.proto.StreamH\x00\x12\x30\n\x0clast_updated\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08schedule\x18\x0e \x01(\t\x12\x36\n\x04tags\x18\x0f \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x10 \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\x12\x41\n\x04mode\x18\x12 \x01(\x0e\x32\x33.featureform.serving.metadata.proto.ComputationMode\x12\x14\n\x0cis_embedding\x18\x13 \x01(\x08\x12\x11\n\tdimension\x18\x14 \x01(\x05\x42\n\n\x08location\"d\n\nFeatureLag\x12\x0f\n\x07\x66\x65\x61ture\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12&\n\x03lag\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\"\x84\x01\n\x05Label\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x17\n\x0f\x64\x65\x66\x61ult_variant\x18\x03 \x01(\t\x12\x10\n\x08variants\x18\x04 \x03(\t\"\x80\x05\n\x0cLabelVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12?\n\x06source\x18\x05 \x01(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x0e\n\x06\x65ntity\x18\x06 \x01(\t\x12+\n\x07\x63reated\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05owner\x18\x08 \x01(\t\x12\x10\n\x08provider\x18\t \x01(\t\x12\x42\n\x06status\x18\n \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x45\n\x0ctrainingsets\x18\x0b \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12>\n\x07\x63olumns\x18\x0c \x01(\x0b\x32+.featureform.serving.metadata.proto.ColumnsH\x00\x12<\n\x06stream\x18\x10 \x01(\x0b\x32*.featureform.serving.metadata.proto.StreamH\x00\x12\x36\n\x04tags\x18\r \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x0e \x01(\x0b\x32..featureform.serving.metadata.proto.PropertiesB\n\n\x08location\"\xc3\x04\n\x08Provider\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x10\n\x08software\x18\x04 \x01(\t\x12\x0c\n\x04team\x18\x05 \x01(\t\x12\x19\n\x11serialized_config\x18\x06 \x01(\x0c\x12\x42\n\x06status\x18\x07 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12@\n\x07sources\x18\x08 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x41\n\x08\x66\x65\x61tures\x18\t \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x45\n\x0ctrainingsets\x18\n \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12?\n\x06labels\x18\x0b \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x36\n\x04tags\x18\x0c \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\r \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\"\x8a\x01\n\x0bTrainingSet\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x17\n\x0f\x64\x65\x66\x61ult_variant\x18\x03 \x01(\t\x12\x10\n\x08variants\x18\x04 \x03(\t\"\xe3\x04\n\x12TrainingSetVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05owner\x18\x04 \x01(\t\x12+\n\x07\x63reated\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08provider\x18\x06 \x01(\t\x12\x42\n\x06status\x18\x07 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x41\n\x08\x66\x65\x61tures\x18\x08 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12>\n\x05label\x18\t \x01(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x30\n\x0clast_updated\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08schedule\x18\x0e \x01(\t\x12\x44\n\x0c\x66\x65\x61ture_lags\x18\x0f \x03(\x0b\x32..featureform.serving.metadata.proto.FeatureLag\x12\x36\n\x04tags\x18\x10 \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x11 \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\"\xb6\x03\n\x06\x45ntity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x42\n\x06status\x18\x03 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x41\n\x08\x66\x65\x61tures\x18\x04 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12?\n\x06labels\x18\x05 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x45\n\x0ctrainingsets\x18\x06 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x36\n\x04tags\x18\x07 \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x08 \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\"\xf1\x02\n\x05Model\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x41\n\x08\x66\x65\x61tures\x18\x03 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12?\n\x06labels\x18\x04 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x45\n\x0ctrainingsets\x18\x05 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x36\n\x04tags\x18\x06 \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x07 \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\"\xe1\x03\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x41\n\x08\x66\x65\x61tures\x18\x03 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12?\n\x06labels\x18\x04 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x45\n\x0ctrainingsets\x18\x05 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12@\n\x07sources\x18\x06 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x36\n\x04tags\x18\x08 \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\t \x01(\x0b\x32..featureform.serving.metadata.proto.Properties\"\x85\x01\n\x06Source\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x42\n\x06status\x18\x02 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\x17\n\x0f\x64\x65\x66\x61ult_variant\x18\x03 \x01(\t\x12\x10\n\x08variants\x18\x04 \x03(\t\"\x93\x06\n\rSourceVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12L\n\x0etransformation\x18\x0e \x01(\x0b\x32\x32.featureform.serving.metadata.proto.TransformationH\x00\x12\x46\n\x0bprimaryData\x18\x0f \x01(\x0b\x32/.featureform.serving.metadata.proto.PrimaryDataH\x00\x12\r\n\x05owner\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x10\n\x08provider\x18\x06 \x01(\t\x12+\n\x07\x63reated\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x42\n\x06status\x18\x08 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.ResourceStatus\x12\r\n\x05table\x18\t \x01(\t\x12\x45\n\x0ctrainingsets\x18\n \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x41\n\x08\x66\x65\x61tures\x18\x0b \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12?\n\x06labels\x18\x0c \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x30\n\x0clast_updated\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08schedule\x18\x10 \x01(\t\x12\x36\n\x04tags\x18\x11 \x01(\x0b\x32(.featureform.serving.metadata.proto.Tags\x12\x42\n\nproperties\x18\x12 \x01(\x0b\x32..featureform.serving.metadata.proto.PropertiesB\x0c\n\ndefinition\"\x95\x02\n\x0eTransformation\x12R\n\x11SQLTransformation\x18\x01 \x01(\x0b\x32\x35.featureform.serving.metadata.proto.SQLTransformationH\x00\x12P\n\x10\x44\x46Transformation\x18\x02 \x01(\x0b\x32\x34.featureform.serving.metadata.proto.DFTransformationH\x00\x12M\n\x0fkubernetes_args\x18\x03 \x01(\x0b\x32\x32.featureform.serving.metadata.proto.KubernetesArgsH\x01\x42\x06\n\x04typeB\x06\n\x04\x61rgs\"o\n\x17KubernetesResourceSpecs\x12\x13\n\x0b\x63pu_request\x18\x01 \x01(\t\x12\x11\n\tcpu_limit\x18\x02 \x01(\t\x12\x16\n\x0ememory_request\x18\x03 \x01(\t\x12\x14\n\x0cmemory_limit\x18\x04 \x01(\t\"r\n\x0eKubernetesArgs\x12\x14\n\x0c\x64ocker_image\x18\x01 \x01(\t\x12J\n\x05specs\x18\x02 \x01(\x0b\x32;.featureform.serving.metadata.proto.KubernetesResourceSpecs\"c\n\x11SQLTransformation\x12\r\n\x05query\x18\x01 \x01(\t\x12?\n\x06source\x18\x02 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\"w\n\x10\x44\x46Transformation\x12\r\n\x05query\x18\x01 \x01(\x0c\x12?\n\x06inputs\x18\x02 \x03(\x0b\x32/.featureform.serving.metadata.proto.NameVariant\x12\x13\n\x0bsource_text\x18\x03 \x01(\t\"_\n\x0bPrimaryData\x12\x44\n\x05table\x18\x01 \x01(\x0b\x32\x33.featureform.serving.metadata.proto.PrimarySQLTableH\x00\x42\n\n\x08location\"\x1f\n\x0fPrimarySQLTable\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x13\n\x04Tags\x12\x0b\n\x03tag\x18\x01 \x03(\t\"+\n\x08Property\x12\x16\n\x0cstring_value\x18\x01 \x01(\tH\x00\x42\x07\n\x05value\"\xbb\x01\n\nProperties\x12N\n\x08property\x18\x01 \x03(\x0b\x32<.featureform.serving.metadata.proto.Properties.PropertyEntry\x1a]\n\rPropertyEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12;\n\x05value\x18\x02 \x01(\x0b\x32,.featureform.serving.metadata.proto.Property:\x02\x38\x01\"\x7f\n\x17StreamingFeatureVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12\x0e\n\x06\x65ntity\x18\x03 \x01(\t\x12\r\n\x05value\x18\x04 \x01(\t\x12&\n\x02ts\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"}\n\x15StreamingLabelVariant\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07variant\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\x12\x0e\n\x06\x65ntity\x18\x04 \x01(\t\x12&\n\x02ts\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp*\xc9\x01\n\x0cResourceType\x12\x0b\n\x07\x46\x45\x41TURE\x10\x00\x12\t\n\x05LABEL\x10\x01\x12\x10\n\x0cTRAINING_SET\x10\x02\x12\n\n\x06SOURCE\x10\x03\x12\x13\n\x0f\x46\x45\x41TURE_VARIANT\x10\x04\x12\x11\n\rLABEL_VARIANT\x10\x05\x12\x18\n\x14TRAINING_SET_VARIANT\x10\x06\x12\x12\n\x0eSOURCE_VARIANT\x10\x07\x12\x0c\n\x08PROVIDER\x10\x08\x12\n\n\x06\x45NTITY\x10\t\x12\t\n\x05MODEL\x10\n\x12\x08\n\x04USER\x10\x0b*F\n\x0f\x43omputationMode\x12\x0f\n\x0bPRECOMPUTED\x10\x00\x12\x13\n\x0f\x43LIENT_COMPUTED\x10\x01\x12\r\n\tSTREAMING\x10\x02\x32\x88\x1a\n\x08Metadata\x12h\n\x0cListFeatures\x12).featureform.serving.metadata.proto.Empty\x1a+.featureform.serving.metadata.proto.Feature0\x01\x12u\n\x14\x43reateFeatureVariant\x12\x32.featureform.serving.metadata.proto.FeatureVariant\x1a).featureform.serving.metadata.proto.Empty\x12h\n\x0bGetFeatures\x12(.featureform.serving.metadata.proto.Name\x1a+.featureform.serving.metadata.proto.Feature(\x01\x30\x01\x12}\n\x12GetFeatureVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x32.featureform.serving.metadata.proto.FeatureVariant(\x01\x30\x01\x12\x64\n\nListLabels\x12).featureform.serving.metadata.proto.Empty\x1a).featureform.serving.metadata.proto.Label0\x01\x12q\n\x12\x43reateLabelVariant\x12\x30.featureform.serving.metadata.proto.LabelVariant\x1a).featureform.serving.metadata.proto.Empty\x12\x64\n\tGetLabels\x12(.featureform.serving.metadata.proto.Name\x1a).featureform.serving.metadata.proto.Label(\x01\x30\x01\x12y\n\x10GetLabelVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x30.featureform.serving.metadata.proto.LabelVariant(\x01\x30\x01\x12p\n\x10ListTrainingSets\x12).featureform.serving.metadata.proto.Empty\x1a/.featureform.serving.metadata.proto.TrainingSet0\x01\x12}\n\x18\x43reateTrainingSetVariant\x12\x36.featureform.serving.metadata.proto.TrainingSetVariant\x1a).featureform.serving.metadata.proto.Empty\x12p\n\x0fGetTrainingSets\x12(.featureform.serving.metadata.proto.Name\x1a/.featureform.serving.metadata.proto.TrainingSet(\x01\x30\x01\x12\x85\x01\n\x16GetTrainingSetVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x36.featureform.serving.metadata.proto.TrainingSetVariant(\x01\x30\x01\x12\x66\n\x0bListSources\x12).featureform.serving.metadata.proto.Empty\x1a*.featureform.serving.metadata.proto.Source0\x01\x12s\n\x13\x43reateSourceVariant\x12\x31.featureform.serving.metadata.proto.SourceVariant\x1a).featureform.serving.metadata.proto.Empty\x12\x66\n\nGetSources\x12(.featureform.serving.metadata.proto.Name\x1a*.featureform.serving.metadata.proto.Source(\x01\x30\x01\x12{\n\x11GetSourceVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x31.featureform.serving.metadata.proto.SourceVariant(\x01\x30\x01\x12\x62\n\tListUsers\x12).featureform.serving.metadata.proto.Empty\x1a(.featureform.serving.metadata.proto.User0\x01\x12\x61\n\nCreateUser\x12(.featureform.serving.metadata.proto.User\x1a).featureform.serving.metadata.proto.Empty\x12\x62\n\x08GetUsers\x12(.featureform.serving.metadata.proto.Name\x1a(.featureform.serving.metadata.proto.User(\x01\x30\x01\x12j\n\rListProviders\x12).featureform.serving.metadata.proto.Empty\x1a,.featureform.serving.metadata.proto.Provider0\x01\x12i\n\x0e\x43reateProvider\x12,.featureform.serving.metadata.proto.Provider\x1a).featureform.serving.metadata.proto.Empty\x12j\n\x0cGetProviders\x12(.featureform.serving.metadata.proto.Name\x1a,.featureform.serving.metadata.proto.Provider(\x01\x30\x01\x12g\n\x0cListEntities\x12).featureform.serving.metadata.proto.Empty\x1a*.featureform.serving.metadata.proto.Entity0\x01\x12\x65\n\x0c\x43reateEntity\x12*.featureform.serving.metadata.proto.Entity\x1a).featureform.serving.metadata.proto.Empty\x12g\n\x0bGetEntities\x12(.featureform.serving.metadata.proto.Name\x1a*.featureform.serving.metadata.proto.Entity(\x01\x30\x01\x12\x64\n\nListModels\x12).featureform.serving.metadata.proto.Empty\x1a).featureform.serving.metadata.proto.Model0\x01\x12\x63\n\x0b\x43reateModel\x12).featureform.serving.metadata.proto.Model\x1a).featureform.serving.metadata.proto.Empty\x12\x64\n\tGetModels\x12(.featureform.serving.metadata.proto.Name\x1a).featureform.serving.metadata.proto.Model(\x01\x30\x01\x12t\n\x11SetResourceStatus\x12\x34.featureform.serving.metadata.proto.SetStatusRequest\x1a).featureform.serving.metadata.proto.Empty\x12}\n\x15RequestScheduleChange\x12\x39.featureform.serving.metadata.proto.ScheduleChangeRequest\x1a).featureform.serving.metadata.proto.Empty2\xff\x1a\n\x03\x41pi\x12\x61\n\nCreateUser\x12(.featureform.serving.metadata.proto.User\x1a).featureform.serving.metadata.proto.Empty\x12i\n\x0e\x43reateProvider\x12,.featureform.serving.metadata.proto.Provider\x1a).featureform.serving.metadata.proto.Empty\x12s\n\x13\x43reateSourceVariant\x12\x31.featureform.serving.metadata.proto.SourceVariant\x1a).featureform.serving.metadata.proto.Empty\x12\x65\n\x0c\x43reateEntity\x12*.featureform.serving.metadata.proto.Entity\x1a).featureform.serving.metadata.proto.Empty\x12u\n\x14\x43reateFeatureVariant\x12\x32.featureform.serving.metadata.proto.FeatureVariant\x1a).featureform.serving.metadata.proto.Empty\x12q\n\x12\x43reateLabelVariant\x12\x30.featureform.serving.metadata.proto.LabelVariant\x1a).featureform.serving.metadata.proto.Empty\x12}\n\x18\x43reateTrainingSetVariant\x12\x36.featureform.serving.metadata.proto.TrainingSetVariant\x1a).featureform.serving.metadata.proto.Empty\x12\x63\n\x0b\x43reateModel\x12).featureform.serving.metadata.proto.Model\x1a).featureform.serving.metadata.proto.Empty\x12}\n\x15RequestScheduleChange\x12\x39.featureform.serving.metadata.proto.ScheduleChangeRequest\x1a).featureform.serving.metadata.proto.Empty\x12\x62\n\x08GetUsers\x12(.featureform.serving.metadata.proto.Name\x1a(.featureform.serving.metadata.proto.User(\x01\x30\x01\x12h\n\x0bGetFeatures\x12(.featureform.serving.metadata.proto.Name\x1a+.featureform.serving.metadata.proto.Feature(\x01\x30\x01\x12}\n\x12GetFeatureVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x32.featureform.serving.metadata.proto.FeatureVariant(\x01\x30\x01\x12\x64\n\tGetLabels\x12(.featureform.serving.metadata.proto.Name\x1a).featureform.serving.metadata.proto.Label(\x01\x30\x01\x12y\n\x10GetLabelVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x30.featureform.serving.metadata.proto.LabelVariant(\x01\x30\x01\x12p\n\x0fGetTrainingSets\x12(.featureform.serving.metadata.proto.Name\x1a/.featureform.serving.metadata.proto.TrainingSet(\x01\x30\x01\x12\x85\x01\n\x16GetTrainingSetVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x36.featureform.serving.metadata.proto.TrainingSetVariant(\x01\x30\x01\x12\x66\n\nGetSources\x12(.featureform.serving.metadata.proto.Name\x1a*.featureform.serving.metadata.proto.Source(\x01\x30\x01\x12{\n\x11GetSourceVariants\x12/.featureform.serving.metadata.proto.NameVariant\x1a\x31.featureform.serving.metadata.proto.SourceVariant(\x01\x30\x01\x12j\n\x0cGetProviders\x12(.featureform.serving.metadata.proto.Name\x1a,.featureform.serving.metadata.proto.Provider(\x01\x30\x01\x12g\n\x0bGetEntities\x12(.featureform.serving.metadata.proto.Name\x1a*.featureform.serving.metadata.proto.Entity(\x01\x30\x01\x12\x64\n\tGetModels\x12(.featureform.serving.metadata.proto.Name\x1a).featureform.serving.metadata.proto.Model(\x01\x30\x01\x12h\n\x0cListFeatures\x12).featureform.serving.metadata.proto.Empty\x1a+.featureform.serving.metadata.proto.Feature0\x01\x12\x64\n\nListLabels\x12).featureform.serving.metadata.proto.Empty\x1a).featureform.serving.metadata.proto.Label0\x01\x12p\n\x10ListTrainingSets\x12).featureform.serving.metadata.proto.Empty\x1a/.featureform.serving.metadata.proto.TrainingSet0\x01\x12\x66\n\x0bListSources\x12).featureform.serving.metadata.proto.Empty\x1a*.featureform.serving.metadata.proto.Source0\x01\x12\x62\n\tListUsers\x12).featureform.serving.metadata.proto.Empty\x1a(.featureform.serving.metadata.proto.User0\x01\x12j\n\rListProviders\x12).featureform.serving.metadata.proto.Empty\x1a,.featureform.serving.metadata.proto.Provider0\x01\x12g\n\x0cListEntities\x12).featureform.serving.metadata.proto.Empty\x1a*.featureform.serving.metadata.proto.Entity0\x01\x12\x64\n\nListModels\x12).featureform.serving.metadata.proto.Empty\x1a).featureform.serving.metadata.proto.Model0\x01\x12y\n\rWriteFeatures\x12;.featureform.serving.metadata.proto.StreamingFeatureVariant\x1a).featureform.serving.metadata.proto.Empty(\x01\x12u\n\x0bWriteLabels\x12\x39.featureform.serving.metadata.proto.StreamingLabelVariant\x1a).featureform.serving.metadata.proto.Empty(\x01\x42\'Z%github.com/featureform/metadata/protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'featureform.proto.metadata_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z%github.com/featureform/metadata/proto'
  _PROPERTIES_PROPERTYENTRY._options = None
  _PROPERTIES_PROPERTYENTRY._serialized_options = b'8\001'
  _globals['_RESOURCETYPE']._serialized_start=7797
  _globals['_RESOURCETYPE']._serialized_end=7998
  _globals['_COMPUTATIONMODE']._serialized_start=8000
  _globals['_COMPUTATIONMODE']._serialized_end=8070
  _globals['_NAME']._serialized_start=137
  _globals['_NAME']._serialized_end=157
  _globals['_RESOURCESTATUS']._serialized_start=160
  _globals['_RESOURCESTATUS']._serialized_end=348
  _globals['_RESOURCESTATUS_STATUS']._serialized_start=276
  _globals['_RESOURCESTATUS_STATUS']._serialized_end=348
  _globals['_RESOURCEID']._serialized_start=351
  _globals['_RESOURCEID']._serialized_end=503
  _globals['_SETSTATUSREQUEST']._serialized_start=506
  _globals['_SETSTATUSREQUEST']._serialized_end=661
  _globals['_SCHEDULECHANGEREQUEST']._serialized_start=663
  _globals['_SCHEDULECHANGEREQUEST']._serialized_end=773
  _globals['_NAMEVARIANT']._serialized_start=775
  _globals['_NAMEVARIANT']._serialized_end=819
  _globals['_EMPTY']._serialized_start=821
  _globals['_EMPTY']._serialized_end=828
  _globals['_FEATURE']._serialized_start=831
  _globals['_FEATURE']._serialized_end=965
  _globals['_COLUMNS']._serialized_start=967
  _globals['_COLUMNS']._serialized_end=1019
  _globals['_PYTHONFUNCTION']._serialized_start=1021
  _globals['_PYTHONFUNCTION']._serialized_end=1052
  _globals['_STREAM']._serialized_start=1054
  _globals['_STREAM']._serialized_end=1088
  _globals['_FEATUREVARIANT']._serialized_start=1091
  _globals['_FEATUREVARIANT']._serialized_end=1981
  _globals['_FEATURELAG']._serialized_start=1983
  _globals['_FEATURELAG']._serialized_end=2083
  _globals['_LABEL']._serialized_start=2086
  _globals['_LABEL']._serialized_end=2218
  _globals['_LABELVARIANT']._serialized_start=2221
  _globals['_LABELVARIANT']._serialized_end=2861
  _globals['_PROVIDER']._serialized_start=2864
  _globals['_PROVIDER']._serialized_end=3443
  _globals['_TRAININGSET']._serialized_start=3446
  _globals['_TRAININGSET']._serialized_end=3584
  _globals['_TRAININGSETVARIANT']._serialized_start=3587
  _globals['_TRAININGSETVARIANT']._serialized_end=4198
  _globals['_ENTITY']._serialized_start=4201
  _globals['_ENTITY']._serialized_end=4639
  _globals['_MODEL']._serialized_start=4642
  _globals['_MODEL']._serialized_end=5011
  _globals['_USER']._serialized_start=5014
  _globals['_USER']._serialized_end=5495
  _globals['_SOURCE']._serialized_start=5498
  _globals['_SOURCE']._serialized_end=5631
  _globals['_SOURCEVARIANT']._serialized_start=5634
  _globals['_SOURCEVARIANT']._serialized_end=6421
  _globals['_TRANSFORMATION']._serialized_start=6424
  _globals['_TRANSFORMATION']._serialized_end=6701
  _globals['_KUBERNETESRESOURCESPECS']._serialized_start=6703
  _globals['_KUBERNETESRESOURCESPECS']._serialized_end=6814
  _globals['_KUBERNETESARGS']._serialized_start=6816
  _globals['_KUBERNETESARGS']._serialized_end=6930
  _globals['_SQLTRANSFORMATION']._serialized_start=6932
  _globals['_SQLTRANSFORMATION']._serialized_end=7031
  _globals['_DFTRANSFORMATION']._serialized_start=7033
  _globals['_DFTRANSFORMATION']._serialized_end=7152
  _globals['_PRIMARYDATA']._serialized_start=7154
  _globals['_PRIMARYDATA']._serialized_end=7249
  _globals['_PRIMARYSQLTABLE']._serialized_start=7251
  _globals['_PRIMARYSQLTABLE']._serialized_end=7282
  _globals['_TAGS']._serialized_start=7284
  _globals['_TAGS']._serialized_end=7303
  _globals['_PROPERTY']._serialized_start=7305
  _globals['_PROPERTY']._serialized_end=7348
  _globals['_PROPERTIES']._serialized_start=7351
  _globals['_PROPERTIES']._serialized_end=7538
  _globals['_PROPERTIES_PROPERTYENTRY']._serialized_start=7445
  _globals['_PROPERTIES_PROPERTYENTRY']._serialized_end=7538
  _globals['_STREAMINGFEATUREVARIANT']._serialized_start=7540
  _globals['_STREAMINGFEATUREVARIANT']._serialized_end=7667
  _globals['_STREAMINGLABELVARIANT']._serialized_start=7669
  _globals['_STREAMINGLABELVARIANT']._serialized_end=7794
  _globals['_METADATA']._serialized_start=8073
  _globals['_METADATA']._serialized_end=11409
  _globals['_API']._serialized_start=11412
  _globals['_API']._serialized_end=14867
# @@protoc_insertion_point(module_scope)
