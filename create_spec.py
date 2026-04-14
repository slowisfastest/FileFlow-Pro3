#!/usr/bin/env python3
"""创建 PyInstaller spec 文件 - 包含完整的 OCR 支持"""
import os
from pathlib import Path

spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

# ═══════════════════════════════════════════════════════════
# 收集所有数据文件
# ═══════════════════════════════════════════════════════════

datas = []
binaries = []

# 1. 收集 OCR 模型文件（如果存在）
ocr_models_dir = Path("ocr_models")
if ocr_models_dir.exists():
    for root, dirs, files in os.walk(ocr_models_dir):
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(Path("."))
            dest_path = rel_path.parent
            datas.append((str(file_path), str(dest_path)))

# 2. 使用 PyInstaller 的 collect_all 收集依赖
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules, collect_dynamic_libs

# 收集 paddle
try:
    paddle_datas = collect_data_files('paddle')
    paddle_binaries = collect_dynamic_libs('paddle')
    datas.extend(paddle_datas)
    binaries.extend(paddle_binaries)
    print(f"Collected {len(paddle_datas)} paddle data files")
    print(f"Collected {len(paddle_binaries)} paddle binaries")
except Exception as e:
    print(f"Warning: Could not collect paddle files: {e}")

# 收集 paddleocr
try:
    paddleocr_datas = collect_data_files('paddleocr')
    paddleocr_binaries = collect_dynamic_libs('paddleocr')
    datas.extend(paddleocr_datas)
    binaries.extend(paddleocr_binaries)
    print(f"Collected {len(paddleocr_datas)} paddleocr data files")
    print(f"Collected {len(paddleocr_binaries)} paddleocr binaries")
except Exception as e:
    print(f"Warning: Could not collect paddleocr files: {e}")

# 收集 easyocr
try:
    easyocr_datas = collect_data_files('easyocr')
    easyocr_binaries = collect_dynamic_libs('easyocr')
    datas.extend(easyocr_datas)
    binaries.extend(easyocr_binaries)
    print(f"Collected {len(easyocr_datas)} easyocr data files")
    print(f"Collected {len(easyocr_binaries)} easyocr binaries")
except Exception as e:
    print(f"Warning: Could not collect easyocr files: {e}")

# 收集 torch - 关键修复：确保所有DLL都被收集
try:
    import torch
    torch_datas = collect_data_files('torch')
    torch_binaries = collect_dynamic_libs('torch')
    datas.extend(torch_datas)
    binaries.extend(torch_binaries)
    print(f"Collected {len(torch_datas)} torch data files")
    print(f"Collected {len(torch_binaries)} torch binaries")
    
    # Critical: collect ALL files from torch/lib (DLLs, pyd, etc.)
    torch_lib_dir = Path(torch.__file__).parent / 'lib'
    if torch_lib_dir.exists():
        for f in torch_lib_dir.iterdir():
            if f.is_file() and (f.suffix in ('.dll', '.pyd', '.so', '.bin')):
                binaries.append((str(f), 'torch/lib'))
                print(f"Added torch lib: {f.name}")
    
    # Critical: collect ALL files from torch/bin (if exists)
    torch_bin_dir = Path(torch.__file__).parent / 'bin'
    if torch_bin_dir.exists():
        for f in torch_bin_dir.iterdir():
            if f.is_file() and (f.suffix in ('.dll', '.pyd', '.so', '.bin', '.exe')):
                binaries.append((str(f), 'torch/bin'))
                print(f"Added torch bin: {f.name}")
    
    # Critical: collect torch C extensions (.pyd files)
    torch_dir = Path(torch.__file__).parent
    for f in torch_dir.iterdir():
        if f.is_file() and f.suffix == '.pyd':
            binaries.append((str(f), 'torch'))
            print(f"Added torch ext: {f.name}")
    
    # Critical: torch.distributed and multiprocessing DLLs
    torch_distributed_dir = torch_dir / 'distributed'
    if torch_distributed_dir.exists():
        for f in torch_distributed_dir.iterdir():
            if f.is_file() and f.suffix in ('.dll', '.pyd'):
                binaries.append((str(f), 'torch/distributed'))
                print(f"Added torch/distributed: {f.name}")
except Exception as e:
    print(f"Warning: Could not collect torch files: {e}")

# 收集 torchvision
try:
    torchvision_datas = collect_data_files('torchvision')
    torchvision_binaries = collect_dynamic_libs('torchvision')
    datas.extend(torchvision_datas)
    binaries.extend(torchvision_binaries)
    print(f"Collected {len(torchvision_datas)} torchvision data files")
    print(f"Collected {len(torchvision_binaries)} torchvision binaries")
except Exception as e:
    print(f"Warning: Could not collect torchvision files: {e}")

