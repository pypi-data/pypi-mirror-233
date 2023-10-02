import torch
import torch.nn as nn


class ModuleObserver(nn.Module):
    """
    An observer class on a given module

    Parameters
    ----------
    `model` : nn.Module
        The model to watch for modules on
    `watch` : list[nn.Module] | nn.Module, default: []
        A module or a list of modules to watch for
    """

    def __init__(
        self, model: nn.Module, watch: list[nn.Module] | nn.Module = [], *args, **kwargs
    ) -> None:
        super(ModuleObserver, self).__init__(*args, **kwargs)
        self.watch = watch if isinstance(watch, list) else [watch]
        self.handles = []
        self.module_observer = model
        self.outputs_ = []
        self.output_ = None
        self.names_ = []

        self.__attach()

    def __attach(self):
        """
        Attache the modules to watch with a forward_hook
        """

        for name, conv in [
            (name, module)
            for name, module in self.module_observer.named_modules()
            if type(module) in self.watch
        ]:
            handle = conv.register_forward_hook(self.__observe)
            self.names_.append(name)
            self.handles.append(handle)

    def __observe(self, module: nn.Module, input: torch.Tensor, output: torch.Tensor):
        self.outputs_.append(output)

    def outputs(self) -> list[torch.Tensor]:
        """
        The feature outputs from the convlayers
        """
        return self.outputs_

    def output(self):
        """
        The model's real output
        """
        return self.output_

    def forward(self, *args):
        self.outputs_ = []
        self.output_ = self.module_observer(*args)
        return zip(self.names_, self.outputs())

    def __call__(self, *args) -> list[tuple[str, torch.Tensor]]:
        return self.forward(*args)
