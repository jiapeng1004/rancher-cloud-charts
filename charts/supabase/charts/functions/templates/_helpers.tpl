{{/*
Functions component helpers
*/}}
{{- define "functions.name" -}}
{{- default "functions" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "functions.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "functions" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-functions" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "functions.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "functions.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "functions.selectorLabels" -}}
app.kubernetes.io/name: {{ include "functions.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "functions.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "functions.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
