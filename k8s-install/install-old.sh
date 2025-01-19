#!/bin/bash
# 获取系统包管理apt/yum
function getAppManager() {
  if grep < /etc/os-release -i "debian" > /dev/null; then
    echo "apt"
  elif grep < /etc/os-release -i "deepin" > /dev/null; then
    echo "apt"
  elif grep < /etc/os-release -i "ubuntu" > /dev/null; then
    echo "yum"
  else
    echo "不支持的操作系统" >&2
    exit 1
  fi
}
#获取系统类型
function getSystemType() {
  if grep < /etc/os-release-i "deepin" > /dev/null; then
    echo "deepin"
  else
    #echo 包管理器
    appManager=$(getAppManager)
    echo "$appManager"
  fi
}
# 安装docker
function requireDocker() {
    # 测试docker命令是否存在
    docker > /dev/null 2>&1
    if [ $? -eq 127 ]; then
        echo "docker未安装，开始安装"
        packageList=()
        systemType=$(getSystemType)
        if [ "$systemType" = "deepin" ]; then
          packageList+=("docker.io")
        elif [ "$systemType" = "apt" ]; then
          packageList+=("docker-ce")
          packageList+=("docker-ce-cli")
        elif [ "$systemType" = "yum" ]; then
          packageList+=("docker-ce")
          packageList+=("docker-ce-cli")
        fi
        appManager=$(getAppManager)
        eval "$appManager install ${packageList[*]} -y"
    fi
}

# docker换源
function dockerInit() {
    # 如果文件本就存在则直接返回0
    if [ -f /etc/docker/daemon.json ]; then
        return 0
    fi
    touch /etc/docker/daemon.json
    cat > /etc/docker/daemon.json << EOF
{
      "features": {
        "buildkit": true
      },
      "registry-mirrors": [
                "https://docker.1ms.run",
                "https://docker.xuanyuan.me"
        ]
}
EOF
}
# 主函数
function main() {
    requireDocker
    dockerInit
    docker run -itd --name test  --rm --entrypoint=bash --privileged rancher/rancher:v2.4.17
    mkdir -p /var/lib/rancher
    docker cp test:/var/lib/rancher /var/lib/rancher
    docker rm -f test
    curl https://gitee.com/jiapengCode/rancher-cloud-charts/raw/master/k8s-install/ssl.tar -o ./ssl.tar
    tar -zxvf ssl.tar -C /opt
    docker run -itd --name rancher --restart unless-stopped -p 9080:80 -p 9443:443 -e CATTLE_SYSTEM_DEFAULT_REGISTRY=docker.xuanyuan.me -e CATTLE_BOOTSTRAP_PASSWORD=123456  -v /opt/ssl:/etc/rancher/ssl -v /var/lib/rancher:/var/lib/rancher --privileged rancher/rancher:v2.4.17
    echo "127.0.0.1 lc.jiapeng.icu" >> /etc/hosts
    SEALOS_VERSION=5.0.1
    curl -sfL https://mirror.ghproxy.com/https://raw.githubusercontent.com/labring/sealos/main/scripts/install.sh | PROXY_PREFIX=https://mirror.ghproxy.com sh -s ${SEALOS_VERSION} labring/sealos
    SEALOS_NAME=lc
    sealos run registry.cn-shanghai.aliyuncs.com/labring/kubernetes-docker:v1.18.18 registry.cn-shanghai.aliyuncs.com/labring/helm:v3.9.4 registry.cn-shanghai.aliyuncs.com/labring/cilium:v1.12.0 \
         --masters "master.$SEALOS_NAME"  771314
}
main "$@"

