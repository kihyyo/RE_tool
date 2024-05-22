import os
import platform
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))

os.system("pip install protobuf==3.20")

try:
    import xmltodict
except:
    os.system("pip install xmltodict")

try:
    from Cryptodome.Random import get_random_bytes
except:
    os.system('pip install pycryptodomex')

try:
    folder = None
    if platform.machine() == 'aarch64':
        # arm64 환경일 경우 실행권한 부여
        folder = 'LinuxArm'
    elif platform.system() == 'Linux':
        folder = 'Linux'

    if folder:
        bin_path = os.path.join(os.path.dirname(__file__), 'bin', folder)
        os.system(f"chmod 777 -R {bin_path}")
except:
    pass

from .manager import WVDecryptManager
from .tool import WVTool



if os.path.exists(os.path.join(os.path.dirname(__file__), 'downloader.py')):
    from . import downloader
    REDownloader = downloader.REDownloader
else:
    from support import SupportSC

    downloader = SupportSC.load_module_f(__file__, 'downloader')
    REDownloader = downloader.REDownloader

import functools
import re
from urllib.parse import urlparse
from unittest.mock import patch

import requests

from framework.init_main import Framework
from .setup import P as PLUGIN

F = Framework.get_instance()


# def start_wrapper(f):
#     @functools.wraps(f)
#     def wrap(*args, **kwargs):
#         self = args[0]
#         mpd_url = urlparse(self.mpd_url)
#         match = re.search(r'wavve\.com', mpd_url.netloc)
#         if match and 'Host' in self.mpd_headers:
#             # 요청 주소와 헤더의 Host 주소가 다를 경우 수정
#             self.mpd_headers['Host'] = mpd_url.netloc
#         return f(*args, **kwargs)
#     return wrap
# REDownloader.start = start_wrapper(REDownloader.start)


# def patch_wavve_requests(f, mod: str):
#     '''
#     by ssokka
#         2023.08.21 웨이브 Proxy 패치
#         2023.08.22 코드 정리
#     '''
#     f_name = f.__name__
#     def req(*args, f=getattr(requests, mod), **kwargs):
#         support_site = F.PluginManager.get_plugin_instance('support_site')
#         use_proxy = support_site.ModelSetting.get_bool('site_wavve_use_proxy')
#         proxy_url = support_site.ModelSetting.get('site_wavve_proxy_url')
#         proxies = {'http': None, 'https': None}
#         if use_proxy and proxy_url:
#             proxies['http'] = proxy_url
#             proxies['https'] = proxy_url
#         PLUGIN.logger.debug(f'{f_name}, requests.{mod}, {proxies}')
#         response = f(*args, proxies=proxies, **kwargs)
#         if response.text.startswith('<?xml'):
#             # xml 내용 중에 escape 처리되지 않은 ampersand가 있을 경우 처리
#             response._content = bytes(
#                 re.sub(r'&(?!#38;)', '&#38;', response.text),
#                 response.encoding if response.encoding else 'utf-8')
#         return response
#     @functools.wraps(f)
#     @patch(f'requests.{mod}', req)
#     def wrap(*args, **kwargs):
#         return f(*args, **kwargs)
#     return wrap
# REDownloader.get_mpd = patch_wavve_requests(REDownloader.get_mpd, 'get')
# REDownloader.do_make_key = patch_wavve_requests(REDownloader.do_make_key, 'post')
