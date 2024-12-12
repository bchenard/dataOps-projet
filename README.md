# dataOps-projet

## Installation

```bash
kind delete clusters --all

kind create cluster --config ./kind/config.yaml -n projet

kubectl create namespace projet

docker build -t 2024_kubernetes_post_consumer -f ./post_consumer/Dockerfile .
kind load docker-image 2024_kubernetes_post_consumer -n projet

docker build -t 2024_kubernetes_post_pusher -f ./post_pusher/Dockerfile .
kind load docker-image 2024_kubernetes_post_pusher -n projet

kubectl apply -f cours_kafka/post_consumer/deployment.yaml -n projet

kubectl apply -f cours_kafka/ui/deployment.yaml -n projet
kubectl apply -f cours_kafka/ui/service.yaml -n projet

kubectl apply -f cours_kafka/kafka/deployment.yaml -n projet
kubectl apply -f cours_kafka/kafka/service.yaml -n projet

kubectl apply -f airflow/airflow-dags-pv.yaml -n projet
kubectl apply -f airflow/airflow-dags-pvc.yaml -n projet

helm install airflow airflow-stable/airflow --version 8.9.0 --values ./airflow/custom-values.yaml --namespace projet
```