# 收集 scipy
try:
    scipy_datas = collect_data_files('scipy')
    scipy_binaries = collect_dynamic_libs('scipy')
    datas.extend(scipy_datas)
    binaries.extend(scipy_binaries)
    print(f"Collected {len(scipy_datas)} scipy data files")
    print(f"Collected {len(scipy_binaries)} scipy binaries")
except Exception as e:
    print(f"Warning: Could not collect scipy files: {e}")

# 收集 skimage
try:
    skimage_datas = collect_data_files('skimage')
    skimage_binaries = collect_dynamic_libs('skimage')
    datas.extend(skimage_datas)
    binaries.extend(skimage_binaries)
    print(f"Collected {len(skimage_datas)} skimage data files")
    print(f"Collected {len(skimage_binaries)} skimage binaries")
except Exception as e:
    print(f"Warning: Could not collect skimage files: {e}")

# 收集 cv2
try:
    cv2_datas = collect_data_files('cv2')
    cv2_binaries = collect_dynamic_libs('cv2')
    datas.extend(cv2_datas)
    binaries.extend(cv2_binaries)
    print(f"Collected {len(cv2_datas)} cv2 data files")
    print(f"Collected {len(cv2_binaries)} cv2 binaries")
except Exception as e:
    print(f"Warning: Could not collect cv2 files: {e}")

# 收集 shapely
try:
    shapely_datas = collect_data_files('shapely')
    shapely_binaries = collect_dynamic_libs('shapely')
    datas.extend(shapely_datas)
    binaries.extend(shapely_binaries)
    print(f"Collected {len(shapely_datas)} shapely data files")
    print(f"Collected {len(shapely_binaries)} shapely binaries")
except Exception as e:
    print(f"Warning: Could not collect shapely files: {e}")

# ═══════════════════════════════════════════════════════════
# 分析配置
# ═══════════════════════════════════════════════════════════

