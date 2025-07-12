# Real-ESRGAN Fine-Tuned Model

This repository contains a fine-tuned version of the [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) network for single-image super-resolution. The model has been trained for 100,000 iterations on the Flickr2K dataset and extends the original implementation.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Patch Guide](#patch-guide)
4. [Quick Inference](#quick-inference)
   - [Command-Line Inference](#command-line-inference)
   - [Inference Example](#inference-example)
5. [Training](#training)
6. [License](#license)

---

## Prerequisites

- Python 3.8 or higher
- `pip` package manager
- Git

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Real-ESRGAN-finetune.git
   cd Real-ESRGAN-finetune
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   python setup.py develop
   ```

---

## Patch Guide

To ensure compatibility with the latest `torchvision`, update the import path in `basicsr/data/degradations.py`:

```diff
- from torchvision.transforms.functional_tensor import rgb_to_grayscale
+ from torchvision.transforms.functional import rgb_to_grayscale
```

---

## Quick Inference

You can run inference using the provided Python script:

### Command-Line Interface

```bash
python inference_realesrgan.py \
  -n RealESRGAN_x4plus \
  -i <input_path> \
  -o <output_path> \
  [--outscale <scale>] \
  [--face_enhance] \
  [--fp32] \
  [--tile <size>] \
  [--suffix <suffix>] \
  [--ext <auto|jpg|png>]
```

**Options**:

- `-i`, `--input`       : Input image or directory (default: `inputs`).
- `-o`, `--output`      : Output directory (default: `results`).
- `-n`, `--model_name`  : Model name (default: `RealESRGAN_x4plus`).
- `-s`, `--outscale`    : Final upsampling scale (default: `4`).
- `--face_enhance`      : Enable GFPGAN face enhancement.
- `--fp32`              : Use full (fp32) precision instead of fp16.
- `-t`, `--tile`        : Tile size for tiled inference (0 = no tiling).
- `--suffix`            : Suffix for output filenames (default: `out`).
- `--ext`               : Output image format (`auto`, `jpg`, `png`).

### Inference Example

1. **Download pre-trained weights**:
   ```bash
   wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights
   ```
2. **Run inference**:
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs --face_enhance
   ```
3. **Results** will be saved in the `results` folder.

---

## Training

Train the model or fine-tune on your own data:

```bash
python realesrgan/train.py \
  -opt options/finetune_realesrgan_x4plus_pairdata.yml \
  --auto_resume
```

Modify the YAML file in `options/` to adjust training parameters, dataset paths, and logging configurations.

---

## License

This project is licensed under the [MIT License](LICENSE).

