from support import SupportSubprocess

from .setup import *

name = 'download'
   
from . import REDownloader

class ModuleDownload(PluginModuleBase):

    def __init__(self, P):
        super(ModuleDownload, self).__init__(P, 'list')
        self.name = name
        REDownloader.initialize(self.callback_function)
        default_route_socketio_module(self, attach='/list')


    def process_menu(self, page_name, req):
        return render_template(f'{P.package_name}_{name}_{page_name}.html', arg={})


    def process_command(self, command, arg1, arg2, arg3, req):
        ret = {'ret':'success'}
        if command == 'list':
            ret = []
            for ins in REDownloader.get_list():
                ret.append(ins.get_data())
        elif command == 'stop':
            for ins in REDownloader.get_list():
                if ins.idx == arg1:
                    ins.stop()
                    ret['data'] = ins.get_data()
                    break
        return jsonify(ret)


    def callback_function(self, args):
        refresh_type = 'refresh'
        if args['status'] == "READY":
            data = {'type':'info', 'msg' : f"{args['data']['output_filename']} 다운로드를 시작합니다.", 'url':'/RE_tool/download/list'}
            socketio.emit("notify", data, namespace='/framework')
            refresh_type = 'add'
        elif args['status'] == "EXIST_OUTPUT_FILEPATH":
            data = {'type':'warning', 'msg' : f"{args['data']['output_filename']} 파일이 있습니다.",  'url':'/RE_tool/download/list'}
            socketio.emit("notify", data, namespace='/framework')
        elif args['status'] == "COMPLETED":
            data = {'type':'info', 'msg' : f"{args['data']['output_filename']} 다운로드 완료",  'url':'/RE_tool/download/list'}
            socketio.emit("notify", data, namespace='/framework')
        self.socketio_callback(refresh_type, args['data'])
