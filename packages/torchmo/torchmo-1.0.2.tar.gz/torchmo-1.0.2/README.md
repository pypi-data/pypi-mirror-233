# Torch-Module-Observer

Torch-Module-Observer is a tool that uses the internal torch hook functionnalities to provide an API to observe on a model's `nn.Module`s.

Here is an example with a ConvObserver, but this tool can be used to **observe any module**, not only Convs.

![image of dog](https://github.com/AlanBlanchet/torch-module-observer/blob/master/images/dog.jpg?raw=true)

Extract features :

<div style="width:100%;height:400px;display:flex;align-items:center">
    <div style="display:flex;flex-direction:column;align-items:center">
        <img src="https://github.com/AlanBlanchet/torch-module-observer/blob/master/images/conv1.jpg?raw=true"/>
        <label>First layer</label>
    </div>
    <div style="margin:10px;white-space:nowrap">--------------></div>
    <div style="display:flex;flex-direction:column;align-items:center">
        <img src="https://github.com/AlanBlanchet/torch-module-observer/blob/master/images/layer4.1.conv2.jpg?raw=true"/>
        <label>Last layer</label>
    </div>
</div>

## Installation

```bash
pip install torchmo
```

This package also works with conda and poetry.

## Use

```python
from torchmo import ConvObserver

model = ... # nn.Module

observer = ConvObserver(model) # Observe model

features = observer(tensor_imgs) # Forward pass through the observer

# After the forward pass, the observer stored the feature info

out_p = ".cache"
out_p.mkdir(exist_ok=True)

# Save figures
observer.save_figs(cache_p)

# Iterate manually through conv features
for name, output in features:
    # output is a batch of
    # output.shape (B,N,H,W)

    print(output.shape)
    break
```

## Create your own

All you need to do is to inherit the `ModuleObserver` class.

See `ConvObserver` to see how to inherit and use.

## Contribute

The project is small and some peope may have other use cases.

Poetry is being used to manage the environment.

Feel free to open an [issue](https://github.com/AlanBlanchet/torch-module-observer/issues) and/or do a PR when you believe it would help the community.
