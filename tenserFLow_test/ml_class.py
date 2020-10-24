from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf


from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

c_total = pd.read_csv("/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices.csv")
c_samsung = pd.read_csv("/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices_teste.csv")
#data = c_total.head(-1)
#print(data)
#print(len(c_total.index))
tam_total = len(c_total.index)
tam_samsung = len(c_samsung.index)

#c_total = "/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices.csv"
#c_samsung = "/home/feup/Documents/IOT_catalog/prog/pcap_tensor/devices_teste.csv"


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

#raw_total_data = get_dataset(c_total,batch_size=tam_total)
#raw_samsung_data = get_dataset(c_samsung,batch_size=tam_samsung)

################################################################################
# show raw
################################################################################

def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

#show_batch(raw_total_data)
#show_batch(raw_samsung_data)


################################################################################
# start ML
################################################################################


#preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)


# In the original dataset "4" indicates the pet was not adopted.
c_total['target'] = np.where(c_total['Label']=="y",0,1)
c_total = c_total.drop(columns=['Label'])
#c_samsung = c_samsung.drop(columns=['Label'])

train, test = train_test_split(c_total, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print(len(train), 'train examples')
print(len(val), 'validation examples')
print(len(test), 'test examples')



# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('target')
  dataframe = np.asarray(dataframe).astype('float32')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds


batch_size = 5 # A small batch sized is used for demonstration purposes
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)


