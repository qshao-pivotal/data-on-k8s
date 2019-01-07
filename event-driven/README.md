# Event Driven

## chart-values
  - minio-chart-values.yaml: override default values.yaml of [Minio Helm Chart](https://github.com/helm/charts/tree/master/stable/minio)
  - confluent-chart-values.yaml: override default values.yaml of [Confluent Helm Chart](https://github.com/confluentinc/cp-helm-charts)
## Installation
### Minio
```
helm install stable/minio --name event-driven-minio -f ./chart-values/minio-chart-values.yaml
```
### Confluent Kafka
```
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update
helm install confluentinc/cp-helm-charts --name event-driven-confluent -f ./chart-values/confluent-chart-values.yaml
```