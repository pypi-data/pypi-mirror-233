import shutil
import sys
from pathlib import Path

from NuFaster.get_library_depand import get_version, get_dependencies, get_top_level_name
from NuFaster.to_pack import get_pyd_file, get_dll_file
from NuFaster.setting import Default_module_dir
from NuFaster.tools import copy

py_version = sys.winver


class Library:
    
    def __init__(self, library_name, auto_generate=True):
        self.library_name = library_name
        self.name = get_top_level_name(library_name)
        self.auto_generate = auto_generate
        
        if self.version == '0.0.0':
            print(f'找不到{library_name}版本信息')
    
    def check_dependencies(self):
        """检查依赖库文件"""
        for lib in self.dependencies:
            print(f'检查依赖库: {lib}')
            lib_pyd = lib.pyd
            lib_dll = lib.dll_dir
            
            lib.check_dependencies()
            
            dep_pyd = self.dll_dir.joinpath(lib_pyd.name)
            
            if not dep_pyd.exists():
                print('复制依赖库的pyd文件')
                dep_pyd.parent.mkdir(parents=True, exist_ok=True)
                copy(lib_pyd, dep_pyd, )
                # shutil.copy(lib_pyd, dep_pyd, )
            
            # shutil.copytree(lib_dll, self.dll_dir, ignore_dangling_symlinks=True, dirs_exist_ok=True)
            
            for file in lib_dll.rglob('*'):
                relative = file.relative_to(lib_dll)
                
                dep_file = self.dll_dir.joinpath(relative)
                if dep_file.exists() and dep_file.stat().st_size == file.stat().st_size:
                    pass
                else:
                    # print(f'复制依赖库的dll文件:{relative}  {file} {file.exists()} -> {dep_file}')
                    print(f'复制依赖库的dll文件: {relative}')
                    dep_file.parent.mkdir(parents=True, exist_ok=True)
                    copy(file, dep_file)
                    # if file.is_file():
                    #     shutil.copy(file, dep_file)
                    # else:
                    #     shutil.copytree(file, dep_file, dirs_exist_ok=True)
    
    def reload_dll_file(self):
        shutil.rmtree(self.dll_dir, ignore_errors=True, )
        self.check_dependencies()
    
    @property
    def version(self):
        return get_version(self.library_name)
    
    @property
    def library_file(self):
        try:
            __import__(self.name)
        except ImportError as e:
            raise ImportError(f'{self.name}模块导入失败:{e}')
        module_info = sys.modules.get(self.name)
        return module_info.__file__
    
    @property
    def dependencies(self):
        res_list = []
        dependencies = get_dependencies(self.library_name)
        for lib in dependencies:
            res_list.append(Library(lib, auto_generate=self.auto_generate))
        return res_list
    
    @property
    def dependenciesName(self):
        res_list = []
        dependencies = get_dependencies(self.name)
        for lib in dependencies:
            res_list.append(get_top_level_name(lib))
        return res_list
    
    @property
    def dll_dir(self):
        dll_dir = Path(Default_module_dir.str()).joinpath(py_version, self.name, str(self.version), 'Dll')
        if dll_dir.exists():
            return dll_dir
        else:
            if not self.auto_generate:
                ok = input('当前不存在{self.name}的dll文件, 是否要生成0(否), 1(是):')
                if ok != '1':
                    return
            print(f'\n{self} 获取模块dll文件中')
            lib_dll_dir = get_dll_file(self.library_name)
            for file in Path(lib_dll_dir).rglob('*'):
                p_file = file
                relative = p_file.relative_to(lib_dll_dir)
                p_dll_file = Path(dll_dir).joinpath(relative)
                
                if not p_dll_file.exists():
                    p_dll_file.parent.mkdir(parents=True, exist_ok=True)
                    copy(p_file, p_dll_file)
                    # if p_file.is_file():
                    #     shutil.copy(p_file, p_dll_file)
                    # else:
                    #     shutil.copytree(p_file, p_dll_file)
        
        return dll_dir
    
    @property
    def pyd(self):
        pyd_name = f'{self.name}.pyd'
        pyd_file = Path(Default_module_dir).joinpath(py_version, self.name, str(self.version), pyd_name)
        if pyd_file.exists():
            return pyd_file
        else:
            if not self.auto_generate:
                ok = input('当前不存在{self.name}的pyd文件, 是否要生成0(否), 1(是):')
                if ok != '1':
                    return
            print(f'\n{self} 打包模块pyd文件中')
            pyd_file.parent.mkdir(parents=True, exist_ok=True)
            file = get_pyd_file(self.library_name)
            copy(file, pyd_file)
            # shutil.copy(file, pyd_file)
        return pyd_file
    
    def __str__(self):
        return f'< library: {self.name} >'


if __name__ == '__main__':
    """
    Main run
    """
    library = Library('pandas')
    print(library)
    # dll_ = library.dll_dir
    # print(dll_, dll_.exists())
    # pyd_ = library.pyd
    # print(pyd_, pyd_.exists())
    # library.check_dependencies()
