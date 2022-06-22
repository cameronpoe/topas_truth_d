guide to this directory:

the config/ folder allows for simple python script use across machines by allowing for relative paths per machine

pet_scanner.topas is the main TOPAS file that scores gamma rays emitted from radioactive sources within the geometry inside the PET detector. It contains a statement that includes xcat_hoffman_brain.topas

xcat_activity_phantom.topas is the actual XCAT phantom built in TOPAS. Its grey and white matter has positrons distributed within it based on volumetric sources within volumetric_sources_hoffman_brain.topas, which it includes. These activities are specified by the Hoffman brain.

volumetric_sources_hoffman_brain.topas is the file that contains volumetric sources for every tissue in the XCAT phantom. Most are set to have 0 activity (0 positrons), but grey and white matter are set to non-zero activities
