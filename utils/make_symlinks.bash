# # This will be a problem if these simulations are ever removed from the publication archives!
# for i in $(seq 1 20); do
#     hsi ln -s /home/projects/e3sm/www/publication-archives/pub_archive_E3SM_1_0_LE_historical_ens$i /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/LE_historical_ens$i
# done

# for i in $(seq 1 20); do
#     hsi ln -s /home/projects/e3sm/www/publication-archives/pub_archive_E3SM_1_0_LE_ssp370_ens$i /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/LE_ssp370_ens$i
# done

# # Symlink last remaining large simulation
# # This will be a problem if ndk ever deletes the source!
# hsi ln -s /home/n/ndk/2019/theta.20190910.branch_noCNT.n825def.unc06.A_WCYCL1950S_CMIP6_HR.ne120_oRRS18v3_ICG /home/projects/e3sm/www/WaterCycle/E3SMv1/LR/theta.20190910.branch_noCNT.n825def.unc06.A_WCYCL1950S_CMIP6_HR.ne120_oRRS18v3_ICG

# Note:
# It seems impossible to do a recursive remove with HSI/on HPSS.
# > rm -rf E3SM_1_0_LE_historical_ens1@ # Trying to remove mislabeled directory
# Unknown option or missing argument: 'r' ignored
# Unknown option or missing argument: 'f' ignored

### Cryosphere ###
hsi ln -s /home/d/dcomeau/cryosphere_simulations/20190430.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.control.cori-knl /home/projects/e3sm/www/Cryosphere/E3SMv1/20190430.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.control.cori-knl
for simulation in "20190306.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.edison" "20190923.GMPAS-IAF.T62_oEC60to30v3wLI.cori-knl" "20190225.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl" "20200610.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.cori-knl.maint1p2-3DGM" "20190819.GMPAS-DIB-IAF-ISMF.T62_oEC60to30v3wLI.cori-knl.testNewGM" "20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_oECv3wLI.DIBbugfix.anvil" "20210614.A_WCYCL1850-DIB-ISMF_CMIP6.ne30_ECwISC30to60E1r2.anvil.DIBbugFixMGM"; do
    hsi ln -s /home/projects/m3412/${simulation} /home/projects/e3sm/www/Cryosphere/E3SMv1/${simulation}
done

# TODO: complete the v1 cryo csv
# TODO: add docs for v1 cryo
# TODO: run the table generator script for that csv
