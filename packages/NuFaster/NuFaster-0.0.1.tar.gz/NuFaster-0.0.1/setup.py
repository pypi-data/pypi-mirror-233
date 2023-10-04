from setuptools import setup, find_packages

setup(
        name='NuFaster',  # 包的名称
        version='0.0.1',  # 版本号
        author='toca-Y',  # 作者名字
        author_email='',  # 作者邮箱
        description='借助nuitka更快的打包(分模块打包)',  # 包的简短描述
        long_description='分模块打包',  # 包的详细描述
        url='https://github.com/toca-Y/NuitkaPackV2',  # 包的主页或仓库链接
        packages=find_packages(),  # 寻找和包含所有的 Python 包
        install_requires=[
            'nuitka==1.5.8'
        ],  # 依赖项列表，如果有的话
        classifiers=[  # 包的分类
        ],
)
