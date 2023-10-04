"""
"""
# pyright: reportPrivateImportUsage=false

from __future__ import annotations

import importlib
from contextlib import contextmanager
from ctypes import CDLL
from typing import TYPE_CHECKING, Any
from typing import Tuple

if TYPE_CHECKING:
    import torch as Torch

try:
    import torch
except ImportError:
    torch = None


@contextmanager
def cuda_unavailable():
    assert torch
    _is_available = torch.cuda.is_available
    torch.cuda.is_available = lambda: False
    yield
    torch.cuda.is_available = _is_available


if torch:
    with cuda_unavailable():
        try:
            import bitsandbytes as bnb
        except ImportError:
            bnb = None
else:
    bnb = None


if torch and bnb:

    with cuda_unavailable():
        from bitsandbytes import cextension
        from bitsandbytes import functional
        from bitsandbytes.cuda_setup.main import CUDASetup
        from bitsandbytes.nn import Int8Params

    _param_to   = Int8Params.to     # type: ignore
    _param_cuda = Int8Params.cuda

    TensorToArgs = Tuple[torch.device, torch.dtype, bool, torch.memory_format]

    to_ops: list[tuple[Int8Params, TensorToArgs]] = []
    cuda_ops: list[Int8Params] = []

    def _to_op_register(self: Int8Params, *args, **kwargs):
        parsed = torch._C._nn._parse_to(*args, **kwargs)
        device, *_ = parsed
        if not isinstance(device, torch.device): # pragma: no cover
            return _param_to(self, *args, **kwargs)
        if device.type != 'cuda':
            return _param_to(self, *args, **kwargs)
        to_ops.append((self, parsed))
        return self

    def _cuda_op_arg_check(device: Torch.device | int | str | None) -> bool:
        if device is None: # pragma: no cover
            return True
        if isinstance(device, int):
            return True
        if isinstance(device, str): # pragma: no cover
            device = torch.device(device)
        return device.type == 'cuda' # pragma: no cover

    def _cuda_op_register(self: Int8Params, device: Torch.device | int | str | None = None, **kwargs):
        if not _cuda_op_arg_check(device): # pragma: no cover
            # Let PyTorch handle the fail
            return _param_cuda(self, device, **kwargs)
        cuda_ops.append(self)
        return self

    def _patch():
        Int8Params.to   = _to_op_register   # type: ignore
        Int8Params.cuda = _cuda_op_register # type: ignore

    def _unpatch():
        Int8Params.to   = _param_to   # type: ignore
        Int8Params.cuda = _param_cuda

    def _move():
        CUDASetup._instance = None
        importlib.reload(cextension)
        functional.lib = cextension.lib
        for op in to_ops:
            tensor, parsed_args = op
            _, dtype, _, memory_format = parsed_args
            tensor.data = _param_to(tensor,
                device='cuda',
                dtype=dtype,
                memory_format=memory_format,
            ) # type: ignore
        for op in cuda_ops:
            tensor = op
            tensor.data = _param_cuda(tensor, torch.device('cuda', index=0))

else:

    _patch = lambda: None
    _unpatch = lambda: None
    _move = lambda: None


patch = _patch
unpatch = _unpatch
move = _move
