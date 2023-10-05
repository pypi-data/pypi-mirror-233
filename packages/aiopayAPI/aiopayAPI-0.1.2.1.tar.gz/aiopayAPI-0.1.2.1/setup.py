from setuptools import setup, find_packages


with open('README.md', encoding="utf-8") as f:
  long_description = f.read()


setup(
  name='aiopayAPI',
  version='0.1.2.1',
  author='xllebbSQ',
  author_email='090504opo@gmail.com',
  description='Асинхронный API для работы с платежной системой Payok.io.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/xllebbSQ/aiopay',
  packages=find_packages(),
  install_requires=['aiohttp>=3.8.5',
                    "asyncio>=3.4.3",
                    "hashlib>=20081119"],
  classifiers=[
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python PayOk payok api API ayncio payok api',
  project_urls={
    'GitHub': 'https://github.com/xllebbSQ'
  },
  python_requires='>=3.8'
)