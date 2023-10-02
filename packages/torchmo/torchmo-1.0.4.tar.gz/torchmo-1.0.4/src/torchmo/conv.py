from pathlib import Path
import torch
import torch.nn as nn
from torchmo.observer import ModuleObserver
import matplotlib.pyplot as plt
from tqdm import tqdm


class ConvObserver(ModuleObserver):
    """
    An observer class for nn.Conv2d

    Parameters
    ----------
    `model` : nn.Module
        The model to watch for modules on
    `watch` : str | list[str], default: []
        A str or a list str conv modules to watch for
    `limit` : int, default: -1
        The limit number of convs to extract
    See also
    ----------
    ModuleObserver
    """

    def __init__(
        self,
        model: nn.Module,
        watch: str | list[str] = [],
        limit: int = -1,
        *args,
        **kwargs,
    ) -> None:
        super(ConvObserver, self).__init__(
            model,
            [nn.Conv2d, *(watch if isinstance(watch, list) else [watch])],
            limit,
            *args,
            **kwargs,
        )

    def __get_fig(self, output: torch.Tensor):
        """
        Get the figure for an output item
        """

        C, H, W = output.shape

        C_f = C**0.5

        rows = int(C_f) if C_f == int(C_f) else int(C_f) + 1
        cols = int(C_f)

        output = output.detach().numpy()

        fig, axs = plt.subplots(
            rows,
            cols,
            figsize=(14, 14),
            gridspec_kw={
                "wspace": 0,
                "hspace": 0,
                "left": 0,
                "bottom": 0,
                "top": 1,
                "right": 1,
            },
        )

        for ax in axs.flatten():
            ax.grid(False)
            ax.set_xticks([])
            ax.set_yticks([])

        for ax, feature in zip(axs.flatten(), output):
            ax.imshow(feature, cmap="gray")

        return fig

    def save_figs(self, path: str | Path, progress=True):
        """
        Save each Conv2d features to an image at the specified
        path.

        Parameters
        ----------
        `path`: str | Path
            The path for where to output the feature maps
        `progress`: bool, default: `True`
            Weither to show a tqdm loading bar
        """
        path = Path(path)

        for name, batch in tqdm(
            zip(self.names_, self.outputs_),
            disable=not progress,
            total=len(self.names_),
        ):
            for idx, output in enumerate(batch):
                batch_p = path / f"batch_{idx}"
                batch_p.mkdir(exist_ok=True)

                fig = self.__get_fig(output)
                fig.savefig(batch_p / f"{name}.jpg")
