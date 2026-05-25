{{/*
Rest component helpers
*/}}
{{- define "rest.name" -}}
{{- default "rest" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "rest.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "rest" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-rest" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "rest.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "rest.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "rest.selectorLabels" -}}
app.kubernetes.io/name: {{ include "rest.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "rest.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "rest.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
