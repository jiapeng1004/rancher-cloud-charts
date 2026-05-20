WordPress 使用 **官方 `wordpress:*-apache`** 镜像，通过环境变量连接 **已有 MySQL/MariaDB**。

`wordpress.db.password` 仅作演示，**生产务必**用 SealedSecrets / ExternalSecrets 等方式管理。
