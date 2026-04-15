#!/usr/bin/env python3
"""创建 PyInstaller spec 文件 - 包含完整的 OCR 支持"""
import os
from pathlib import Path

spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

# ===========================================================
# Collect all data files
# ===========================================================

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

# 收集 paddle - CRITICAL: must use collect_all + manual .pyd scan
# paddle.base.core etc are .pyd C extensions that collect_submodules misses
try:
    import paddle
    paddle_dir = Path(paddle.__file__).parent

    # Method 1: collect_all returns (datas, binaries, hiddenimports) tuple
    paddle_datas, paddle_binaries, paddle_hidden = collect_all('paddle')
    datas.extend(paddle_datas)
    binaries.extend(paddle_binaries)
    _paddle_submodules = paddle_hidden
    print(f"collect_all('paddle'): +{len(paddle_datas)} data, +{len(paddle_binaries)} binaries, +{len(paddle_hidden)} hidden")

    # Method 2: explicitly walk paddle package and grab ALL .pyd files
    pyd_count = 0
    for root, dirs, files in os.walk(paddle_dir):
        for f in files:
            if f.endswith('.pyd') or f.endswith('.dll') or f.endswith('.so'):
                src = os.path.join(root, f)
                # Relative to paddle package root
                rel = os.path.relpath(src, paddle_dir)
                dest_dir = os.path.join('paddle', os.path.dirname(rel))
                binaries.append((src, dest_dir))
                pyd_count += 1
    print(f"Manual paddle .pyd/.dll/.so scan: +{pyd_count} files")

    # Note: collect_all already includes hiddenimports, no need for separate collect_submodules

except Exception as e:
    print(f"Warning: Could not collect paddle files: {e}")
    _paddle_submodules = []

# 收集 paddleocr - CRITICAL: use collect_all + manual .pyd scan
try:
    paddleocr_datas, paddleocr_binaries, paddleocr_hidden = collect_all('paddleocr')
    datas.extend(paddleocr_datas)
    binaries.extend(paddleocr_binaries)

    # Manual .pyd scan for paddleocr
    try:
        import paddleocr as _paddleocr_pkg
        paddleocr_dir = Path(_paddleocr_pkg.__file__).parent
        pyd_count = 0
        for root, dirs, files in os.walk(paddleocr_dir):
            for f in files:
                if f.endswith('.pyd') or f.endswith('.dll') or f.endswith('.so'):
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, paddleocr_dir)
                    dest_dir = os.path.join('paddleocr', os.path.dirname(rel))
                    binaries.append((src, dest_dir))
                    pyd_count += 1
        print(f"Manual paddleocr .pyd/.dll/.so scan: +{pyd_count} files")
    except Exception as e2:
        print(f"Note: paddleocr .pyd scan skipped: {e2}")

    print(f"collect_all('paddleocr'): +{len(paddleocr_datas)} data, +{len(paddleocr_binaries)} binaries, +{len(paddleocr_hidden)} hidden")
except Exception as e:
    print(f"Warning: Could not collect paddleocr files: {e}")

# 收集 easyocr - CRITICAL: use collect_all for completeness
try:
    easyocr_datas, easyocr_binaries, easyocr_hidden = collect_all('easyocr')
    datas.extend(easyocr_datas)
    binaries.extend(easyocr_binaries)
    _easyocr_submodules = easyocr_hidden

    # Manual .pyd scan for easyocr
    try:
        import easyocr as _easyocr_pkg
        easyocr_dir = Path(_easyocr_pkg.__file__).parent
        pyd_count = 0
        for root, dirs, files in os.walk(easyocr_dir):
            for f in files:
                if f.endswith('.pyd') or f.endswith('.dll') or f.endswith('.so'):
                    src = os.path.join(root, f)
                    rel = os.path.relpath(src, easyocr_dir)
                    dest_dir = os.path.join('easyocr', os.path.dirname(rel))
                    binaries.append((src, dest_dir))
                    pyd_count += 1
        print(f"Manual easyocr .pyd/.dll/.so scan: +{pyd_count} files")
    except Exception as e2:
        print(f"Note: easyocr .pyd scan skipped: {e2}")

    print(f"collect_all('easyocr'): +{len(easyocr_datas)} data, +{len(easyocr_binaries)} binaries, +{len(easyocr_hidden)} hidden")
