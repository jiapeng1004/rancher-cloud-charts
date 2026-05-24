{{/*
显式将 values.environment.auth 中的固定键注入 GoTrue（避免对 map 盲 range，便于审查与顺序稳定）。
新增标准变量：同时改 values.yaml 与本文件。
实验性 / 临时变量：放在 environment.auth.extra（map），在文件末尾统一 range。
*/}}
{{- define "supabase.auth.envFromValues" -}}
{{- $a := .root.Values.environment.auth }}
- name: DB_USER
  value: {{ $a.DB_USER | quote }}
- name: DB_DRIVER
  value: {{ $a.DB_DRIVER | quote }}
- name: DB_SSL
  value: {{ $a.DB_SSL | quote }}
- name: API_EXTERNAL_URL
  value: {{ $a.API_EXTERNAL_URL | quote }}
- name: GOTRUE_API_HOST
  value: {{ $a.GOTRUE_API_HOST | quote }}
- name: GOTRUE_API_PORT
  value: {{ $a.GOTRUE_API_PORT | quote }}
- name: GOTRUE_SITE_URL
  value: {{ $a.GOTRUE_SITE_URL | quote }}
- name: GOTRUE_URI_ALLOW_LIST
  value: {{ $a.GOTRUE_URI_ALLOW_LIST | quote }}
- name: GOTRUE_DISABLE_SIGNUP
  value: {{ $a.GOTRUE_DISABLE_SIGNUP | quote }}
- name: GOTRUE_JWT_DEFAULT_GROUP_NAME
  value: {{ $a.GOTRUE_JWT_DEFAULT_GROUP_NAME | quote }}
- name: GOTRUE_JWT_ADMIN_ROLES
  value: {{ $a.GOTRUE_JWT_ADMIN_ROLES | quote }}
- name: GOTRUE_JWT_AUD
  value: {{ $a.GOTRUE_JWT_AUD | quote }}
- name: GOTRUE_JWT_EXP
  value: {{ $a.GOTRUE_JWT_EXP | quote }}
- name: GOTRUE_EXTERNAL_EMAIL_ENABLED
  value: {{ $a.GOTRUE_EXTERNAL_EMAIL_ENABLED | quote }}
- name: GOTRUE_MAILER_AUTOCONFIRM
  value: {{ $a.GOTRUE_MAILER_AUTOCONFIRM | quote }}
- name: GOTRUE_EXTERNAL_ANONYMOUS_USERS_ENABLED
  value: {{ $a.GOTRUE_EXTERNAL_ANONYMOUS_USERS_ENABLED | quote }}
- name: GOTRUE_SMTP_ADMIN_EMAIL
  value: {{ $a.GOTRUE_SMTP_ADMIN_EMAIL | quote }}
- name: GOTRUE_SMTP_HOST
  value: {{ $a.GOTRUE_SMTP_HOST | quote }}
- name: GOTRUE_SMTP_PORT
  value: {{ $a.GOTRUE_SMTP_PORT | quote }}
- name: GOTRUE_EXTERNAL_PHONE_ENABLED
  value: {{ $a.GOTRUE_EXTERNAL_PHONE_ENABLED | quote }}
- name: GOTRUE_SMS_AUTOCONFIRM
  value: {{ $a.GOTRUE_SMS_AUTOCONFIRM | quote }}
- name: GOTRUE_SMTP_SENDER_NAME
  value: {{ $a.GOTRUE_SMTP_SENDER_NAME | quote }}
- name: GOTRUE_MAILER_URLPATHS_INVITE
  value: {{ $a.GOTRUE_MAILER_URLPATHS_INVITE | quote }}
- name: GOTRUE_MAILER_URLPATHS_CONFIRMATION
  value: {{ $a.GOTRUE_MAILER_URLPATHS_CONFIRMATION | quote }}
- name: GOTRUE_MAILER_URLPATHS_RECOVERY
  value: {{ $a.GOTRUE_MAILER_URLPATHS_RECOVERY | quote }}
- name: GOTRUE_MAILER_URLPATHS_EMAIL_CHANGE
  value: {{ $a.GOTRUE_MAILER_URLPATHS_EMAIL_CHANGE | quote }}
{{- range $k, $v := ($a.extra | default dict) }}
- name: {{ $k }}
  value: {{ $v | quote }}
{{- end }}
{{- end }}
