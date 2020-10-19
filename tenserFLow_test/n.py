import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

print("\n------------------------------------------------------------------------------------------------------------------------------\n")
tf.test.is_gpu_available()
