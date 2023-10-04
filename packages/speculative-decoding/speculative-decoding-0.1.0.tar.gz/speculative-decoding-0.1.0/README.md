<img src="./speculative-decoding.png" width="500px"></img>

## Speculative Decoding (wip)

Explorations into some recent techniques surrounding <a href="https://arxiv.org/abs/2211.17192">speculative decoding</a>

Also have a few ideas of my own that I will try and share in this repository, if they work. The goal is to initially use it to speed up the text-to-semantic decoder in <a href="https://github.com/lucidrains/spear-tts-pytorch">Spear-TTS</a>

## Appreciation

- <a href="https://stability.ai/">StabilityAI</a> and <a href="https://huggingface.co/">🤗 Huggingface</a> for the generous sponsorship, as well as my other sponsors, for affording me the independence to open source current artificial intelligence techniques.

## Todo

- [x] in early exit scheme, cache the hidden layer during spec decoding, as small and large models share the same first few layers
- [x] for early exit, allow an extra transformer block head (separate from main transformer stem)
- [x] figure out batched spec decoding - different rows may advance at different rates
- [x] further optimize batched spec decoding, as losing some performance from all the indexing - seems like it will take some work for this technique to be actually usable
- [x] make batched spec decoding work with early exit strategy
- [x] complete speculative sampling with prophet transformer idea - seems to work well! 🙌

- [ ] get some wandb charts and see how prophet compares with early exit strategy, share on repository
- [ ] for early exit strategy, try randomly summing last cached embedding back to the same model (a la alphafold2 recycling), randomly cropped along sequence length, and train early exit loss this way. see if one can improve the gamma this way
- [ ] dedicate a morning to microoptimizations

## Citations

```bibtex
@inproceedings{Leviathan2022FastIF,
    title   = {Fast Inference from Transformers via Speculative Decoding},
    author  = {Yaniv Leviathan and Matan Kalman and Y. Matias},
    booktitle = {International Conference on Machine Learning},
    year    = {2022},
    url     = {https://api.semanticscholar.org/CorpusID:254096365}
}
```

```bibtex
@inproceedings{sun2023spectr,
    title     = {SpecTr: Fast Speculative Decoding via Optimal Transport},
    author    = {Ziteng Sun and Ananda Theertha Suresh and Jae Hun Ro and Ahmad Beirami and Himanshu Jain and Felix Yu and Michael Riley and Sanjiv Kumar},
    booktitle = {Workshop on Efficient Systems for Foundation Models @ ICML2023},
    year      = {2023},
    url       = {https://openreview.net/forum?id=d0mGsaheuT}
}
```

```bibtex
@article{Chen2023AcceleratingLL,
    title     = {Accelerating Large Language Model Decoding with Speculative Sampling},
    author    = {Charlie Chen and Sebastian Borgeaud and Geoffrey Irving and Jean-Baptiste Lespiau and L. Sifre and John M. Jumper},
    journal   = {ArXiv},
    year      = {2023},
    volume    = {abs/2302.01318},
    url       = {https://api.semanticscholar.org/CorpusID:256503945}
}
```

```bibtex
@article{Yan2020ProphetNetPF,
    title   = {ProphetNet: Predicting Future N-gram for Sequence-to-Sequence Pre-training},
    author  = {Yu Yan and Weizhen Qi and Yeyun Gong and Dayiheng Liu and Nan Duan and Jiusheng Chen and Ruofei Zhang and Ming Zhou},
    journal = {ArXiv},
    year    = {2020},
    volume  = {abs/2001.04063},
    url     = {https://api.semanticscholar.org/CorpusID:210164665}
}
```
