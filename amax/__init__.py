# SPDX-License-Identifier: Apache-2.0
#
# AMAX 推理作业命令行
#
# 命令面在引导期一次性定死：job 与 receipt 两组子命令。作业是本层的
# 唯一管理对象——不是模型、不是进程。命令名与退出码都是对外契约：
# 一旦有调用方依赖，改名与改码都等于违约，故从空壳起就按定稿注册，
# 未实现的路径宁可显式失败，也不预留会被误用的别名。

"""AMAX inference job command line."""

__all__ = ["VERSION"]

VERSION = "0.1.0"
