{{/*
Meta component helpers
*/}}
{{- define "meta.name" -}}
{{- default "meta" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "meta.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "meta" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-meta" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "meta.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "meta.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "meta.selectorLabels" -}}
app.kubernetes.io/name: {{ include "meta.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "meta.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "meta.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
