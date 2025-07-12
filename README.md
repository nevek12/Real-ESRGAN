# 🚀 Fine-Tuned Real-ESRGAN Model

This repository provides a fine-tuned version of the Real-ESRGAN model for high-quality image super-resolution tasks.

---

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Patching](#patching)
- [⚡ Quick Inference](#-quick-inference)
  - [Python Script](#python-script)
- [🧠 Model Training](#-model-training)
- [📈 Validation](#-validation)
- [📦 Used in Application](#-used-in-application)

---

## 🔧 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/xinntao/Real-ESRGAN.git
   cd Real-ESRGAN
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python setup.py develop
   ```

---

## 🩹 Patching

Update the import in `degradations.py` due to `torchvision` changes:

File to edit:
```
venv/Lib/site-packages/basicsr/data/degradations.py
```

Replace:
```python
from torchvision.transforms.functional_tensor import rgb_to_grayscale
```

With:
```python
from torchvision.transforms.functional import rgb_to_grayscale
```

---

## ⚡ Quick Inference

### 🐍 Python Script

You can use the X4 model for arbitrary output sizes with the `--outscale` argument.

**Usage Example:**
```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i infile --outscale 3.5 --face_enhance
```

**Help:**
```bash
  -h                   Show help
  -i, --input          Input image or folder (default: inputs)
  -o, --output         Output folder (default: results)
  -n, --model_name     Model name (default: RealESRGAN_x4plus)
  -s, --outscale       Final upsampling scale (default: 4)
  --suffix             Suffix of restored image (default: out)
  -t, --tile           Tile size (0 = no tiling)
  --face_enhance       Use GFPGAN to enhance faces (default: False)
  --fp32               Use fp32 precision (default: fp16)
  --ext                Image extension: auto | jpg | png (default: auto)
```

### Download Pre-trained Weights

```bash
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights
```

### Run Inference

```bash
python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs --face_enhance
```

Output images will be saved in the `results` directory.

---

## 🧠 Model Training

The model was fine-tuned for **100,000 iterations** on the **Flickr2K** dataset.

```bash
python realesrgan/train.py -opt options/finetune_realesrgan_x4plus_pairdata.yml --auto_resume
```

The file `finetune_realesrgan_x4plus_pairdata.yml` contains the training settings.

- **Generator** model: `RealESRGAN_x4plus.pth`
- **Discriminator** model: `RealESRGAN_x4plus_netD.pth`

---

## 📈 Validation

Validation was performed using the script:

```bash
python validation.py
```

Validation results for all checkpoints were logged in:

```
result_validation_models.txt
```

After evaluating all iterations, the best performing model was:

```text
net_g_85000.pth
```

---

## 📦 Used in Application

The final deployed application uses the selected model `net_g_85000.pth` for super-resolution inference.

---
