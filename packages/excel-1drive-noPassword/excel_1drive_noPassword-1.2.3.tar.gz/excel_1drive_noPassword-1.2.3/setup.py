from setuptools import setup, find_packages

setup(
    name='excel_1drive_noPassword',
    version='1.2.3',
    description='Package to download and manipulate Excel files from OneDrive URLs that are set to *accessible by anyone with the URL*',
    author='Abhishek Venkatachalam',
    author_email='abhishek.venkatachalam06@gmail.com',
    url='https://github.com/abhishekvenkat764/excel_1drive_noPassword',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'beautifulsoup4',
        're',
        'html',
        'json',
        'urllib',
    ],
)
