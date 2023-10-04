pack_root = f'{__file__}/../pack_dir/Record'


class Dir(str):
    
    def __init__(self, sub_dir):
        self.sub_dir = sub_dir
    
    def str(self):
        return self.__str__()
    
    def __str__(self):
        return fr'{pack_root}\{self.sub_dir}'


Default_build_dir = Dir('Build')  # 默认打包路径
Default_module_dir = Dir('Module')  # 默认打包路径
