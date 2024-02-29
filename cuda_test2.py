import tensorflow as tf

# Check if CUDA GPUs are available
gpus = tf.config.list_physical_devices('GPU')
is_cuda_available = len(gpus) > 0

print(f"CUDA available: {is_cuda_available}")

# Print details about the GPUs
if is_cuda_available:
    for gpu in gpus:
        print(gpu)

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    print("We got a GPU")
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
else:
    print("Sorry, no GPU for you...")
