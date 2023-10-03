#!/usr/bin/env python
# (C) Copyright 2023 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


import io
import os

import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(file_path, encoding="utf-8").read()


package_name = "climetlab_wekeo_clms"  # noqa: E501

version = None
lines = read(f"{package_name}/version").split("\n")
if lines:
    version = lines[0]

assert version


extras_require = {}

setuptools.setup(
    name=package_name,
    version=version,
    description=(
        "A dataset plugin for climetlab for the dataset wekeo-clms"  # noqa: E501
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Germano Guerrini",
    author_email="germano.guerrini@exprivia.com",
    url="http://github.com/wekeo/climetlab-wekeo-clms",
    license="Apache License Version 2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "climetlab>=0.10.0",
        "climetlab-wekeo-source",
    ],
    extras_require=extras_require,
    zip_safe=True,
    entry_points={
        "climetlab.datasets": [
            # End-users will use cml.load_dataset("wekeo-clms", ...)
            # see the tests/ folder for a example.
            "wekeo-clms-cgls-continents-wb-v1-1km=climetlab_wekeo_clms.cgls_continents_wb_v1_1km:cgls_continents_wb_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-daily10-lst-dc-global-v1=climetlab_wekeo_clms.cgls_daily10_lst_dc_global_v1:cgls_daily10_lst_dc_global_v1",  # noqa: E501
            "wekeo-clms-cgls-daily10-lst-dc-global-v2=climetlab_wekeo_clms.cgls_daily10_lst_dc_global_v2:cgls_daily10_lst_dc_global_v2",  # noqa: E501
            "wekeo-clms-cgls-daily10-lst-tci-global-v1=climetlab_wekeo_clms.cgls_daily10_lst_tci_global_v1:cgls_daily10_lst_tci_global_v1",  # noqa: E501
            "wekeo-clms-cgls-daily10-lst-tci-global-v2=climetlab_wekeo_clms.cgls_daily10_lst_tci_global_v2:cgls_daily10_lst_tci_global_v2",  # noqa: E501
            "wekeo-clms-cgls-global-albh-v1-1km=climetlab_wekeo_clms.cgls_global_albh_v1_1km:cgls_global_albh_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-global-aldh-v1-1km=climetlab_wekeo_clms.cgls_global_aldh_v1_1km:cgls_global_aldh_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-global-ba300-v1-333m=climetlab_wekeo_clms.cgls_global_ba300_v1_333m:cgls_global_ba300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-ba300-v3=climetlab_wekeo_clms.cgls_global_ba300_v3:cgls_global_ba300_v3",  # noqa: E501
            "wekeo-clms-cgls-global-dmp-v2-1km=climetlab_wekeo_clms.cgls_global_dmp_v2_1km:cgls_global_dmp_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-dmp300-v1-333m=climetlab_wekeo_clms.cgls_global_dmp300_v1_333m:cgls_global_dmp300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-fapar-v1-1km=climetlab_wekeo_clms.cgls_global_fapar_v1_1km:cgls_global_fapar_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-global-fapar-v2-1km=climetlab_wekeo_clms.cgls_global_fapar_v2_1km:cgls_global_fapar_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-fapar300-v1-333m=climetlab_wekeo_clms.cgls_global_fapar300_v1_333m:cgls_global_fapar300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-fcover-v1-1km=climetlab_wekeo_clms.cgls_global_fcover_v1_1km:cgls_global_fcover_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-global-fcover-v2-1km=climetlab_wekeo_clms.cgls_global_fcover_v2_1km:cgls_global_fcover_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-fcover300-v1-333m=climetlab_wekeo_clms.cgls_global_fcover300_v1_333m:cgls_global_fcover300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-gdmp-v2-1km=climetlab_wekeo_clms.cgls_global_gdmp_v2_1km:cgls_global_gdmp_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-gdmp300-v1-333m=climetlab_wekeo_clms.cgls_global_gdmp300_v1_333m:cgls_global_gdmp300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-lai-v1-1km=climetlab_wekeo_clms.cgls_global_lai_v1_1km:cgls_global_lai_v1_1km",  # noqa: E501
            "wekeo-clms-cgls-global-lai-v2-1km=climetlab_wekeo_clms.cgls_global_lai_v2_1km:cgls_global_lai_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-lai300-v1-333m=climetlab_wekeo_clms.cgls_global_lai300_v1_333m:cgls_global_lai300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi-st=climetlab_wekeo_clms.cgls_global_ndvi_st:cgls_global_ndvi_st",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi-v2-1km-lts=climetlab_wekeo_clms.cgls_global_ndvi_v2_1km_lts:cgls_global_ndvi_v2_1km_lts",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi-v2-1km=climetlab_wekeo_clms.cgls_global_ndvi_v2_1km:cgls_global_ndvi_v2_1km",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi-v3-1km=climetlab_wekeo_clms.cgls_global_ndvi_v3_1km:cgls_global_ndvi_v3_1km",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi300-v1-333m=climetlab_wekeo_clms.cgls_global_ndvi300_v1_333m:cgls_global_ndvi300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-global-ndvi300-v2-333m=climetlab_wekeo_clms.cgls_global_ndvi300_v2_333m:cgls_global_ndvi300_v2_333m",  # noqa: E501
            "wekeo-clms-cgls-global-swi-static-v1-0-1degree=climetlab_wekeo_clms.cgls_global_swi_static_v1_0_1degree:cgls_global_swi_static_v1_0_1degree",  # noqa: E501
            "wekeo-clms-cgls-global-swi10-v3-0-1degree=climetlab_wekeo_clms.cgls_global_swi10_v3_0_1degree:cgls_global_swi10_v3_0_1degree",  # noqa: E501
            "wekeo-clms-cgls-global-wb300-v1-333m=climetlab_wekeo_clms.cgls_global_wb300_v1_333m:cgls_global_wb300_v1_333m",  # noqa: E501
            "wekeo-clms-cgls-hourly-lst-global-v1=climetlab_wekeo_clms.cgls_hourly_lst_global_v1:cgls_hourly_lst_global_v1",  # noqa: E501
            "wekeo-clms-cgls-hourly-lst-global-v2=climetlab_wekeo_clms.cgls_hourly_lst_global_v2:cgls_hourly_lst_global_v2",  # noqa: E501
        ]
        # source plugins would be here
        # "climetlab.sources": []
    },
    keywords="meteorology",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
    ],
)
