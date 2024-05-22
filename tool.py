import codecs
import json
import os
import platform
import subprocess
import time
import traceback
import threading

from support import SupportSubprocess, get_logger
from .subprocess_tool import ToolSubprocess
logger = get_logger()


bin_dir = os.path.join(os.path.dirname(__file__), 'bin', platform.system())

if platform.system() == 'Linux':
    if (platform.platform().find('86') == -1 and platform.platform().find('64') == -1) or platform.platform().find('arch') != -1 or platform.platform().find('arm') != -1:
        bin_dir = os.path.join(os.path.dirname(__file__), 'bin', 'LinuxArm')


M3U8DL = os.path.join(bin_dir, 'N_m3u8DL-RE' + ('.exe' if platform.system() == 'Windows' else ''))
FFMPEG = os.path.join(bin_dir, 'ffmpeg' + ('.exe' if platform.system() == 'Windows' else ''))
MP4DUMP = os.path.join(bin_dir, 'mp4dump' + ('.exe' if platform.system() == 'Windows' else ''))
MP4INFO = os.path.join(bin_dir, 'mp4info' + ('.exe' if platform.system() == 'Windows' else ''))
MP4DECRYPT = os.path.join(bin_dir, 'mp4decrypt' + ('.exe' if platform.system() == 'Windows' else ''))
MKVMERGE = os.path.join(bin_dir, 'mkvmerge' + ('.exe' if platform.system() == 'Windows' else ''))

if platform.system() != 'Windows':
    FFMPEG = 'ffmpeg'
    MKVMERGE = 'mkvmerge'


class WVTool(object):

    @classmethod
    def m3u8dl_download(cls, url, temp_dir, savename, headers=None, segment=True, retry_segment=True):
        try:
            filepath = os.path.join(temp_dir, savename + '.mp4')
            filepath_sub = os.path.join(temp_dir, savename + '.mkv')
            if os.path.exists(filepath) or os.path.exists(filepath_sub):
                return True
            command = [M3U8DL]
            if headers is not None:
                for key, value in headers.items():
                    if key.lower() == 'accept-encoding':
                        continue
                    value = value.replace('"', '\\"')
                    command.append('--header="%s:%s"' % (key, value))
            if platform.system() == 'Windows':
                command += [f'"{url}"', '--auto-select', '--no-log', '--save-dir', temp_dir, '--save-name', savename, '--tmp-dir', temp_dir]
            else:
                command += [url, '--auto-select', '--no-log', '--save-dir',  temp_dir, '--save-name', savename, '--tmp-dir', temp_dir]

            tool_subprocess = ToolSubprocess()
            result = tool_subprocess.execute_command_return(command)

            if not result :
                logger.warning("사용자 중지")
                return False

            if os.path.exists(filepath):
                return True
            else:
                time.sleep(2)
                if os.path.exists(filepath):
                    return True
            if not os.path.exists(filepath):
                logger.error("ERROR")
            return os.path.exists(filepath)
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            logger.error(traceback.format_exc())
            return False


    @classmethod
    def convert_headers_to_string(cls, headers):
        header_strings = [] 
        for key, value in headers.items():
            header_string = f"{key}: {value}"  
            header_strings.append(header_string)  
            
        return '\n'.join(header_strings)
    
    @classmethod
    def mp4dump(cls, source, target):
        try:
            if os.path.exists(target):
                return
            command = [MP4DUMP, source, '>', target]
            os.system(' '.join(command))
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 
    
    @classmethod
    def mp4info(cls, source, target):
        try:
            if os.path.exists(target):
                return
            command = [MP4INFO, '--format', 'json', source, '>', target]
            os.system(' '.join(command))
        except Exception as exceptieon: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 

    @classmethod
    def mp4decrypt(cls, source, target, kid, key):
        try:
            if os.path.exists(target) or kid is None or key is None:
                return
            command = [MP4DECRYPT, '--key', '%s:%s' % (kid, key), source, target]
            os.system(' '.join(command))
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 


    @classmethod
    def write_file(cls, filename, data):
        try:
            import codecs
            ofp = codecs.open(filename, 'w', encoding='utf8')
            ofp.write(data)
            ofp.close()
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 

    @classmethod
    def read_file(cls, filename):
        try:
            ifp = codecs.open(filename, 'r', encoding='utf8')
            data = ifp.read()
            ifp.close()
            return data
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())



    @classmethod
    def write_json(cls, filepath, data):
        try:
            if os.path.exists(os.path.dirname(filepath)) == False:
                os.makedirs(os.path.dirname(filepath))
            with open(filepath, "w", encoding='utf8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 
    
    @classmethod
    def read_json(cls, filepath):
        try:
            with open(filepath, "r", encoding='utf8') as json_file:
                data = json.load(json_file)
                return data
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc()) 


    @classmethod
    def ffmpeg_copy(cls, source, target):
        try:
            if os.path.exists(target):
                return
            command = [FFMPEG, '-y', '-i', source, '-c', 'copy', target]
            os.system(' '.join(command))
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())


    @classmethod
    def ffmpeg_merge(cls, command):
        try:
            command = [FFMPEG] + command
            subprocess.run(command)
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())


