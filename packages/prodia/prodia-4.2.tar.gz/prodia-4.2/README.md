# prodia
Not official library for using Prodia Stable Diffusion API

# Installation
```
pip install prodiapy==4.2
```

# Example
```python
from prodia import StableDiffusion

pipe = StableDiffusion("your-prodia-x-key")

job = pipe.generate({'prompt': 'puppies in cloud, 4k'})

result = pipe.wait_for(job)
print(result['imageUrl'])
```

# Full documentation
[link to docs](https://prodiapy.readme.io/reference/introduction)

# Discord Server
Feel free to join our [community](https://discord.gg/PtdHCVysfj) 