a = Analysis(
    ["fileflow_pro.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        # 基础依赖
        "pdfplumber",
        "pdf2docx",
        "PIL",
        "PIL._imagingtk",
        "PIL._tkinter_finder",
        "fitz",
        "docx",
        "openpyxl",
        "pptx",
        "reportlab",
        "reportlab.pdfbase._fontdata",
        "reportlab.pdfbase._fontdata_widths_courier",
        "reportlab.pdfbase._fontdata_widths_courierbold",
        "reportlab.pdfbase._fontdata_widths_courieroblique",
        "reportlab.pdfbase._fontdata_widths_courierboldoblique",
        "reportlab.pdfbase._fontdata_widths_helvetica",
        "reportlab.pdfbase._fontdata_widths_helveticabold",
        "reportlab.pdfbase._fontdata_widths_helveticaoblique",
        "reportlab.pdfbase._fontdata_widths_helveticaboldoblique",
        "reportlab.pdfbase._fontdata_widths_timesroman",
        "reportlab.pdfbase._fontdata_widths_timesbold",
        "reportlab.pdfbase._fontdata_widths_timesitalic",
        "reportlab.pdfbase._fontdata_widths_timesbolditalic",
        "reportlab.pdfbase._fontdata_widths_symbol",
        "reportlab.pdfbase._fontdata_widths_zapfdingbats",
        "reportlab.pdfbase._fontdata_enc_winansi",
        "reportlab.pdfbase._fontdata_enc_macroman",
        "reportlab.pdfbase._fontdata_enc_standard",
        "reportlab.pdfbase._fontdata_enc_symbol",
        "reportlab.pdfbase._fontdata_enc_zapfdingbats",
        "lxml",
        "lxml.etree",
        "lxml._elementpath",
        "xml.etree.ElementTree",
        "xml.etree.cElementTree",
        
        # NumPy 和 OpenCV
        "numpy",
        "numpy.core._dtype_ctypes",
        "numpy.core._multiarray_tests",
        "cv2",
        "cv2.cv2",
        
        # Paddle 相关
        "paddle",
        "paddle.base",
        "paddle.base.core",
        "paddle.base.framework",
        "paddle.base.executor",
        "paddle.base.compiler",
        "paddle.base.dygraph",
        "paddle.base.layers",
        "paddle.base.optimizer",
        "paddle.base.regularizer",
        "paddle.base.backward",
        "paddle.base.proto",
        "paddle.base.log_helper",
        "paddle.base.layer_helper",
        "paddle.base.unique_name",
        "paddle.utils",
        "paddle.utils.download",
        "paddle.utils.image_util",
        "paddle.utils.cpp_extension",
        "paddle.utils.dlpack",
        "paddle.utils.install_check",
        "paddle.utils.layer_utils",
        "paddle.utils.op_version",
        "paddle.utils.lazy_import",
        "paddle.dataset",
        "paddle.device",
        "paddle.distributed",
        "paddle.framework",
        "paddle.io",
        "paddle.jit",
        "paddle.metric",
        "paddle.nn",
        "paddle.optimizer",
        "paddle.regularizer",
        "paddle.scheduler",
        "paddle.static",
        "paddle.sysconfig",
        "paddle.tensor",
        "paddle.text",
        "paddle.vision",
        
        # PaddleOCR 相关
        "paddleocr",
        "paddleocr.ppocr",
        "paddleocr.ppocr.utils",
        "paddleocr.ppocr.utils.utility",
        "paddleocr.ppocr.utils.logging",
        "paddleocr.ppocr.utils.network",
        "paddleocr.ppocr.utils.visual",
        "paddleocr.ppocr.utils.save_load",
        "paddleocr.ppocr.utils.stats",
        "paddleocr.ppocr.data",
        "paddleocr.ppocr.data.imaug",
        "paddleocr.ppocr.data.imaug.operators",
        "paddleocr.ppocr.data.imaug.text_image_aug",
        "paddleocr.ppocr.data.imaug.rec_img_aug",
        "paddleocr.ppocr.data.imaug.copy_paste",
        "paddleocr.ppocr.data.imaug.iaa_augment",
        "paddleocr.ppocr.data.imaug.random_crop_data",
        "paddleocr.ppocr.data.imaug.make_shrink_map",
        "paddleocr.ppocr.data.imaug.make_border_map",
        "paddleocr.ppocr.data.imaug.label_ops",
        "paddleocr.ppocr.data.imaug.fce_aug",
        "paddleocr.ppocr.data.imaug.sast_process",
        "paddleocr.ppocr.data.imaug.abinet_aug",
        "paddleocr.ppocr.data.imaug.vqa",
        "paddleocr.ppocr.data.imaug.vqa.tokenizer",
        "paddleocr.ppocr.data.imaug.vqa.augment",
        "paddleocr.ppocr.modeling",
        "paddleocr.ppocr.modeling.architectures",
        "paddleocr.ppocr.modeling.backbones",
        "paddleocr.ppocr.modeling.backbones.det_mobilenet_v3",
        "paddleocr.ppocr.modeling.backbones.det_resnet_vd",
        "paddleocr.ppocr.modeling.backbones.det_resnet_vdb",
        "paddleocr.ppocr.modeling.backbones.det_resnet_sast",
        "paddleocr.ppocr.modeling.backbones.e2e_resnet_vd",
        "paddleocr.ppocr.modeling.backbones.rec_mobilenet_v3",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_vd",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_fpn",
        "paddleocr.ppocr.modeling.backbones.rec_mv1_enhance",
        "paddleocr.ppocr.modeling.backbones.rec_nrtr_mtb",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_31",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_32",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_45",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_aster",
        "paddleocr.ppocr.modeling.backbones.rec_svtrnet",
        "paddleocr.ppocr.modeling.backbones.rec_vitstr",
        "paddleocr.ppocr.modeling.backbones.rec_abinet_vl",
        "paddleocr.ppocr.modeling.backbones.rec_resnet_rfl",
        "paddleocr.ppocr.modeling.backbones.table_master_resnet",
        "paddleocr.ppocr.modeling.backbones.table_resnet_vd",
        "paddleocr.ppocr.modeling.necks",
        "paddleocr.ppocr.modeling.heads",
        "paddleocr.ppocr.modeling.transforms",
        "paddleocr.ppocr.losses",
        "paddleocr.ppocr.metrics",
        "paddleocr.ppocr.optimizer",
        "paddleocr.ppocr.scheduler",
        "paddleocr.tools",
        "paddleocr.tools.infer",
        "paddleocr.tools.infer.utility",
        "paddleocr.tools.infer.predict_system",
        "paddleocr.tools.infer.predict_rec",
        "paddleocr.tools.infer.predict_det",
        "paddleocr.tools.infer.predict_cls",
        "paddleocr.tools.infer.predict_e2e",
        "paddleocr.tools.infer.predict_table",
        "paddleocr.tools.infer.predict_sr",
        "paddleocr.tools.infer.predict_pse",
        "paddleocr.tools.infer.predict_fce",
        "paddleocr.tools.infer.predict_sast",
        "paddleocr.tools.infer.predict_abinet",
        "paddleocr.tools.infer.predict_satrn",
        "paddleocr.tools.infer.predict_nrtr",
        "paddleocr.tools.infer.predict_srn",
        "paddleocr.tools.infer.predict_rare",
        "paddleocr.tools.infer.predict_drrg",
        "paddleocr.tools.infer.predict_can",
        
        # skimage 相关
        "skimage",
        "skimage.filters",
        "skimage.filters.edges",
        "skimage.filters.rank",
        "skimage.transform",
        "skimage.transform._warps",
        "skimage.transform._geometric",
        "skimage.morphology",
        "skimage.measure",
        "skimage.feature",
        "skimage.util",
        "skimage.io",
        "skimage.color",
        "skimage.draw",
        "skimage.exposure",
        "skimage.segmentation",
        "skimage.restoration",
        "skimage.graph",
        "skimage.future",
        
        # imgaug 相关
        "imgaug",
        "imgaug.augmenters",
        "imgaug.augmenters.arithmetic",
        "imgaug.augmenters.blend",
        "imgaug.augmenters.blur",
        "imgaug.augmenters.color",
        "imgaug.augmenters.contrast",
        "imgaug.augmenters.convolutional",
        "imgaug.augmenters.flip",
        "imgaug.augmenters.geometric",
        "imgaug.augmenters.meta",
        "imgaug.augmenters.mixed",
        "imgaug.augmenters.pooling",
        "imgaug.augmenters.segmentation",
        "imgaug.augmenters.size",
        "imgaug.augmenters.weather",
        "imgaug.parameters",
        "imgaug.random",
        
        # 其他 OCR 依赖
        "lmdb",
        "pyclipper",
        "shapely",
        "shapely.geometry",
        "shapely.geos",
        "shapely.affinity",
        "shapely.ops",
        "shapely.prepared",
        "shapely.validation",
        "shapely.speedups",
        "shapely.vectorized",
        "scipy",
        "scipy.special",
        "scipy.optimize",
        "scipy.ndimage",
        "scipy.ndimage.filters",
        "scipy.ndimage.measurements",
        "scipy.ndimage.morphology",
        "scipy.signal",
        "scipy.spatial",
        "scipy.spatial.distance",
        "scipy.cluster",
        "scipy.cluster.vq",
        "scipy.cluster.hierarchy",
        "scipy.interpolate",
        "scipy.integrate",
        "scipy.linalg",
        "scipy.sparse",
        "scipy.stats",
        
        # EasyOCR 相关
        "easyocr",
        "easyocr.model",
        "easyocr.model.model",
        "easyocr.model.modules",
        "easyocr.model.vgg_model",
        "easyocr.model.resnet_model",
        "easyocr.model.sequence_model",
        "easyocr.model.transformation",
        "easyocr.model.prediction",
        "easyocr.utils",
        "easyocr.utils.imgproc",
        "easyocr.utils.general",
        "easyocr.utils.group_text",
        "easyocr.config",
        "easyocr.character",
        "easyocr.dict",
        
        # PyTorch 相关
        "torch",
        "torch.nn",
        "torch.nn.functional",
        "torch.nn.modules",
        "torch.nn.modules.activation",
        "torch.nn.modules.batchnorm",
        "torch.nn.modules.container",
        "torch.nn.modules.conv",
        "torch.nn.modules.dropout",
        "torch.nn.modules.flatten",
        "torch.nn.modules.linear",
        "torch.nn.modules.loss",
        "torch.nn.modules.module",
        "torch.nn.modules.normalization",
        "torch.nn.modules.padding",
        "torch.nn.modules.pooling",
        "torch.nn.modules.rnn",
        "torch.nn.modules.sparse",
        "torch.nn.modules.upsampling",
        "torch.nn.modules.utils",
        "torch.nn.parameter",
        "torch.nn.init",
        "torch.nn.utils",
        "torch.optim",
        "torch.optim.adam",
        "torch.optim.sgd",
        "torch.optim.lr_scheduler",
        "torch.utils",
        "torch.utils.data",
        "torch.utils.model_zoo",
        "torch.serialization",
        "torch.jit",
        "torch.onnx",
        "torchvision",
        "torchvision.transforms",
        "torchvision.models",
        "torchvision.ops",
        "torchvision.utils",
        # PyTorch multiprocessing & shm (critical for DLL loading)
        "torch.multiprocessing",
        "torch.multiprocessing.reductions",
        "torch.multiprocessing.spawn",
        "torch.distributed",
        "torch.distributed.elastic",
        "torch._C",
        "torch._dl",
        "torch.cuda",
        "torch.backends",
        "torch.backends.cudnn",
        "torch.backends.mkl",
        "torch.backends.mkldnn",
        "torch.storage",
        "torch.utils.dlpack",
        
        # 其他工具
        "tqdm",
        "yaml",
        "pyyaml",
        "packaging",
        "packaging.version",
        "packaging.specifiers",
        "packaging.requirements",
    ],
    hookspath=["hooks"] if os.path.exists("hooks") else [],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="FileFlowPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico" if os.path.exists("icon.ico") else None,
)
'''

with open('FileFlowPro.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)
print('Spec file created successfully: FileFlowPro.spec')
print('   Contains full OCR support with PaddleOCR, EasyOCR, and PyTorch')
