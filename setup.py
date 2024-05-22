setting = {
    'filepath' : __file__,
    'use_db': False,
    'use_default_setting': False,
    'home_module': None,
    'menu': {
        'uri': __package__,
        'name': 'RE 다운로드',
        'list': [
            {
                'uri': 'download',
                'name': '다운로드',
                'list': [
                    {
                        'uri': 'list',
                        'name': '다운로드 목록',
                    },
                    
                ]
            },
            {
                'uri': 'manual',
                'name': '매뉴얼',
                'list': [
                    {
                        'uri': 'README.md',
                        'name': 'README',
                    },
                ]
            },
            {
                'uri': 'log',
                'name': '로그',
            },
        ]
    },
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)
try:
    from .mod_download import ModuleDownload
    P.set_module_list([ModuleDownload])
except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc())

