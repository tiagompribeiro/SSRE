from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import os
import glob
import pandas as pd
import numpy as np
import tensorflow as tf

total = pd.read_csv("../pcap_tensor/lable_feature_IOT.csv")

#data = total.head(-1)
#print(data)
#print(len(total.index))

################################################################################
# criar raw de data
################################################################################
NAME_COLUMN = ['Label','IPLength','IPHeaderLength','TTL','Protocol','SourcePort','DestPort','SequenceNumber','AckNumber','WindowSize','TCPHeaderLength','TCPLength','TCPStream','TCPUrgentPointer','IPFlags','IPID','IPchecksum','TCPflags','TCPChecksum']
LABEL_COLUMN_NAME = 'Label'

def get_dataset(file_path, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size=len(file_path.index), # nº de linhas
      column_names=NAME_COLUMN,
      label_name=LABEL_COLUMN_NAME,
      na_value="?",
      num_epochs=1,
      #num_parallel_reads ??? 
      ignore_errors=True, 
      **kwargs)
  return dataset

raw_total_data = get_dataset (total)

################################################################################
# Seprar da Data total em data de treino e teste
################################################################################

