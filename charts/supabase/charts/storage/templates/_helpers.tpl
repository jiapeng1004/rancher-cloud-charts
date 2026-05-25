{{/*
Storage component helpers
*/}}
{{- define "storage.name" -}}
{{- default "storage" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "storage.fullname" -}}
{{- if .Values.fullnameOverride }}{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}{{- $name := default "storage" .Values.nameOverride }}{{- if contains $name .Release.Name }}{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}{{- printf "%s-storage" .Release.Name | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}
{{- end }}
{{- define "storage.labels" -}}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{ include "storage.selectorLabels" . | indent 0 }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
{{- define "storage.selectorLabels" -}}
app.kubernetes.io/name: {{ include "storage.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
{{- define "storage.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}{{- default (include "storage.fullname" .) .Values.serviceAccount.name }}
{{- else }}{{- default "default" .Values.serviceAccount.name }}{{- end }}
{{- end }}
