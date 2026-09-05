import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dasdynamics_navigation_pose_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dmitry-savin-dev',
    maintainer_email='das-dev-dt@mail.ru',
    description='TODO: Package description',
    license='TODO: License declaration',

    entry_points={
        'console_scripts': [
            'pose_save_node = dasdynamics_navigation_pose_control.pose_save_node:main'
        ],
    },
)
