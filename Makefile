# 原则：helm 打包只用 helm + shell；批量维护才用 scripts/*.py（make icons / questions）
.DEFAULT_GOAL := help

HELM_OUT ?= .helm-packages
HELM_URL ?= https://jiapeng1004.github.io/rancher-cloud-charts

.PHONY: help helm-package icons questions

help:
	@echo "常用："
	@echo "  make helm-package   打包 charts -> $(HELM_OUT)（helm + shell，与 CI 相同）"
	@echo ""
	@echo "批量维护（Python，一般不常跑）："
	@echo "  make icons          写回全部 Chart.yaml icon"
	@echo "  make questions      sync Rancher questions.yaml"

helm-package:
	rm -rf $(HELM_OUT) && mkdir -p $(HELM_OUT)
	@set -e; \
	count=0; \
	for chart in $$(find charts -name Chart.yaml | sort); do \
	  dir=$$(dirname "$$chart"); \
	  rel="$${dir#charts/}"; \
	  echo "$$rel" | grep -q '/charts/' && continue; \
	  echo "[pack] $$dir"; \
	  helm dependency build "$$dir" 2>/dev/null || true; \
	  helm package "$$dir" -d $(HELM_OUT); \
	  count=$$((count + 1)); \
	done; \
	test "$$count" -gt 0; \
	helm repo index $(HELM_OUT) --url $(HELM_URL); \
	index="$(HELM_OUT)/index.yaml"; \
	{ printf '\357\273\277'; cat "$$index"; } > "$$index.tmp" && mv "$$index.tmp" "$$index"; \
	touch $(HELM_OUT)/.nojekyll; \
	echo "done: $$count chart(s) -> $(HELM_OUT)"

icons:
	python3 scripts/apply_chart_icons.py

questions:
	python3 scripts/sync_rancher_questions.py
