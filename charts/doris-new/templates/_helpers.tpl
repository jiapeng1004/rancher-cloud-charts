{{/*
Expand the name of the chart.
*/}}
{{- define "doris.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "doris.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
FE full name
*/}}
{{- define "doris.fe.fullname" -}}
{{- printf "%s-fe" (include "doris.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
BE full name
*/}}
{{- define "doris.be.fullname" -}}
{{- printf "%s-be" (include "doris.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "doris.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "doris.labels" -}}
helm.sh/chart: {{ include "doris.chart" . }}
{{ include "doris.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "doris.selectorLabels" -}}
app.kubernetes.io/name: {{ include "doris.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
FE selector labels
*/}}
{{- define "doris.fe.selectorLabels" -}}
{{ include "doris.selectorLabels" . }}
component: fe
{{- end }}

{{/*
BE selector labels
*/}}
{{- define "doris.be.selectorLabels" -}}
{{ include "doris.selectorLabels" . }}
component: be
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "doris.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "doris.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
