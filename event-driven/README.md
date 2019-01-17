# Event Driven [![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/qshao-pivotal_marketplace/qshao-pivotal%2Fdata-on-k8s%2Fdata-on-k8s?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWMxYWE4MTZlNWFiYjUwNGU1MjljNTY3.6aWX049NTXW6u_sh7DqsbusOf606eHaoVUw7wD-NHeo&type=cf-2)]( https://g.codefresh.io/pipelines/data-on-k8s/builds?repoOwner=qshao-pivotal&repoName=data-on-k8s&serviceName=qshao-pivotal%2Fdata-on-k8s&filter=trigger:build~Build;branch:master;pipeline:5c3382bfc67fe4a2d98c9cd9~data-on-k8s)

## Architecture
![](event-driven-architecture.png)
## chart-values
  - minio-chart-values.yaml: override default values.yaml of [Minio Helm Chart](https://github.com/helm/charts/tree/master/stable/minio)
  - confluent-chart-values.yaml: override default values.yaml of [Confluent Helm Chart](https://github.com/confluentinc/cp-helm-charts)
## Setup
### 1. Install Confluent Kafka
Install a 3 nodes Zookeeper and 3 nodes Kafka cluster with a proper size config
```
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update
helm install confluentinc/cp-helm-charts --name event-driven-confluent -f ./chart-values/confluent-chart-values.yaml
```
### 2. Install Minio
Config Minio Notification desitination with Kafka info in [minio-chart-values.yaml](chart-values/minio-chart-values.yaml)
```
helm install stable/minio --name event-driven-minio -f ./chart-values/minio-chart-values.yaml --version 2.3.0
```
### 3. Install MongoDB
```
helm install stable/mongodb --name event-driven-mongodb -f ./chart-values/mongodb-chart-values.yaml
```
### 4. Create buckets, topic and event notification
```
kubectl apply -f ./setup.yaml
```
This Kubernetes Job contains:
  - Create `images-bucket-event` topic in Kafka
  - Create `thumbnails-event` topic in Kafka
  - Create `images` and `thumbnails` buckets in Minio
  - Create event notification for `images` bucket to publish `put` event to `images-bucjet-event` topic in Kafka