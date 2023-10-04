# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afids_cnn',
 'afids_cnn.apply_workflow',
 'afids_cnn.train_workflow',
 'afids_cnn.train_workflow.workflow.scripts']

package_data = \
{'': ['*'],
 'afids_cnn': ['resources/*'],
 'afids_cnn.apply_workflow': ['config/*', 'workflow/*'],
 'afids_cnn.train_workflow': ['config/*', 'workflow/*']}

install_requires = \
['keras>=2.12.0,<3.0.0',
 'numpy>=1.22,<1.24',
 'pandas>=1.3,<2',
 'scikit-image>=0.19.3,<0.20.0',
 'snakebids>=0.9.0,<0.10.0',
 'tensorflow>=2.12.0,<3.0.0',
 'torch>=1.13.1,<3.0.0']

entry_points = \
{'console_scripts': ['auto_afids_cnn_apply = afids_cnn.apply:main',
                     'auto_afids_cnn_apply_bids = '
                     'afids_cnn.apply_workflow.run:main',
                     'auto_afids_cnn_train = afids_cnn.train:main',
                     'auto_afids_cnn_train_bids = '
                     'afids_cnn.train_workflow.run:main']}

setup_kwargs = {
    'name': 'afids-cnn',
    'version': '0.2.1',
    'description': '',
    'long_description': '# afids-NN\nUtilizing the anatomical fiducals framework to identify other salient brain regions and automatic localization of anatomical fiducials using neural networks\n\n\n# Processing data for training \n\nConvert3D\n\n## Anatomical landmark data (AFIDs)\n\nConvert3D:\n1) .fcsv -> threshold image -> landmark distance map (could be considered probability map) \n2) distance map used for training \n\n## Structural T1w imaging \n\nConvert3D: \n1) brainmask.nii -> 3D patches sampled at x voxels \n2) matching of distance maps and anatomical imaging patches is crucial for proper training \n\n\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
