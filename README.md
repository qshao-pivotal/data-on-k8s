# data-on-k8s
Data on Kubernetes

[![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/qshao-pivotal_marketplace/qshao-pivotal%2Fdata-on-k8s%2Fdata-on-k8s?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWMxYWE4MTZlNWFiYjUwNGU1MjljNTY3.6aWX049NTXW6u_sh7DqsbusOf606eHaoVUw7wD-NHeo&type=cf-2)]( https://g.codefresh.io/pipelines/data-on-k8s/builds?repoOwner=qshao-pivotal&repoName=data-on-k8s&serviceName=qshao-pivotal%2Fdata-on-k8s&filter=trigger:build~Build;branch:master;pipeline:5c3382bfc67fe4a2d98c9cd9~data-on-k8s)

  - minio-chart-values.yaml: override default values.yaml of [Minio Helm Chart](https://github.com/helm/charts/tree/master/stable/minio)

## Installation
### Minio
```
helm install stable/minio --name qshao-minio -f chart-values/minio-chart-values.yaml
```
