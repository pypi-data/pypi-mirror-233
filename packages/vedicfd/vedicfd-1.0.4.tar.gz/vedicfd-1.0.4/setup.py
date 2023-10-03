from setuptools import setup, find_packages

setup(
    name='vedicfd',
    version='1.0.4',
    author='USP',
    author_email='pathakumashankar@hotmail.com',
    description='detect faces',
    # long_description='A longer description of your package',
    # url='https://github.com/yourusername/your_package_name',
    packages=find_packages(),
    install_requires=[
        'opencv-python-headless', 'requests' , 'face_recognition', 'pickle4', 'pytube'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
