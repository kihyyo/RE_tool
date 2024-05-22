import subprocess
import threading
import platform
import json
import traceback

from support import SupportSubprocess, get_logger
logger = get_logger()

class ToolSubprocess(object):
    __idx = 1
    __instance_list = []

    def __init__(self):
        self.idx = str(ToolSubprocess.__idx)
        ToolSubprocess.__idx += 1
        ToolSubprocess.__instance_list.append(self)
        self.stop_flag = threading.Event()  # Use instance-specific stop flag
        self.process = None

    @classmethod
    def get_list(cls):
        return cls.__instance_list
    
    def stop(self):
        self.stop_flag.set()  # Set the stop flag for this instance
        if self.process:
            try:
                self.process.terminate()  # Terminate the subprocess
            except Exception as e:
                logger.error(f"Failed to terminate process: {str(e)}")
                logger.error(traceback.format_exc())
            finally:
                self.process = None  # Set the process to None in any case


    def execute_command_return(self, command, format=None, force_log=False, shell=False, env=None, timeout=1800):
        try:
            if platform.system() == 'Windows':
                command = ' '.join(command)

            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                shell=shell,
                env=env,
                encoding='utf8'
            )

            ret = []
            try:
                while True:
                    line = self.process.stdout.readline()
                    if line == '' or (self.process and self.process.poll() is not None):
                        break
                    if line:
                        logger.info(line.strip())
                        ret.append(line.strip())
                        if force_log:
                            logger.debug(line.strip())
                    
                    if self.stop_flag.is_set():
                        logger.warning("사용자 중지")
                        return False
                if self.process:
                    self.process.stdout.close()
                    self.process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                self.process.kill()
                return "timeout"

            if format is None:
                ret2 = '\n'.join(ret)
            elif format == 'json':
                try:
                    index = 0
                    for idx, tmp in enumerate(ret):
                        if tmp.startswith('{') or tmp.startswith('['):
                            index = idx
                            break
                    ret2 = json.loads(''.join(ret[index:]))
                except json.JSONDecodeError:
                    ret2 = None

            return ret2
        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            logger.error(traceback.format_exc())
            logger.error('command: %s', command)
            return None