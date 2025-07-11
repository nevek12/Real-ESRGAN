import os
import sys
import importlib


def patch_degradations():
    try:
        # Пытаемся импортировать basicsr
        import basicsr
        basicsr_path = os.path.dirname(basicsr.__file__)
        degradations_path = os.path.join(basicsr_path, 'data', 'degradations.py')

        # Читаем содержимое файла
        with open(degradations_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Заменяем проблемную строку
        new_content = content.replace(
            "from torchvision.transforms.functional_tensor import rgb_to_grayscale",
            "from torchvision.transforms.functional import rgb_to_grayscale"
        )

        # Если изменения нужны, сохраняем файл
        if new_content != content:
            with open(degradations_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Patched {degradations_path}")
        else:
            print(f"⚠️ Patch not needed for {degradations_path}")

    except Exception as e:
        print(f"❌ Error patching degradations.py: {str(e)}")


# Применяем патч при импорте
patch_degradations()