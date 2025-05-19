# CIFAR-10 Real-Time Streaming with Kafka

This repository implements a real-time data streaming pipeline for the CIFAR-10 dataset using Kafka. The producer streams CIFAR-10 data in batches of 100 samples, while the consumer trains an online `PassiveAggressiveClassifier` model incrementally using scikit-learn. Notifications are provided for each batch processed by both producer and consumer.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Khoa-Nguyen-Truong/DS200_Lab4.git
   cd DS200_Lab4
   ```
2. Set up a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start Kafka server:
   ```bash
   bin\windows\kafka-server-start.bat config\server.properties
   ```
5. Creat Kafka topic
   ```bash
   bin\windows\kafka-topics.bat --create --topic cifar10-stream --bootstrap-server localhost:9092
   ```
## Usage
1. Start the consumer:
   ```bash
   python consumer.py
   ```
2. In a separate terminal, start the producer:
   ```bash
   python producer.py
   ```

## Project Structure
```
D:\Khoa\University\3rdYear\BigData\
├── Lab4\
│   ├── consumer.py        # Kafka consumer, trains model on batches
│   ├── producer.py        # Kafka producer, streams CIFAR-10 batches
│   ├── models\
│       ├── pac.py           #PassiveAggressiveClassifier
│   ├── requirements.txt   # Dependency list
│   └── README.md          # This file
└── data\   # CIFAR-10 dataset (data_batch_1 to data_batch_5)
```
## License
This project is licensed under the [Apache-2.0 license](LICENSE).