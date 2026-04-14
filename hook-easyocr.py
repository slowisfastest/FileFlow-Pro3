# PyInstaller hook for easyocr
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules, collect_dynamic_libs

# Collect all easyocr data files
datas = collect_data_files('easyocr')

# Collect all easyocr submodules
hiddenimports = collect_submodules('easyocr')

# Collect binaries (DLLs/SOs)
binaries = collect_dynamic_libs('easyocr')

# Additional hidden imports for easyocr
hiddenimports += [
    'easyocr.model',
    'easyocr.model.model',
    'easyocr.model.modules',
    'easyocr.model.vgg_model',
    'easyocr.model.resnet_model',
    'easyocr.model.sequence_model',
    'easyocr.model.transformation',
    'easyocr.model.prediction',
    'easyocr.utils',
    'easyocr.utils.imgproc',
    'easyocr.utils.general',
    'easyocr.utils.group_text',
    'easyocr.config',
    'easyocr.character',
    'easyocr.dict',
]

# Note: binaries already set above via collect_dynamic_libs('easyocr')
