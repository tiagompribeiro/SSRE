from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf

c_total = pd.read_csv("/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices.csv")
c_samsung = pd.read_csv("/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices_teste.csv")
#data = c_total.head(-1)
#print(data)
print(len(c_total.index))
tam_total = len(c_total.index)
tam_samsung = len(c_samsung.index)

c_total = "/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices.csv"
c_samsung = "/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices_teste.csv"


################################################################################
# criar raw de data
################################################################################
NAME_COLUMN = ['Label','IPLength','IPHeaderLength','TTL','Protocol','SourcePort','DestPort','SequenceNumber','AckNumber','WindowSize','TCPHeaderLength','TCPLength','TCPStream','TCPUrgentPointer','IPFlags','IPID','IPchecksum','TCPflags','TCPChecksum']
LABEL_COLUMN_NAME = 'Label'

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      column_names=NAME_COLUMN,
      label_name=LABEL_COLUMN_NAME,
      na_value="?",
      num_epochs=1,
      #num_parallel_reads ??? 
      ignore_errors=True, 
      **kwargs)
  return dataset

raw_total_data = get_dataset(c_total,batch_size=tam_total)
raw_samsung_data = get_dataset(c_samsung,batch_size=tam_samsung)

################################################################################
# show raw
################################################################################

def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

show_batch(raw_total_data)
show_batch(raw_samsung_data)


################################################################################
# start ML
################################################################################


#preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)


