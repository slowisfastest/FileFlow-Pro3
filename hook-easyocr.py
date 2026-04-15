# PyInstaller hook for easyocr - collect_all returns (datas, binaries, hiddenimports)
from PyInstaller.utils.hooks import collect_all, collect_submodules

# collect_all catches data + binaries + submodules including C extensions
datas, binaries, hiddenimports = collect_all('easyocr')

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
