from .dependencies import get_xhs_downloader_service
from .module import get_module
from .services.xhs_downloader_service import XHSDownloaderService

__all__ = [
    "get_module",
    "get_xhs_downloader_service",
    "XHSDownloaderService",
]
