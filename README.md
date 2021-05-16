# ml-microservice-example

How to run:
- Add RabbitMQ URL as `AMQP_URL` to `.env` in worker and api directories
- Python app
  ```
    conda create -n <env name> python=3.8
    conda activate <env name>
    python consumer.py
  ```
- Node app
  ```
    npm install
    node app.js
  ```
  
