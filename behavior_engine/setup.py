import os
from setuptools import setup
from catkin_pkg import python_setup

package_xml = python_setup.generate_distutils_setup("./package.xml")


def package_data_files(dir_list):
    prefix_path = os.path.join('src', package_xml['name'])
    data_files = []

    for directory in dir_list:
        # Recursive-Search files
        start_point = os.path.join(prefix_path, directory)
        for root, dirs, files in os.walk(start_point):
            for file_name in files:
                # Append file path that is removed prefix path (e.g. 'src/pkgname/aaa.txt' -> 'aaa.txt')
                data_files.append(
                    os.path.join(root, file_name)[len(prefix_path) + 1:])

    return data_files


setup(
    version=package_xml['version'],
    packages=[package_xml['name']],
    package_dir={'': 'src'},
    package_data={package_xml['name']: package_data_files(['actions'])})

