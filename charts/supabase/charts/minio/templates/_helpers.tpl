{{/*
MinIO component helpers
*/}}
{{- define "minio.name" -}}
{{- default "minio" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "minio.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "minio" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-minio" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "minio.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "minio.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "minio.selectorLabels" -}}
app.kubernetes.io/name: {{ include "minio.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "minio.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "minio.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
