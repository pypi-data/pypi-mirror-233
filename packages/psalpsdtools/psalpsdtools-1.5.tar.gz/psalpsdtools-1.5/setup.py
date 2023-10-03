from setuptools import setup

setup(name='psalpsdtools',
      version='1.5',
      description='PSA-LPSD Tools',
      packages=['psalpsdtools'],
      install_requires=[
          'pip',
          'openpyxl',
      ],
      author_email='a.diaziii@psa.gov.ph',
      long_description=open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/tondiaz/psalpsdtools',
      zip_safe=False)
