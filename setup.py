from setuptools import setup, find_packages

setup(
    name="MinecraftProcessManager",
    version="0.1",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'start_process_manager = minecraft.launcher:main'
        ]
    },
    author="Cameron Alberts",
    python_requires='>=3',
    author_email="alberts.cameron@gmail.com",
    description="Process manager to keep your minecraft server healthy and running",
    keywords="minecraft server process manager",
    url="https://github.com/Cameron-Alberts/MinecraftProcessManager",
    classifiers=[
        'License :: MIT License'
    ]
)