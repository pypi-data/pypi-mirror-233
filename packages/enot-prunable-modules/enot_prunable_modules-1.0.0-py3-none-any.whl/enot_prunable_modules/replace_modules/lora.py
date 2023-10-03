from typing import Union

from diffusers.models.lora import LoRACompatibleConv
from diffusers.models.lora import LoRACompatibleLinear
from diffusers.models.lora import LoRAConv2dLayer
from diffusers.models.lora import LoRALinearLayer
from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = ["LoraLinearReplacer", "LoraConvReplacer"]


class LoraLinearReplacer(Replacer):
    """
    Lora Linear module replacer.

    https://arxiv.org/abs/2106.09685

    """

    def replace(self, module: nn.Linear) -> nn.Module:
        """Replace Linear module inplace with its Lora version."""
        if isinstance(module, LoRACompatibleLinear):
            return module

        new_linear = LoRACompatibleLinear(
            in_features=module.in_features, out_features=module.out_features, bias=module.bias is not None
        )

        new_linear.bias = module.bias
        new_linear.weight = module.weight

        new_linear.set_lora_layer(
            LoRALinearLayer(
                in_features=module.in_features,
                out_features=module.out_features,
            )
        )

        setattr(new_linear, "enot_prev_linear", module)

        return new_linear

    def revert(self, module: LoRACompatibleLinear) -> nn.Module:
        """Fuse Lora layer and return previous Linear."""
        module._fuse_lora()  # pylint: disable=W0212
        if hasattr(module, "enot_prev_linear"):
            new_linear = getattr(module, "enot_prev_linear")
            delattr(module, "enot_prev_linear")

            new_linear.bias = module.bias
            new_linear.weight = module.weight

            return new_linear

        return module


class LoraConvReplacer(Replacer):
    """
    Lora Conv2d module replacer.

    https://arxiv.org/abs/2106.09685

    """

    def replace(self, module: Union[nn.Conv2d, LoRACompatibleConv]) -> nn.Module:
        """Replace Conv2d module inplace with its Lora version."""
        if isinstance(module, LoRACompatibleConv):
            return module

        new_conv = LoRACompatibleConv(
            in_channels=module.in_channels,
            out_channels=module.out_channels,
            kernel_size=module.kernel_size,
            bias=module.bias is not None,
            padding=module.padding,
            stride=module.stride,
        )

        new_conv.bias = module.bias
        new_conv.weight = module.weight

        assert isinstance(module.padding, tuple)
        new_conv.set_lora_layer(
            LoRAConv2dLayer(
                in_features=module.in_channels,
                out_features=module.out_channels,
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding[0],
            )
        )

        setattr(new_conv, "enot_prev_conv", module)

        return new_conv

    def revert(self, module: LoRACompatibleConv) -> nn.Module:
        """Fuse Lora layer and return previous Conv2d."""
        module._fuse_lora()  # pylint: disable=W0212

        if hasattr(module, "enot_prev_conv"):
            new_conv = getattr(module, "enot_prev_conv")
            delattr(module, "enot_prev_conv")

            new_conv.bias = module.bias
            new_conv.weight = module.weight

            return new_conv

        return module
