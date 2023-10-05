<div style="display: flex; flex-direction: column; justify-content: center">
    <div style="text-align:center">
        <img src="assets/foolai_256.png"/>
    </div>
    <h1 align="center" style="border:none">FoolAI</h1>
    <p align="center">
        <a href="#about">About</a> |
        <a href="#usage">Usage</a> |
        <a href="#installation">Installation</a> |
        <a href="#disclaimer">Disclaimer</a>
    </p>
</div>

## About

A command-line tool for fooling AI/machine learning models. In concrete, it generates adversarial examples to destroy the ability of ML models.  

Easy to use, and light-weight.

### Supported Methods

This is under development so has few method yet.

|Tasks|Attack Methods|
|:---|:---|
|Image Classification|Adversarial Examples (FGSM)|
<!-- |Text Classification|Adversarial Text| -->

<br />

## Usage

```sh
foolai --help
```

### Fool Image Classification Models on Hugging Face

```sh
# --model/-m: Target model. Set repository ID on Hugging Face.
# --img/-i: Original image to be used for generating adversarial examples
foolai fool -m microsoft/resnet-50 -i dog.jpg
```

<br />

## Installation

### From Pip

```sh
pip install foolai
foolai --help
```

### From Git Repo

```sh
git clone https://github.com/hideckies/foolai.git
cd foolai
poetry shell
poetry install
foolai --help
```

<br />

## Disclaimer

- It's an experimental project and ML models are constantly evolving, so it may not necessarily work well.
- Currently its target is **Hugging Face** models only yet.
