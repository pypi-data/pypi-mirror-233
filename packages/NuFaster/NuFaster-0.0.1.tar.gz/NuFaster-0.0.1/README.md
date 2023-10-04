# NuitkaPackV2

## 更快的使用Nuitka打包 (Faster! Exclude first time)

原理: 分模块打包

## Demo

Run "toPack-main1002.py" toPack -> "main1002.py"

## Usage

```python
# 设置打包本地缓存目录
from NuFaster import set_save_dir

set_save_dir(r'OutputDir')  # 修改缓存库文件保存位置

```

```python
# 运行打包
from NuFaster.to_pack import to_pack_main

dependent_libs = [
    'requests', 'numpy'
]  # 项目中依赖的模块, 分开打包的模块

to_pack_main(
        'main.py',          # 打包文件
        dependent_libs,     # 分开打包的模块
        
        # 接下来的参数和Nuitka的参数是一样的, 如果使用关键字需要 去掉开头的"--" 和将"-"转化为"_"
        # 例如: --windows-icon-from-ico, 要换为 windows_icon_from_ico
        output_dir=None,    
        standalone=True,    # bool
        mingw=True,         # 
)
```


## 