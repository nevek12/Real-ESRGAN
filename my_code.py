import os


from basicsr.metrics import calculate_psnr, calculate_ssim
import cv2
import os
gt_folder = 'datasets/Flickr2K/val/HR'  # эталонные изображения
sr_folder = 'results'  # сгенерированные изображения

max_psnr = 0
max_ssim = 0
best_model_psnr = 0
best_model_ssim = 0
lsst = ['100000', 'latest']
for i in range(len(lsst)):
    print(os.system(f'powershell python inference_realesrgan.py -n net_g_{lsst[i]}.pth -i datasets/Flickr2K/val/LR -o results'))

    psnr_values = []
    ssim_values = []

    # Проходим по всем изображениям
    for img_name in os.listdir(gt_folder):
        gt_path = os.path.join(gt_folder, img_name)
        sr_path = os.path.join(sr_folder, img_name.replace('.png', '_out.png'))

        # Загружаем изображения
        gt_img = cv2.imread(gt_path)
        sr_img = cv2.imread(sr_path)

        # Вычисляем метрики
        psnr = calculate_psnr(gt_img, sr_img, crop_border=4)
        ssim = calculate_ssim(gt_img, sr_img, crop_border=4)

        psnr_values.append(psnr)
        ssim_values.append(ssim)

        print(f'{img_name} - PSNR: {psnr:.2f} dB, SSIM: {ssim:.4f}')

    # Считаем средние значения
    avg_psnr = sum(psnr_values) / len(psnr_values)
    avg_ssim = sum(ssim_values) / len(ssim_values)

    if avg_psnr > max_psnr:
        best_model_psnr = i
        max_psnr = avg_psnr
    if avg_ssim > max_ssim:
        best_model_ssim = i
        max_ssim = avg_ssim
    print('______________________________________________________________')
    print(f'MODEL: net_g_{lsst[i]}.pth')
    print(f'Средний PSNR: {avg_psnr:.2f} dB')
    print(f'Средний SSIM: {avg_ssim:.4f}')
    print('______________________________________________________________')

print(f"max psnr: {max_psnr}")
print(f"max ssim: {max_ssim}")
print(f"the best model: {best_model_psnr} : {best_model_ssim}")

