import traceback

import pkg_resources


def get_top_level(library_name):
    distribution = pkg_resources.get_distribution(library_name)
    return distribution.get_metadata_lines("top_level.txt")


def get_top_level_name(library_name):
    try:
        return list(get_top_level(library_name))[0]
    except:
        return library_name


# def get_dependencies(library_name):
#     try:
#         # 获取指定库的分发信息
#         distribution = pkg_resources.get_distribution(library_name)
#         depand_library_list = []
#         # 获取依赖库列表
#         dependencies = distribution.requires()
#         for depand in dependencies:
#             depand_library_list.append(get_top_level_name(depand.project_name))
#         return depand_library_list
#     except pkg_resources.DistributionNotFound:
#         # 如果找不到指定库，可以处理异常或返回错误消息
#         print(f"Library '{library_name}' not found.")
#         return []


def get_dependencies(library_name):
    try:
        # 获取指定库的分发信息
        distribution = pkg_resources.get_distribution(library_name)
        depand_library_list = []
        # 获取依赖库列表
        dependencies = distribution.requires()
        for depand in dependencies:
            # depand_library_list.append(get_top_level_name(depand.project_name))
            depand_library_list.append(depand.project_name)
        return depand_library_list
    except pkg_resources.DistributionNotFound:
        # 如果找不到指定库，可以处理异常或返回错误消息
        print(f"Library '{library_name}' not found.")
        return []


def get_version(library_name):
    try:
        # 获取指定库的分发信息
        distribution = pkg_resources.get_distribution(library_name)
        depand_library_list = []
        # 获取依赖库列表
        return distribution.version
    
    except pkg_resources.DistributionNotFound:
        traceback.print_exc()
        # 如果找不到指定库，可以处理异常或返回错误消息
        print(f"Library '{library_name}' not found.")
        return '0.0.0'


if __name__ == "__main__":
    """
    """
    
    