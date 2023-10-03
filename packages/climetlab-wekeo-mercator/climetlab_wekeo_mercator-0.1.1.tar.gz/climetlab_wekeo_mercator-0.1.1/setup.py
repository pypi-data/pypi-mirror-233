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


package_name = "climetlab_wekeo_mercator"  # noqa: E501

version = None
lines = read(f"{package_name}/version").split("\n")
if lines:
    version = lines[0]

assert version


extras_require = {"dask": ["dask[complete]"]}

setuptools.setup(
    name=package_name,
    version=version,
    description=(
        "A dataset plugin for climetlab for the dataset wekeo-mercator"  # noqa: E501
    ),
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Germano Guerrini",
    author_email="germano.guerrini@exprivia.com",
    url="http://github.com/wekeo/climetlab-wekeo-mercator",
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
            # End-users will use cml.load_dataset("wekeo-mercator", ...)
            # see the tests/ folder for a example.
            "wekeo-mercator-test-clms=climetlab_wekeo_mercator.test_clms:test_clms",  # noqa: E501
            "wekeo-mercator-arctic-analysis-forecast-phys=climetlab_wekeo_mercator.arctic_analysis_forecast_phys:arctic_analysis_forecast_phys",  # noqa: E501
            "wekeo-mercator-arctic-analysis-forecast-wav=climetlab_wekeo_mercator.arctic_analysis_forecast_wav:arctic_analysis_forecast_wav",  # noqa: E501
            "wekeo-mercator-arctic-analysisforecast-bgc=climetlab_wekeo_mercator.arctic_analysisforecast_bgc:arctic_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-arctic-analysisforecast-phy-ice=climetlab_wekeo_mercator.arctic_analysisforecast_phy_ice:arctic_analysisforecast_phy_ice",  # noqa: E501
            "wekeo-mercator-arctic-analysisforecast-phy-tide=climetlab_wekeo_mercator.arctic_analysisforecast_phy_tide:arctic_analysisforecast_phy_tide",  # noqa: E501
            "wekeo-mercator-arctic-multiyear-bgc=climetlab_wekeo_mercator.arctic_multiyear_bgc:arctic_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-arctic-multiyear-phy=climetlab_wekeo_mercator.arctic_multiyear_phy:arctic_multiyear_phy",  # noqa: E501
            "wekeo-mercator-arctic-multiyear-wav=climetlab_wekeo_mercator.arctic_multiyear_wav:arctic_multiyear_wav",  # noqa: E501
            "wekeo-mercator-balticsea-analysisforecast-bgc=climetlab_wekeo_mercator.balticsea_analysisforecast_bgc:balticsea_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-balticsea-analysisforecast-phy=climetlab_wekeo_mercator.balticsea_analysisforecast_phy:balticsea_analysisforecast_phy",  # noqa: E501
            "wekeo-mercator-balticsea-analysisforecast-wav=climetlab_wekeo_mercator.balticsea_analysisforecast_wav:balticsea_analysisforecast_wav",  # noqa: E501
            "wekeo-mercator-balticsea-multiyear-bgc=climetlab_wekeo_mercator.balticsea_multiyear_bgc:balticsea_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-balticsea-multiyear-phy=climetlab_wekeo_mercator.balticsea_multiyear_phy:balticsea_multiyear_phy",  # noqa: E501
            "wekeo-mercator-balticsea-reanalysis-wav=climetlab_wekeo_mercator.balticsea_reanalysis_wav:balticsea_reanalysis_wav",  # noqa: E501
            "wekeo-mercator-blksea-analysisforecast-bgc=climetlab_wekeo_mercator.blksea_analysisforecast_bgc:blksea_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-blksea-analysisforecast-phy=climetlab_wekeo_mercator.blksea_analysisforecast_phy:blksea_analysisforecast_phy",  # noqa: E501
            "wekeo-mercator-blksea-analysisforecast-wav=climetlab_wekeo_mercator.blksea_analysisforecast_wav:blksea_analysisforecast_wav",  # noqa: E501
            "wekeo-mercator-blksea-multiyear-phy=climetlab_wekeo_mercator.blksea_multiyear_phy:blksea_multiyear_phy",  # noqa: E501
            "wekeo-mercator-blksea-multiyear-wav=climetlab_wekeo_mercator.blksea_multiyear_wav:blksea_multiyear_wav",  # noqa: E501
            "wekeo-mercator-blksea-reanalysis-bio=climetlab_wekeo_mercator.blksea_reanalysis_bio:blksea_reanalysis_bio",  # noqa: E501
            "wekeo-mercator-global-analysis-forecast-bio=climetlab_wekeo_mercator.global_analysis_forecast_bio:global_analysis_forecast_bio",  # noqa: E501
            "wekeo-mercator-global-analysisforecast-phy=climetlab_wekeo_mercator.global_analysisforecast_phy:global_analysisforecast_phy",  # noqa: E501
            "wekeo-mercator-global-analysisforecast-wav=climetlab_wekeo_mercator.global_analysisforecast_wav:global_analysisforecast_wav",  # noqa: E501
            "wekeo-mercator-global-multiyear-bgc=climetlab_wekeo_mercator.global_multiyear_bgc:global_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-global-multiyear-phy=climetlab_wekeo_mercator.global_multiyear_phy:global_multiyear_phy",  # noqa: E501
            "wekeo-mercator-global-multiyear-wav=climetlab_wekeo_mercator.global_multiyear_wav:global_multiyear_wav",  # noqa: E501
            "wekeo-mercator-global-reanalysis-phy=climetlab_wekeo_mercator.global_reanalysis_phy:global_reanalysis_phy",  # noqa: E501
            "wekeo-mercator-ibi-analysis-forecast-wav=climetlab_wekeo_mercator.ibi_analysis_forecast_wav:ibi_analysis_forecast_wav",  # noqa: E501
            "wekeo-mercator-ibi-analysisforecast-bgc=climetlab_wekeo_mercator.ibi_analysisforecast_bgc:ibi_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-ibi-analysisforecast-phy=climetlab_wekeo_mercator.ibi_analysisforecast_phy:ibi_analysisforecast_phy",  # noqa: E501
            "wekeo-mercator-ibi-multiyear-bgc=climetlab_wekeo_mercator.ibi_multiyear_bgc:ibi_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-ibi-multiyear-phy=climetlab_wekeo_mercator.ibi_multiyear_phy:ibi_multiyear_phy",  # noqa: E501
            "wekeo-mercator-ibi-multiyear-wav=climetlab_wekeo_mercator.ibi_multiyear_wav:ibi_multiyear_wav",  # noqa: E501
            "wekeo-mercator-insitu-arc-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_arc_phybgcwav_discrete_mynrt:insitu_arc_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-bal-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_bal_phybgcwav_discrete_mynrt:insitu_bal_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-blk-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_blk_phybgcwav_discrete_mynrt:insitu_blk_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-glo-bgc-carbon-discrete-my=climetlab_wekeo_mercator.insitu_glo_bgc_carbon_discrete_my:insitu_glo_bgc_carbon_discrete_my",  # noqa: E501
            "wekeo-mercator-insitu-glo-bgc-discrete-my=climetlab_wekeo_mercator.insitu_glo_bgc_discrete_my:insitu_glo_bgc_discrete_my",  # noqa: E501
            "wekeo-mercator-insitu-glo-phy-ts-oa-my=climetlab_wekeo_mercator.insitu_glo_phy_ts_oa_my:insitu_glo_phy_ts_oa_my",  # noqa: E501
            "wekeo-mercator-insitu-glo-phy-ts-oa-nrt=climetlab_wekeo_mercator.insitu_glo_phy_ts_oa_nrt:insitu_glo_phy_ts_oa_nrt",  # noqa: E501
            "wekeo-mercator-insitu-glo-phy-uv-discrete-my=climetlab_wekeo_mercator.insitu_glo_phy_uv_discrete_my:insitu_glo_phy_uv_discrete_my",  # noqa: E501
            "wekeo-mercator-insitu-glo-phy-uv-discrete-nrt=climetlab_wekeo_mercator.insitu_glo_phy_uv_discrete_nrt:insitu_glo_phy_uv_discrete_nrt",  # noqa: E501
            "wekeo-mercator-insitu-glo-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_glo_phybgcwav_discrete_mynrt:insitu_glo_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-ibi-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_ibi_phybgcwav_discrete_mynrt:insitu_ibi_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-med-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_med_phybgcwav_discrete_mynrt:insitu_med_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-insitu-nws-phybgcwav-discrete-mynrt=climetlab_wekeo_mercator.insitu_nws_phybgcwav_discrete_mynrt:insitu_nws_phybgcwav_discrete_mynrt",  # noqa: E501
            "wekeo-mercator-medsea-analysisforecast-bgc=climetlab_wekeo_mercator.medsea_analysisforecast_bgc:medsea_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-medsea-analysisforecast-phy=climetlab_wekeo_mercator.medsea_analysisforecast_phy:medsea_analysisforecast_phy",  # noqa: E501
            "wekeo-mercator-medsea-analysisforecast-wav=climetlab_wekeo_mercator.medsea_analysisforecast_wav:medsea_analysisforecast_wav",  # noqa: E501
            "wekeo-mercator-medsea-multiyear-bgc=climetlab_wekeo_mercator.medsea_multiyear_bgc:medsea_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-medsea-multiyear-phy=climetlab_wekeo_mercator.medsea_multiyear_phy:medsea_multiyear_phy",  # noqa: E501
            "wekeo-mercator-medsea-multiyear-wav=climetlab_wekeo_mercator.medsea_multiyear_wav:medsea_multiyear_wav",  # noqa: E501
            "wekeo-mercator-multiobs-glo-bio-bgc-3d-rep=climetlab_wekeo_mercator.multiobs_glo_bio_bgc_3d_rep:multiobs_glo_bio_bgc_3d_rep",  # noqa: E501
            "wekeo-mercator-multiobs-glo-bio-carbon-surface-rep=climetlab_wekeo_mercator.multiobs_glo_bio_carbon_surface_rep:multiobs_glo_bio_carbon_surface_rep",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-nrt=climetlab_wekeo_mercator.multiobs_glo_phy_nrt:multiobs_glo_phy_nrt",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-rep=climetlab_wekeo_mercator.multiobs_glo_phy_rep:multiobs_glo_phy_rep",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-s-surface-mynrt=climetlab_wekeo_mercator.multiobs_glo_phy_s_surface_mynrt:multiobs_glo_phy_s_surface_mynrt",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-sss-l3-mynrt=climetlab_wekeo_mercator.multiobs_glo_phy_sss_l3_mynrt:multiobs_glo_phy_sss_l3_mynrt",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-sss-l4-my=climetlab_wekeo_mercator.multiobs_glo_phy_sss_l4_my:multiobs_glo_phy_sss_l4_my",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-tsuv-3d-mynrt=climetlab_wekeo_mercator.multiobs_glo_phy_tsuv_3d_mynrt:multiobs_glo_phy_tsuv_3d_mynrt",  # noqa: E501
            "wekeo-mercator-multiobs-glo-phy-w-3d-rep=climetlab_wekeo_mercator.multiobs_glo_phy_w_3d_rep:multiobs_glo_phy_w_3d_rep",  # noqa: E501
            "wekeo-mercator-northwestshelf-analysis-forecast-phy=climetlab_wekeo_mercator.northwestshelf_analysis_forecast_phy:northwestshelf_analysis_forecast_phy",  # noqa: E501
            "wekeo-mercator-northwestshelf-analysis-forecast-wav=climetlab_wekeo_mercator.northwestshelf_analysis_forecast_wav:northwestshelf_analysis_forecast_wav",  # noqa: E501
            "wekeo-mercator-nwshelf-analysisforecast-bgc=climetlab_wekeo_mercator.nwshelf_analysisforecast_bgc:nwshelf_analysisforecast_bgc",  # noqa: E501
            "wekeo-mercator-nwshelf-analysisforecast-phy-lr=climetlab_wekeo_mercator.nwshelf_analysisforecast_phy_lr:nwshelf_analysisforecast_phy_lr",  # noqa: E501
            "wekeo-mercator-nwshelf-multiyear-bgc=climetlab_wekeo_mercator.nwshelf_multiyear_bgc:nwshelf_multiyear_bgc",  # noqa: E501
            "wekeo-mercator-nwshelf-multiyear-phy=climetlab_wekeo_mercator.nwshelf_multiyear_phy:nwshelf_multiyear_phy",  # noqa: E501
            "wekeo-mercator-nwshelf-reanalysis-wav=climetlab_wekeo_mercator.nwshelf_reanalysis_wav:nwshelf_reanalysis_wav",  # noqa: E501
            "wekeo-mercator-oceancolour-arc-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_arc_bgc_hr_l3_nrt:oceancolour_arc_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-arc-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_arc_bgc_hr_l4_nrt:oceancolour_arc_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-atl-bgc-l4-my=climetlab_wekeo_mercator.oceancolour_atl_bgc_l4_my:oceancolour_atl_bgc_l4_my",  # noqa: E501
            "wekeo-mercator-oceancolour-atl-bgc-l4-nrt=climetlab_wekeo_mercator.oceancolour_atl_bgc_l4_nrt:oceancolour_atl_bgc_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_bal_bgc_hr_l3_nrt:oceancolour_bal_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_bal_bgc_hr_l4_nrt:oceancolour_bal_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-l3-my=climetlab_wekeo_mercator.oceancolour_bal_bgc_l3_my:oceancolour_bal_bgc_l3_my",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-l3-nrt=climetlab_wekeo_mercator.oceancolour_bal_bgc_l3_nrt:oceancolour_bal_bgc_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-l4-my=climetlab_wekeo_mercator.oceancolour_bal_bgc_l4_my:oceancolour_bal_bgc_l4_my",  # noqa: E501
            "wekeo-mercator-oceancolour-bal-bgc-l4-nrt=climetlab_wekeo_mercator.oceancolour_bal_bgc_l4_nrt:oceancolour_bal_bgc_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_blk_bgc_hr_l3_nrt:oceancolour_blk_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_blk_bgc_hr_l4_nrt:oceancolour_blk_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-l3-my=climetlab_wekeo_mercator.oceancolour_blk_bgc_l3_my:oceancolour_blk_bgc_l3_my",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-l3-nrt=climetlab_wekeo_mercator.oceancolour_blk_bgc_l3_nrt:oceancolour_blk_bgc_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-l4-my=climetlab_wekeo_mercator.oceancolour_blk_bgc_l4_my:oceancolour_blk_bgc_l4_my",  # noqa: E501
            "wekeo-mercator-oceancolour-blk-bgc-l4-nrt=climetlab_wekeo_mercator.oceancolour_blk_bgc_l4_nrt:oceancolour_blk_bgc_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-glo-bgc-l3-my=climetlab_wekeo_mercator.oceancolour_glo_bgc_l3_my:oceancolour_glo_bgc_l3_my",  # noqa: E501
            "wekeo-mercator-oceancolour-glo-bgc-l3-nrt=climetlab_wekeo_mercator.oceancolour_glo_bgc_l3_nrt:oceancolour_glo_bgc_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-glo-bgc-l4-my=climetlab_wekeo_mercator.oceancolour_glo_bgc_l4_my:oceancolour_glo_bgc_l4_my",  # noqa: E501
            "wekeo-mercator-oceancolour-glo-bgc-l4-nrt=climetlab_wekeo_mercator.oceancolour_glo_bgc_l4_nrt:oceancolour_glo_bgc_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-ibi-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_ibi_bgc_hr_l3_nrt:oceancolour_ibi_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-ibi-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_ibi_bgc_hr_l4_nrt:oceancolour_ibi_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_med_bgc_hr_l3_nrt:oceancolour_med_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_med_bgc_hr_l4_nrt:oceancolour_med_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-l3-my=climetlab_wekeo_mercator.oceancolour_med_bgc_l3_my:oceancolour_med_bgc_l3_my",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-l3-nrt=climetlab_wekeo_mercator.oceancolour_med_bgc_l3_nrt:oceancolour_med_bgc_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-l4-my=climetlab_wekeo_mercator.oceancolour_med_bgc_l4_my:oceancolour_med_bgc_l4_my",  # noqa: E501
            "wekeo-mercator-oceancolour-med-bgc-l4-nrt=climetlab_wekeo_mercator.oceancolour_med_bgc_l4_nrt:oceancolour_med_bgc_l4_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-nws-bgc-hr-l3-nrt=climetlab_wekeo_mercator.oceancolour_nws_bgc_hr_l3_nrt:oceancolour_nws_bgc_hr_l3_nrt",  # noqa: E501
            "wekeo-mercator-oceancolour-nws-bgc-hr-l4-nrt=climetlab_wekeo_mercator.oceancolour_nws_bgc_hr_l4_nrt:oceancolour_nws_bgc_hr_l4_nrt",  # noqa: E501
            "wekeo-mercator-seaice-ant-phy-auto-l3-nrt=climetlab_wekeo_mercator.seaice_ant_phy_auto_l3_nrt:seaice_ant_phy_auto_l3_nrt",  # noqa: E501
            "wekeo-mercator-seaice-ant-phy-l3-my=climetlab_wekeo_mercator.seaice_ant_phy_l3_my:seaice_ant_phy_l3_my",  # noqa: E501
            "wekeo-mercator-seaice-arc-phy-auto-l4-nrt=climetlab_wekeo_mercator.seaice_arc_phy_auto_l4_nrt:seaice_arc_phy_auto_l4_nrt",  # noqa: E501
            "wekeo-mercator-seaice-arc-phy-climate-l3-my=climetlab_wekeo_mercator.seaice_arc_phy_climate_l3_my:seaice_arc_phy_climate_l3_my",  # noqa: E501
            "wekeo-mercator-seaice-arc-phy-climate-l4-my=climetlab_wekeo_mercator.seaice_arc_phy_climate_l4_my:seaice_arc_phy_climate_l4_my",  # noqa: E501
            "wekeo-mercator-seaice-arc-phy-l4-nrt=climetlab_wekeo_mercator.seaice_arc_phy_l4_nrt:seaice_arc_phy_l4_nrt",  # noqa: E501
            "wekeo-mercator-seaice-arc-seaice-l3-rep-observations=climetlab_wekeo_mercator.seaice_arc_seaice_l3_rep_observations:seaice_arc_seaice_l3_rep_observations",  # noqa: E501
            "wekeo-mercator-seaice-arc-seaice-l4-nrt-observations=climetlab_wekeo_mercator.seaice_arc_seaice_l4_nrt_observations:seaice_arc_seaice_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-seaice-bal-phy-l4-my=climetlab_wekeo_mercator.seaice_bal_phy_l4_my:seaice_bal_phy_l4_my",  # noqa: E501
            "wekeo-mercator-seaice-bal-seaice-l4-nrt-observations=climetlab_wekeo_mercator.seaice_bal_seaice_l4_nrt_observations:seaice_bal_seaice_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-seaice-glo-seaice-l4-nrt-observations=climetlab_wekeo_mercator.seaice_glo_seaice_l4_nrt_observations:seaice_glo_seaice_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-seaice-glo-seaice-l4-rep-observations=climetlab_wekeo_mercator.seaice_glo_seaice_l4_rep_observations:seaice_glo_seaice_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-sealevel-blk-phy-mdt-l4-static=climetlab_wekeo_mercator.sealevel_blk_phy_mdt_l4_static:sealevel_blk_phy_mdt_l4_static",  # noqa: E501
            "wekeo-mercator-sealevel-eur-phy-l3-my=climetlab_wekeo_mercator.sealevel_eur_phy_l3_my:sealevel_eur_phy_l3_my",  # noqa: E501
            "wekeo-mercator-sealevel-eur-phy-l3-nrt-observations=climetlab_wekeo_mercator.sealevel_eur_phy_l3_nrt_observations:sealevel_eur_phy_l3_nrt_observations",  # noqa: E501
            "wekeo-mercator-sealevel-eur-phy-l4-my=climetlab_wekeo_mercator.sealevel_eur_phy_l4_my:sealevel_eur_phy_l4_my",  # noqa: E501
            "wekeo-mercator-sealevel-eur-phy-l4-nrt-observations=climetlab_wekeo_mercator.sealevel_eur_phy_l4_nrt_observations:sealevel_eur_phy_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sealevel-glo-phy-climate-l4-my=climetlab_wekeo_mercator.sealevel_glo_phy_climate_l4_my:sealevel_glo_phy_climate_l4_my",  # noqa: E501
            "wekeo-mercator-sealevel-glo-phy-l4-my=climetlab_wekeo_mercator.sealevel_glo_phy_l4_my:sealevel_glo_phy_l4_my",  # noqa: E501
            "wekeo-mercator-sealevel-glo-phy-l4-nrt-observations=climetlab_wekeo_mercator.sealevel_glo_phy_l4_nrt_observations:sealevel_glo_phy_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sealevel-glo-phy-mdt=climetlab_wekeo_mercator.sealevel_glo_phy_mdt:sealevel_glo_phy_mdt",  # noqa: E501
            "wekeo-mercator-sealevel-med-phy-mdt-l4-static=climetlab_wekeo_mercator.sealevel_med_phy_mdt_l4_static:sealevel_med_phy_mdt_l4_static",  # noqa: E501
            "wekeo-mercator-sst-atl-phy-l3s-my=climetlab_wekeo_mercator.sst_atl_phy_l3s_my:sst_atl_phy_l3s_my",  # noqa: E501
            "wekeo-mercator-sst-atl-phy-l3s-nrt=climetlab_wekeo_mercator.sst_atl_phy_l3s_nrt:sst_atl_phy_l3s_nrt",  # noqa: E501
            "wekeo-mercator-sst-atl-sst-l4-nrt-observations=climetlab_wekeo_mercator.sst_atl_sst_l4_nrt_observations:sst_atl_sst_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-atl-sst-l4-rep-observations=climetlab_wekeo_mercator.sst_atl_sst_l4_rep_observations:sst_atl_sst_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-sst-bal-phy-l3s-my=climetlab_wekeo_mercator.sst_bal_phy_l3s_my:sst_bal_phy_l3s_my",  # noqa: E501
            "wekeo-mercator-sst-bal-phy-subskin-l4-nrt=climetlab_wekeo_mercator.sst_bal_phy_subskin_l4_nrt:sst_bal_phy_subskin_l4_nrt",  # noqa: E501
            "wekeo-mercator-sst-bal-sst-l3s-nrt-observations=climetlab_wekeo_mercator.sst_bal_sst_l3s_nrt_observations:sst_bal_sst_l3s_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-bal-sst-l4-nrt-observations=climetlab_wekeo_mercator.sst_bal_sst_l4_nrt_observations:sst_bal_sst_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-bal-sst-l4-rep-observations=climetlab_wekeo_mercator.sst_bal_sst_l4_rep_observations:sst_bal_sst_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-sst-bs-phy-l3s-my=climetlab_wekeo_mercator.sst_bs_phy_l3s_my:sst_bs_phy_l3s_my",  # noqa: E501
            "wekeo-mercator-sst-bs-phy-subskin-l4-nrt=climetlab_wekeo_mercator.sst_bs_phy_subskin_l4_nrt:sst_bs_phy_subskin_l4_nrt",  # noqa: E501
            "wekeo-mercator-sst-bs-sst-l3s-nrt-observations=climetlab_wekeo_mercator.sst_bs_sst_l3s_nrt_observations:sst_bs_sst_l3s_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-bs-sst-l4-nrt-observations=climetlab_wekeo_mercator.sst_bs_sst_l4_nrt_observations:sst_bs_sst_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-bs-sst-l4-rep-observations=climetlab_wekeo_mercator.sst_bs_sst_l4_rep_observations:sst_bs_sst_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-sst-glo-sst-l3s-nrt-observations=climetlab_wekeo_mercator.sst_glo_sst_l3s_nrt_observations:sst_glo_sst_l3s_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-glo-sst-l4-nrt-observations=climetlab_wekeo_mercator.sst_glo_sst_l4_nrt_observations:sst_glo_sst_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-glo-sst-l4-rep-observations=climetlab_wekeo_mercator.sst_glo_sst_l4_rep_observations:sst_glo_sst_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-sst-med-phy-l3s-my=climetlab_wekeo_mercator.sst_med_phy_l3s_my:sst_med_phy_l3s_my",  # noqa: E501
            "wekeo-mercator-sst-med-phy-subskin-l4-nrt=climetlab_wekeo_mercator.sst_med_phy_subskin_l4_nrt:sst_med_phy_subskin_l4_nrt",  # noqa: E501
            "wekeo-mercator-sst-med-sst-l3s-nrt-observations=climetlab_wekeo_mercator.sst_med_sst_l3s_nrt_observations:sst_med_sst_l3s_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-med-sst-l4-nrt-observations=climetlab_wekeo_mercator.sst_med_sst_l4_nrt_observations:sst_med_sst_l4_nrt_observations",  # noqa: E501
            "wekeo-mercator-sst-med-sst-l4-rep-observations=climetlab_wekeo_mercator.sst_med_sst_l4_rep_observations:sst_med_sst_l4_rep_observations",  # noqa: E501
            "wekeo-mercator-wave-glo-phy-spc-l4-nrt=climetlab_wekeo_mercator.wave_glo_phy_spc_l4_nrt:wave_glo_phy_spc_l4_nrt",  # noqa: E501
            "wekeo-mercator-wave-glo-phy-swh-l3-my=climetlab_wekeo_mercator.wave_glo_phy_swh_l3_my:wave_glo_phy_swh_l3_my",  # noqa: E501
            "wekeo-mercator-wave-glo-phy-swh-l3-nrt=climetlab_wekeo_mercator.wave_glo_phy_swh_l3_nrt:wave_glo_phy_swh_l3_nrt",  # noqa: E501
            "wekeo-mercator-wave-glo-phy-swh-l4-my=climetlab_wekeo_mercator.wave_glo_phy_swh_l4_my:wave_glo_phy_swh_l4_my",  # noqa: E501
            "wekeo-mercator-wave-glo-phy-swh-l4-nrt=climetlab_wekeo_mercator.wave_glo_phy_swh_l4_nrt:wave_glo_phy_swh_l4_nrt",  # noqa: E501
            "wekeo-mercator-wind-glo-phy-climate-l4-my=climetlab_wekeo_mercator.wind_glo_phy_climate_l4_my:wind_glo_phy_climate_l4_my",  # noqa: E501
            "wekeo-mercator-wind-glo-phy-l4-my=climetlab_wekeo_mercator.wind_glo_phy_l4_my:wind_glo_phy_l4_my",  # noqa: E501
            "wekeo-mercator-wind-glo-phy-l4-nrt=climetlab_wekeo_mercator.wind_glo_phy_l4_nrt:wind_glo_phy_l4_nrt",  # noqa: E501
            "wekeo-mercator-wind-glo-wind-l3-nrt-observations=climetlab_wekeo_mercator.wind_glo_wind_l3_nrt_observations:wind_glo_wind_l3_nrt_observations",  # noqa: E501
            "wekeo-mercator-wind-glo-wind-l3-rep-observations=climetlab_wekeo_mercator.wind_glo_wind_l3_rep_observations:wind_glo_wind_l3_rep_observations",  # noqa: E501
            # Other datasets can be included here
            # "wekeo-mercator-dataset-2= climetlab_wekeo_mercator.main2:Main2",  # noqa: E501
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
