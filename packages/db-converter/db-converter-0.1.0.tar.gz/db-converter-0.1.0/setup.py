from setuptools import setup, find_packages

setup(
    name='db-converter',  # Kütüphane ismi
    version='0.1.0',  # Versiyon numarası
    packages=find_packages(),  # Dahil edilecek paketlerin listesi
    url='https://github.com/mertcelikan/db-converter',
    install_requires=[  # Gerekli bağımlılıklar
        'numpy',
        'pandas',
        'pymongo',
        'PyMySQL',
        'python-dateutil',
        'pytz',
        'six',
        'dnspython'
    ],
)
