# PyInstaller hook for paddleocr
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Collect all paddleocr data files
datas = collect_data_files('paddleocr')

# Collect all paddleocr submodules
hiddenimports = collect_submodules('paddleocr')

# Additional hidden imports for paddleocr
hiddenimports += [
    'paddleocr.ppocr',
    'paddleocr.ppocr.utils',
    'paddleocr.ppocr.data',
    'paddleocr.ppocr.postprocess',
    'paddleocr.ppocr.data.imaug',
    'paddleocr.ppocr.data.imaug.operators',
    'paddleocr.ppocr.data.imaug.text_image_aug',
    'paddleocr.ppocr.data.imaug.rec_img_aug',
    'paddleocr.ppocr.data.imaug.copy_paste',
    'paddleocr.ppocr.data.imaug.iaa_augment',
    'paddleocr.ppocr.data.imaug.random_crop_data',
    'paddleocr.ppocr.data.imaug.make_shrink_map',
    'paddleocr.ppocr.data.imaug.make_border_map',
    'paddleocr.ppocr.data.imaug.label_ops',
    'paddleocr.ppocr.data.imaug.fce_aug',
    'paddleocr.ppocr.data.imaug.sast_process',
    'paddleocr.ppocr.data.imaug.abinet_aug',
    'paddleocr.ppocr.data.imaug.vqa',
    'paddleocr.ppocr.data.imaug.vqa.tokenizer',
    'paddleocr.ppocr.data.imaug.vqa.augment',
    'paddleocr.ppocr.modeling',
    'paddleocr.ppocr.modeling.architectures',
    'paddleocr.ppocr.modeling.backbones',
    'paddleocr.ppocr.modeling.necks',
    'paddleocr.ppocr.modeling.heads',
    'paddleocr.ppocr.modeling.transforms',
    'paddleocr.ppocr.losses',
    'paddleocr.ppocr.metrics',
    'paddleocr.ppocr.optimizer',
    'paddleocr.ppocr.scheduler',
    'paddleocr.tools',
    'paddleocr.tools.infer',
    'paddleocr.tools.infer.utility',
    'paddleocr.tools.infer.predict_system',
    'paddleocr.tools.infer.predict_rec',
    'paddleocr.tools.infer.predict_det',
    'paddleocr.tools.infer.predict_cls',
    'paddleocr.tools.infer.predict_e2e',
    'paddleocr.tools.infer.predict_table',
    'paddleocr.tools.infer.predict_sr',
    'paddleocr.tools.infer.predict_pse',
    'paddleocr.tools.infer.predict_fce',
    'paddleocr.tools.infer.predict_sast',
    'paddleocr.tools.infer.predict_abinet',
    'paddleocr.tools.infer.predict_satrn',
    'paddleocr.tools.infer.predict_nrtr',
    'paddleocr.tools.infer.predict_srn',
    'paddleocr.tools.infer.predict_rare',
    'paddleocr.tools.infer.predict_drrg',
    'paddleocr.tools.infer.predict_can',
]

# Collect binaries
binaries = []
