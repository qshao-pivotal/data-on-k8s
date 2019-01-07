# Event Driven

## chart-values
  - minio-chart-values.yaml: override default values.yaml of [Minio Helm Chart](https://github.com/helm/charts/tree/master/stable/minio)

## Installation
### Minio
```
helm install stable/minio --name qshao-minio -f chart-values/minio-chart-values.yaml
```
