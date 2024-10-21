import os, json, requests
from urllib.parse import unquote
import pathlib, shutil
from zipfile import ZipFile
import psutil
import platform

### user 
from modules.user.api import Api_SH


URI = 'http://192.168.7.108:9999/'
AUTH_URL ='http://192.168.7.108:9999/api-auth/jwt/'
url ="messagebox/chat-file/"

class Update():
    def __init__(self):
        self.latest_Info = {}
        self._info = {}
        self.read_info()        
        self.suffix = '?page_size=0'
        self.is_Run = True
        self.pid_UpdateName = 'update_pid'
        self.pid_MainName = 'main_pid'

    def run(self):        
        while self.is_Run:
            self.update_routine()
    
    def update_routine(self):
        self.get_info_from_api()
        if self.check_version :
            if (path := self.get_latestFile() ) is not None:
                if ( self.check_stop_this_process_running() ):
                    self.extract(path=path)
                    self.restart_Main_App()
        return True

    def stop(self):
        self.is_Run = False
        return True

    def read_info(self):
        with open('./_info.json', 'r') as f:
            self._info = json.load(f)
        # print ( self._info)
    
    def get_info_from_api(self):
        api = Api_SH()
        info_list = api.getlist( url+ self.suffix )
        # print ( type(info_list), info_list )
        self.latest_Info = info_list[-1]
    
    def check_version(self):
        if self.latest_Info.get('version') == self._info.get('version') :
            return False
        else: return True

    def get_latestFile(self):
        response = requests.get( self.latest_Info.get('file'))
        if response.status_code == 200:
            pathlib.Path('./download').mkdir(parents=True, exist_ok=True)
            # print ( response.headers)
            # print (response.headers.get("Content-Disposition") )

            if 'utf-8' in ( raw := response.headers.get("Content-Disposition") ) :
                raw_fname = raw.split("filename*=")[1]
                fName = unquote(raw_fname.replace("utf-8''", ""))
            else :
                raw_fname = raw.split("filename=")[1]
                fName = raw_fname.replace('"','' )

            path = './download/'+fName
            with open(path, 'wb') as download:
                download.write(response.content)
            
            return path

        else:
            print ('error')
            return None

    #### update는 zip file로 ==> EXE FILE시, 실행에???
    def extract(self, path):

        if path is not None:

            application_path = os.path.dirname(os.path.realpath(__file__))
            print ( path, 'is Extracting to ', application_path)

            with ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(application_path) )

            # with ZipFile(path, 'r') as z:
            #     for file_info in z.infolist():
            #         print ( file_info)
            #         # Only extract regular files
            #         if file_info.is_dir():
            #             continue

            #         file_path = file_info.filename
            #         # Only extract things under 'Content/'
            #         if not file_path.startswith('Content/'):
            #             continue

            #         # Split at slashes, at most one time, and take the second part
            #         # so that we skip the 'Content/' part
            #         extracted_path = file_path.split('/', 1)[1]

            #         # Combine with the destination directory
            #         extracted_path = os.path.join(application_path, extracted_path)
            #         print(extracted_path)

            #         # Make sure the directory for the file exists
            #         os.makedirs(os.path.dirname(extracted_path), exist_ok=True)

            #         # Extract the file. Don't use `z.extract` as it will concatenate
            #         # the full path from inside the zip.
            #         # WARNING: This code does not check for path traversal vulnerabilities
            #         # Refer to the big warning inside the ZipFile module for more details
            #         with open(extracted_path, 'wb') as dst:
            #             with z.open(file_info, 'r') as src:
            #                 shutil.copyfileobj(src, dst)

    def check_stop_this_process_running(self):
        self.read_info()   
        if (pid_main := self._info.get(self.pid_MainName, None) ) is not None:
            if psutil.pid_exists(pid_main):
                return self.kill_pid(pid_main)
        return True


        # print ( self.pid )
        # print('Running Processes \n')
        # print ( platform.system() )
        # match ( os_name := platform.system() ):
        #     case 'Windows':
        #         process_name = 'python.exe'
        #     case 'Linux':
        #         process_name = 'python'
        #     case _:
        #         process_name = 'python'

        # processes = [p.cmdline() for p in psutil.process_iter() if p.name().lower() in [process_name] and  'main.py' in p.cmdline()[1] ]

        # for p in psutil.process_iter():
        #     if process_name in p.name():
        #         print ( p, p.cmdline() )
        # print ( processes )

    def kill_pid(self, pid=int):
        p = psutil.Process(pid)
        try :
            p.terminate()
            print ( f'Kill Process Success : pid = {pid} \n')
            return True
        except Exception as e:
            print ( f'Kill Process Error: pid = {pid}, error={e}\n')
            return False


    def restart_Main_App(self):
        import subprocess
        try:
            subprocess.call ( ['python', './main.py'])
            return True
        except Exception as e:
            print ( 'Main App 실행 오류 : ', e)
            return False
        # self.stop()
        # return None

    def get_File(self):
        response = requests.get( self.latest_Info.get('file'))
        if response.status_code == 200:
            pathlib.Path('./download').mkdir(parents=True, exist_ok=True)
            # print ( response.headers)

            # print (response.headers.get("Content-Disposition") )
            # print ( response.headers.get("Content-Disposition").split("filename*="))

            raw_fname = response.headers.get("Content-Disposition").split("filename*=")[1]
            if 'utf-8' in raw_fname:
                fName = unquote(raw_fname.replace("utf-8''", ""))
            else : fName = raw_fname

            with open('./download/'+fName, 'wb') as download:
                download.write(response.content)

        else:
            print ('error')

    def get_pid_wrte_infojson(self, pid=str):
        try : 
            with open('./_info.json', 'r') as f:
                info_contents = json.load(f)
        except Exception as e:
            print ('json_file open error: ', e)
            return False

        pid_json = {pid:os.getpid()}

        info_contents.update(pid_json)

        with open('./_info.json', 'w') as f:
            json.dump(info_contents, f, ensure_ascii=False)

        return True


# def main():    
#     update = Update()
#     update.run()


#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = MyWindow()
#     # ui = Ui_MainWindow()
#     # ui.setupUi(MainWindow)
#     # MainWindow.show()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
