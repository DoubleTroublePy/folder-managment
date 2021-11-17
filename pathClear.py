from os import listdir, mkdir, path
import shutil


class PathClear:
    val_path = ''
    options_path = ''
    paths = {
        'png': 'images',
        'svg': 'images',
        'jpeg': 'images',
        'app': 'app',
        'pdf': 'pdf',
        'dmg': 'dmg',
        'html': 'html',
        'doc': 'documenti',
        'zip': 'zip',
        'folders': 'folders',
        'all': 'shit',
    }
    
    def __init__(self, val_path: str = None, paths: dict = None) -> None:
        if val_path:
            self.val_path = val_path
        if paths:
            self.paths = paths
    
    def path_clear(self) -> None:
        def create_directory(path):
            try:
                mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)
            else:
                print("Successfully created the directory %s " % path)
            
        for f in listdir(self.val_path):
            flag = False
            sub = ''
            for sub_f in f:
                if sub_f == '.':
                    sub = ''
                    flag = True
                elif flag:
                    sub += sub_f

            start_path = self.val_path + '/' + f
            val_path = None

            if sub in self.paths:
                val_path = self.val_path + '/' + self.paths[sub]
            elif sub != '':
                val_path = self.val_path + '/shit'
            elif not(f in self.paths.values()) or val_path == '':
                val_path = self.val_path + '/folders'
            if val_path is not None:
                if not path.exists(val_path):
                    create_directory(val_path)
                shutil.move(start_path, val_path + '/' + f)

    def update_paths(self, paths: dir) -> None:
        self.paths = paths

    def auto_update_paths(self):
        key = ''
        value = ''
        paths = {}
        flag = True

        with open(self.options_path, 'r') as f:
            for line in f:  
                for ch in line: 
                    if ch == ':':
                        flag = False
                    if ch == ',': 
                        paths[key] = value
                        flag = True 
                        key = ''
                        value = ''
                    elif flag and ch != ' ':
                        key += ch
                    elif ch != ':' and ch != ' ':
                        value += ch
        self.paths = paths
    
    def add_file_type(self, key: str, value: str) -> None:
        self.paths[key] = value

    def del_file_type(self, key: str) -> bool:
        return self.paths.pop(key)

    def print_path(self):
        for val in self.paths:
            print(val, end=' ')
        print()
