# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\x12\x04\x64\x61ta\"*\n\x07Request\x12\x11\n\tclient_id\x18\x01 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"+\n\x08Response\x12\x11\n\tserver_id\x18\x01 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x32{\n\x08GRPCDemo\x12\x41\n\x1c\x42idirectionalStreamingMethod\x12\r.data.Request\x1a\x0e.data.Response(\x01\x30\x01\x12,\n\x0bUnaryMethod\x12\r.data.Request\x1a\x0e.data.Responseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST._serialized_start=20
  _REQUEST._serialized_end=62
  _RESPONSE._serialized_start=64
  _RESPONSE._serialized_end=107
  _GRPCDEMO._serialized_start=109
  _GRPCDEMO._serialized_end=232
# @@protoc_insertion_point(module_scope)
