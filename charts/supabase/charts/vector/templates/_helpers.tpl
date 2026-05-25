{{/*
Vector component helpers
*/}}
{{- define "vector.name" -}}
{{- default "vector" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "vector.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "vector" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-vector" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "vector.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "vector.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "vector.selectorLabels" -}}
app.kubernetes.io/name: {{ include "vector.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "vector.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "vector.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
