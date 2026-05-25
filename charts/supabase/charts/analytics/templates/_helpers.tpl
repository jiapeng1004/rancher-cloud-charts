{{/*
Analytics component helpers
*/}}
{{- define "analytics.name" -}}
{{- default "analytics" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "analytics.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "analytics" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-analytics" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "analytics.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "analytics.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "analytics.selectorLabels" -}}
app.kubernetes.io/name: {{ include "analytics.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "analytics.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "analytics.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
