from kafka import KafkaConsumer
from models.pac import PAC
import json
import numpy as np
from datetime import datetime

# Kafka configuration
topic = 'cifar10-stream'
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    group_id='cifar10-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize model
model = PAC()

# Batch configuration
batch_size = 100
batch_samples = []
batch_count = 0
total_samples = 0

def main():
    print("Starting Kafka consumer...")
    try:
        for msg in consumer:
            sample = msg.value
            batch_samples.append(sample)
            
            # Process batch when enough samples are collected
            if len(batch_samples) >= batch_size:
                global batch_count, total_samples
                batch_count += 1
                total_samples += len(batch_samples)
                
                # Convert batch to NumPy arrays
                try:
                    X = np.array([s['image'] for s in batch_samples]).reshape(-1, 3072)
                    y = np.array([s['label'] for s in batch_samples])
                    
                    # Print notification before training
                    print(f"Training batch #{batch_count} of {len(batch_samples)} samples (total: {total_samples}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Train model
                    predictions, accuracy, precision, recall, f1 = model.train(X, y)
                    
                    # Print performance metrics
                    print(f"Completed training batch #{batch_count} with {len(batch_samples)} samples.")
                    print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")
                    
                    # Clear batch
                    batch_samples.clear()
                except Exception as e:
                    print(f"Error processing batch: {e}")
                    
    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        consumer.close()
        print("Consumer stopped.")

if __name__ == "__main__":
    main()