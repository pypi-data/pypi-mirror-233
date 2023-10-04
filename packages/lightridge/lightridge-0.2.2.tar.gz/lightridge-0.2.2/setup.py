from setuptools import setup

setup(
   name='lightridge',
   version='0.2.2',
   author='Yingjie Li, Cunxi Yu (University of Maryland, College Park)',
   author_email='yingjiel@umd.edu',
   packages=['lightridge'],
   url='https://lightridge.github.io/lightridge/',
   license='LICENSE',
   description=' LightRidge — An Open-Source Hardware Project for Optical AI!',
   long_description="LightRidge is an open-source framework for end-to-end optical machine learning (ML) compilation, which connects physics to system. It is specifically designed for diffractive optical computing, offering a comprehensive set of features (Check out our ASPLOS’23 at https://arxiv.org/abs/2306.11268): (1) Precise and differentiable optical physics kernels: LightRidge empowers researchers and developers to explore and optimize diffractive optical neural network (DONN) architectures. With built-in, accurate, and differentiable optical physics kernels, users can achieve complete and detailed analyses of DONN performance. (2) Accelerated optical physics computation kernel streamlines the development process and boosts the efficiency of optical ML workflows. (3) Versatile and flexible optical system modeling: LightRidge provides a rich set of tools for modeling and simulating optical systems. Researchers can create complex optical setups, simulate light propagation, and analyze system behavior using LightRidge’s versatile capabilities. (4) User-friendly domain-specific language (DSL): LightRidge includes a user-friendly DSL, enabling users to describe and configure diffractive optical networks easily. The DSL simplifies the implementation process and facilitates rapid prototyping of novel optical ML models. LightRidge website is https://lightridge.github.io/lightridge",
   install_requires=[
       "torch>=1.12.0",
       "torchvision>=0.13.0",
       "setuptools>=42",
       "pandas",
       "tqdm",
       "lightpipes"
   ],
)


