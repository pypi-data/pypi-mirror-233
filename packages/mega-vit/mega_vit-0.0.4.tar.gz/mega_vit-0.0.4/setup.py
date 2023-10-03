# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mega_vit']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'mega-vit',
    'version': '0.0.4',
    'description': 'mega-vit - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MegaVit\nThe open source implementation of the model from "Scaling Vision Transformers to 22 Billion Parameters"\n\n\n\n[Paper Link](https://arxiv.org/pdf/2302.05442.pdf)\n\n# Appreciation\n* Lucidrains\n* Agorians\n\n\n\n# Install\n`pip install mega-vit`\n\n# Usage\n- Simple usage,\n```python\nimport torch\nfrom mega_vit.main import MegaVit\n\nv = MegaVit(\n    image_size = 256,\n    patch_size = 32,\n    num_classes = 1000,\n    dim = 1024,\n    depth = 6,\n    heads = 16,\n    mlp_dim = 2048,\n    dropout = 0.1,\n    emb_dropout = 0.1\n)\n\nimg = torch.randn(1, 3, 256, 256)\n\npreds = v(img) # (1, 1000)\nprint(preds)\n```\n\n- Hyperparams as stated in paper:\n```python\nimport torch\nfrom mega_vit.main import MegaVit\n\nv = ViT(\n    image_size = 224,\n    patch_size = 14,\n    num_classes = 1000,\n    dim = 6144,\n    depth = 48,\n    heads = 48,\n    mlp_dim = 2048,\n    dropout = 0.1,\n    emb_dropout = 0.1\n)\n\nimg = torch.randn(1, 3, 224, 224)\n\npreds = v(img) # (1, 1000)\nprint(preds)\n```\n\n# Model Architecture\n- Regular vit with new parallel layers, QK(Query/Key)Normalization, and omitted biases.\n\n----\n# Dataset Strategy\nThe paper trains ViT-22B on a version of the JFT dataset that has been extended to around 4 billion images. JFT is a large-scale dataset scraped from the internet, originally containing over 300 million images labeled with a hierarchical taxonomy of 30,000 categories. \n\nThe authors do not provide full details on how the dataset was extended from the original JFT to 4 billion images. However, the goal seems to be creating a larger and more diverse training set to support scaling up the model size. Pre-training on larger datasets enables learning more robust and generalizable visual representations.\n\nThe authors evaluate ViT-22B on a comprehensive set of 39 datasets covering various domains like image classification, dense prediction tasks, video, and fairness benchmarks. Using such a diverse evaluation suite allows them to thoroughly assess the scalability and transferability of ViT-22B across different domains and data distributions.\n\nBelow is a table summarizing some of the key datasets used in the paper:\n\n| Dataset | Domain | Images | Classes |\n|-|-|-|-| \n| JFT (training set) | Internet images | ~4 billion | 30,000 |\n| ImageNet | Natural images | 1.28M | 1000 |\n| ImageNet-C | Corrupted ImageNet images | 1.28M | 1000 |  \n| ImageNet-R | Hard ImageNet images | 30K | 200 |\n| ImageNet-A | Adversarial ImageNet images | 7.5K | 200 |\n| ObjectNet | Natural images | 113K | 113 |\n| Cifar-10 | Tiny natural images | 60K | 10 |\n| Cifar-100 | Tiny natural images | 60K | 100 | \n| ADE20K | Scene parsing | 25K | 150 |\n| Kinetics-400 | Human action videos | 400K | 400 |\n| CelebA | Celeb faces | 202K | 40 |\n\n\n# License\nMIT\n\n# Citations\n```\n@misc{2302.05442,\nAuthor = {Mostafa Dehghani and Josip Djolonga and Basil Mustafa and Piotr Padlewski and Jonathan Heek and Justin Gilmer and Andreas Steiner and Mathilde Caron and Robert Geirhos and Ibrahim Alabdulmohsin and Rodolphe Jenatton and Lucas Beyer and Michael Tschannen and Anurag Arnab and Xiao Wang and Carlos Riquelme and Matthias Minderer and Joan Puigcerver and Utku Evci and Manoj Kumar and Sjoerd van Steenkiste and Gamaleldin F. Elsayed and Aravindh Mahendran and Fisher Yu and Avital Oliver and Fantine Huot and Jasmijn Bastings and Mark Patrick Collier and Alexey Gritsenko and Vighnesh Birodkar and Cristina Vasconcelos and Yi Tay and Thomas Mensink and Alexander Kolesnikov and Filip Pavetić and Dustin Tran and Thomas Kipf and Mario Lučić and Xiaohua Zhai and Daniel Keysers and Jeremiah Harmsen and Neil Houlsby},\nTitle = {Scaling Vision Transformers to 22 Billion Parameters},\nYear = {2023},\nEprint = {arXiv:2302.05442},\n}\n```\n\n# Todo\n- [ ] Add flash attention, with layernorm before attn, and then layernom for qk values,\n- [ ] Basic training script on CIFAR,\n- [ ] When using ViT-22B, similar to any large scale model, it is difficult to understand how the model arrived at a specific decision, which could lead to lack of\ntrust and accountability. Add in a mechanism to backtrack\n- [ ] create logic to train the decoder for 300k steps with a batch size of 64 using Adam (Kingma and Ba, 2015) and clip the gradients to a global norm value of 0.05 to stabilize training. We linearly increase the learning rate for 2500 steps to 0.0002 (starting from 0) and then decay the learning rate with a cosine schedule (Loshchilov and Hutter, 2017) back to 0.',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/mega-vit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
