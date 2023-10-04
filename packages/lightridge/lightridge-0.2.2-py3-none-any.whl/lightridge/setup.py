from setuptools import setup

setup(
   name='lightridge',
   version='0.1.7',
   author='Yingjie Li, Minhan Lou, Ruiyang Chen, Weilu Gao, Cunxi Yu (University of Utah)',
   author_email='cunxi.linux@gmail.com',
   packages=['lightridge'],
   url='https://github.com/ycunxi/lightbridge',
   license='LICENSE.txt',
   description='lightridge Description',
   long_description="TBD",
   install_requires=[
       "torch==1.12.0",
       "torchvision==0.13.0",
       "lightpipes"
   ],
)


