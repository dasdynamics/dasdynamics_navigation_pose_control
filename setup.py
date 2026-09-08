import os
from glob import glob
from setuptools import setup


package_name = 'dasdynamics_navigation'


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
    install_requires=[],
    zip_safe=False,
    maintainer='dmitry-savin-dev',
    maintainer_email='das-dev-md@mail.ru',
    description='Launch files for navigation and a waypoint control node',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'waypoints_control_node = dasdynamics_navigation.waypoints_control_node:main'
        ],
    },
)