except Exception as e:
    print(f"Warning: Could not collect easyocr files: {e}")
    _easyocr_submodules = []

# 收集 torch - CRITICAL: collect_all + manual lib sweep
try:
    import torch
    torch_dir = Path(torch.__file__).parent

    # collect_all for torch - returns (datas, binaries, hiddenimports)
    torch_datas, torch_binaries, torch_hidden = collect_all('torch')
    datas.extend(torch_datas)
    binaries.extend(torch_binaries)
    print(f"collect_all('torch'): +{len(torch_datas)} data, +{len(torch_binaries)} binaries, +{len(torch_hidden)} hidden")

    # Manual sweep: torch/lib (DLLs, pyd, etc.)
    torch_lib_dir = torch_dir / 'lib'
    if torch_lib_dir.exists():
        for f in torch_lib_dir.iterdir():
            if f.is_file():
                binaries.append((str(f), 'torch/lib'))
        print(f"torch/lib: +{len(list(torch_lib_dir.iterdir()))} files")

    # Manual sweep: torch C extension .pyd files in root
    for f in torch_dir.iterdir():
        if f.is_file() and f.suffix in ('.pyd', '.dll', '.so'):
            binaries.append((str(f), 'torch'))
            print(f"torch root ext: {f.name}")

    # Manual sweep: torch subdirectory .pyd files
    for sub_dir in ['distributed', 'optim', 'nn', 'utils', 'autograd', 'backends',
                    'onnx', 'jit', 'cuda', 'sparse', 'viz']:
        sub = torch_dir / sub_dir
        if sub.exists():
            for f in sub.iterdir():
                if f.is_file() and f.suffix in ('.pyd', '.dll', '.so'):
                    binaries.append((str(f), f'torch/{sub_dir}'))
    print(f"torch subdir .pyd scan done")
except Exception as e:
    print(f"Warning: Could not collect torch files: {e}")

# 收集 torchvision - collect_all returns (datas, binaries, hiddenimports)
try:
    tv_datas, tv_binaries, tv_hidden = collect_all('torchvision')
    datas.extend(tv_datas)
    binaries.extend(tv_binaries)
    print(f"collect_all('torchvision'): +{len(tv_datas)} data, +{len(tv_binaries)} binaries")
except Exception as e:
    print(f"Warning: Could not collect torchvision files: {e}")

# 收集 scipy - collect_all for C extensions (.pyd files)
try:
    sp_datas, sp_binaries, sp_hidden = collect_all('scipy')
    datas.extend(sp_datas)
    binaries.extend(sp_binaries)
    print(f"collect_all('scipy'): +{len(sp_datas)} data, +{len(sp_binaries)} binaries")
except Exception as e:
    print(f"Warning: Could not collect scipy files: {e}")

# 收集 skimage - collect_all for C extensions
try:
    ski_datas, ski_binaries, ski_hidden = collect_all('skimage')
    datas.extend(ski_datas)
    binaries.extend(ski_binaries)
    print(f"collect_all('skimage'): +{len(ski_datas)} data, +{len(ski_binaries)} binaries")
except Exception as e:
    print(f"Warning: Could not collect skimage files: {e}")

# 收集 cv2 (opencv) - collect_all for DLLs
try:
    cv_datas, cv_binaries, cv_hidden = collect_all('cv2')
    datas.extend(cv_datas)
    binaries.extend(cv_binaries)
    print(f"collect_all('cv2'): +{len(cv_datas)} data, +{len(cv_binaries)} binaries")
except Exception as e:
    print(f"Warning: Could not collect cv2 files: {e}")

# 收集 shapely - collect_all for C extensions (GEOS DLL)
try:
    sh_datas, sh_binaries, sh_hidden = collect_all('shapely')
    datas.extend(sh_datas)
    binaries.extend(sh_binaries)
    print(f"collect_all('shapely'): +{len(sh_datas)} data, +{len(sh_binaries)} binaries")
except Exception as e:
    print(f"Warning: Could not collect shapely files: {e}")

# ===========================================================
# Analysis configuration
# ===========================================================

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
        "paddleocr.ppocr.postprocess",
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
    ] + _paddle_submodules + _easyocr_submodules,
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
    upx=False,                # Disabled: UPX compression can corrupt large DLLs (torch/paddle)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,           # DEBUG: temporarily enable console to capture startup errors
    disable_windowed_traceback=False,
    argv_emulation=False,
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
