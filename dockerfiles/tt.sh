#!/bin/sh

if [ $app == '/' ]; then
	return 0
fi

if [ $k8s_cluster == 'esxi_dev' ]; then
	kubectl config use-context kubernetes-admin@kubernetes
else if [ $k8s_cluster == '/' ]; then
	return 0
else
	return 1
fi
