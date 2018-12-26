# data-platform-on-k8s
Data Platform on Kubernetes

- chart-values [![Codefresh build status]( https://g.codefresh.io/api/badges/pipeline/qshao-pivotal_marketplace/qshao-pivotal%2Fdata-platform-on-k8s%2Fchart-values?branch=master&key=eyJhbGciOiJIUzI1NiJ9.NWMxYWE4MTZlNWFiYjUwNGU1MjljNTY3.6aWX049NTXW6u_sh7DqsbusOf606eHaoVUw7wD-NHeo&type=cf-2)]( https://g.codefresh.io/pipelines/chart-values/builds?repoOwner=qshao-pivotal&repoName=data-platform-on-k8s&serviceName=qshao-pivotal%2Fdata-platform-on-k8s&filter=trigger:build~Build;branch:master;pipeline:5c2358b1ada6ff7be6fd4884~chart-values)

  - minio-chart-values.yaml: override default values.yaml of [Minio Helm Chart](https://github.com/helm/charts/tree/master/stable/minio)

## Installation
### Minio
```
helm install stable/minio --name qshao-minio -f chart-values/minio-chart-values.yaml
```