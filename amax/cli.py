# SPDX-License-Identifier: Apache-2.0
#
# AMAX 命令行入口
#
# 四条路径对应作业生命周期的四个动作：submit 提交、status 查询、
# resume 接续、receipt verify 离线复核。退出码与 airyllm 同源
# （0 就绪、1 失败、10 降级），调用方可以用同一套脚本编排两层。
#
# 全部叶子当前显式报 not-implemented 并以 1 退出。命令面先于实现
# 注册，是为了让调用方与脚本从第一天起绑定稳定契约；拿「路径不存
# 在」当错误码等于把契约变化伪装成故障。resume 依赖 AirymaxRT 的
# 检查点（supervisor_d 尚只有重启、无状态恢复），不得在实现落地
# 前暗示「不重 prefill」的能力。

"""AMAX command line surface (job / receipt)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import VERSION

__all__ = ["EXIT_DEGRADED", "EXIT_FAIL", "EXIT_OK", "main"]

EXIT_OK = 0

EXIT_FAIL = 1

EXIT_DEGRADED = 10


def main(argv: Sequence[str] | None = None) -> int:
    """解析命令行并分派；返回值即进程退出码。"""
    args = _args(argv)
    return args.func(args)


def _args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="amax",
        description="AMAX 推理作业命令行（作业与凭证接口）",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"amax {VERSION}",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    job = sub.add_parser("job", help="提交与查询推理作业")
    job_sub = job.add_subparsers(dest="action", required=True)
    submit = job_sub.add_parser("submit", help="按 job.yaml 提交推理作业")
    submit.add_argument("file", metavar="FILE", help="作业描述 job.yaml")
    submit.set_defaults(func=_submit)
    status = job_sub.add_parser("status", help="查询作业状态")
    status.add_argument("job", metavar="JOB", nargs="?", help="作业标识")
    status.set_defaults(func=_status)
    resume = job_sub.add_parser("resume", help="从中断点接续作业")
    resume.add_argument("job", metavar="JOB", help="作业标识")
    resume.set_defaults(func=_resume)

    receipt = sub.add_parser("receipt", help="作业凭证的离线复核")
    receipt_sub = receipt.add_subparsers(dest="action", required=True)
    verify = receipt_sub.add_parser("verify", help="离线复核 receipt.json")
    verify.add_argument("file", metavar="FILE", help="凭证 receipt.json")
    verify.set_defaults(func=_verify)

    return parser.parse_args(argv)


def _submit(args: argparse.Namespace) -> int:
    return _pending("job submit", "job.yaml 校验与判定链接入待接")


def _status(args: argparse.Namespace) -> int:
    return _pending("job status", "作业状态存储待接")


def _resume(args: argparse.Namespace) -> int:
    return _pending("job resume", "依赖 AirymaxRT 检查点，尚未交付")


def _verify(args: argparse.Namespace) -> int:
    return _pending("receipt verify", "receipt 组装待接（判定链骨架在 airyllm）")


def _pending(path: str, why: str) -> int:
    """未实现路径的统一出口：固定 token 落 stderr，退出码 1。"""
    print(f"amax: {path}: not-implemented: {why}", file=sys.stderr)
    return EXIT_FAIL
