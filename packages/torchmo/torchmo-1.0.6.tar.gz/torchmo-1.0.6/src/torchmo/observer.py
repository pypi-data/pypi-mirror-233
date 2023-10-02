import torch
import torch.nn as nn
from itertools import islice


class ModuleObserver:
    """
    An observer class on a given module

    Parameters
    ----------
    `model` : nn.Module
        The model to watch for modules on
    `watch` : list[nn.Module] | nn.Module | str | list[str], default: []
        A module, str or a list of these elements to watch for
    `limit` : int, default: -1
        The limit number of convs to extract
    """

    def __init__(
        self,
        model: nn.Module,
        watch: list[nn.Module] | nn.Module | str | list[str] = [],
        limit: int = -1,
    ) -> None:
        super(ModuleObserver, self).__init__()
        self.watch = watch if isinstance(watch, list) else [watch]
        self.limit = limit
        self.handles = []
        self.module_observer = model
        self.outputs_ = []
        self.output_ = None
        self.names_ = []

        self.observed_modules = []
        self.observed_module_names = []
        for w in watch:

            def err():
                raise TypeError(
                    f"Watched elements should be nn.Module or str. Found {w}"
                )

            if isinstance(w, type):
                if issubclass(w, nn.Module) or isinstance(w, nn.Module):
                    self.observed_modules.append(w)
            elif isinstance(w, str):
                self.observed_module_names.append(w)
            else:
                err()

        self.__attach()

    def __attach(self):
        """
        Attache the modules to watch with a forward_hook
        """
        modules = [
            (name, module)
            for name, module in self.module_observer.named_modules()
            # Valid module to look for
            if (
                len(self.observed_modules) == 0 or type(module) in self.observed_modules
            )
            and (
                len(self.observed_module_names) == 0
                or name in self.observed_module_names
            )
        ]

        lim = self.limit if self.limit > 0 else len(modules)

        for name, conv in islice(modules, lim):
            handle = conv.register_forward_hook(self.__observe)
            self.names_.append(name)
            self.handles.append(handle)

    def __detach(self):
        for h in self.handles:
            h.remove()

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

    def __del__(self):
        self.__detach()
