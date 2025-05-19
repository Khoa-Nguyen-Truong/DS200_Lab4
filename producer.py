from kafka import KafkaProducer
import pickle
import numpy as np
import json
import time
import os
from datetime import datetime

# Kafka configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    client_id='cifar10-producer'
)

# Kafka topic
topic = 'cifar10-stream'

def load_cifar10_batch(file_path):
    """Load a CIFAR-10 batch file"""
    with open(file_path, 'rb') as f:
        batch = pickle.load(f, encoding='bytes')
    data = batch[b'data'].astype(np.float32) / 255.0  # Normalize to [0, 1]
    labels = np.array(batch[b'labels'])
    return data, labels

def generate_cifar10_data(data_dir='data', batch_size=100):
    """Generate data from CIFAR-10 batch files in batches"""
    batch_files = [f'data_batch_{i}' for i in range(1, 6)]
    for batch_file in batch_files:
        file_path = os.path.join(data_dir, batch_file)
        if os.path.exists(file_path):
            data, labels = load_cifar10_batch(file_path)
            for i in range(0, len(data), batch_size):
                batch_data = data[i:i + batch_size]
                batch_labels = labels[i:i + batch_size]
                batch_samples = [
                    {
                        'image': batch_data[j].tolist(),  # 3072-dimensional vector
                        'label': int(batch_labels[j])
                    }
                    for j in range(len(batch_data))
                ]
                yield batch_samples
        else:
            print(f'File not found: {file_path}')

def main():
    print("Starting Kafka producer...")
    try:
        for batch_samples in generate_cifar10_data(batch_size=100):
            # Send each sample in the batch to Kafka topic
            for sample in batch_samples:
                producer.send(topic, value=sample)
            producer.flush()
            # Print notification for the batch
            print(f"Sent batch of {len(batch_samples)} samples at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(10)  # Simulate real-time streaming between batches
        producer.flush()
    except KeyboardInterrupt:
        print("Producer interrupted.")
    finally:
        producer.flush()
        producer.close()
        print("Producer stopped.")

if __name__ == "__main__":
    main()