{{/*
  Ingress apiVersion：按集群版本选择 networking.k8s.io/v1 / v1beta1 / extensions/v1beta1。
  用法示例：
    apiVersion: {{ include "rancher-lib.ingress.apiVersion" . }}

  刻意写成单一 define，避免多层 define/include 嵌套。
*/}}
{{- define "rancher-lib.ingress.apiVersion" -}}
{{- $v := default .Capabilities.KubeVersion.Version .Capabilities.KubeVersion.GitVersion -}}
{{- if semverCompare ">=1.19-0" $v -}}
networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0 <1.22-0" $v -}}
networking.k8s.io/v1beta1
{{- else -}}
extensions/v1beta1
{{- end -}}
{{- end -}}
