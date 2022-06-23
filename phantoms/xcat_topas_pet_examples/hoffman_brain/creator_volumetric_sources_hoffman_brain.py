import os
from config.definitions import ROOT_DIR

def main():
	#modified string created by the tissues_creator.py helper file
	#-1 means the default ratio
	# MUST REMOVE "XCAT_Air = -1" FROM LIST IF IT IS PRESENT

	#for the hoffman brain, it has grey matter and white matter activities changed, and all other activities set to 0

	#list of materials that are NOT present in the XCAT phantom that we are working with
	materials_not_used = '''XCAT_adrenal_activity = -1
	XCAT_airway_activity = -1
	XCAT_Amygdala_act = -1
	XCAT_Anterior_commissure_act = -1
	XCAT_Caudate_act = -1
	XCAT_Cerebral_aqueduct_act = -1
	XCAT_Cerebral_peduncles_act = -1
	XCAT_coronary_vein_activity = -1
	XCAT_ejac_duct_activity = -1
	XCAT_fallopian_tubes_activity = -1
	XCAT_Fornix_act = -1
	XCAT_Fourth_ventricle_act = -1
	XCAT_Globus_pallidus_act = -1
	XCAT_Hippocampus_act = -1
	XCAT_Inferior_colliculus_act = -1
	XCAT_Inferior_olive_act = -1
	XCAT_Internal_capsule_act = -1
	XCAT_Lateral_ventricle_act = -1
	XCAT_lbreast_activity = -1
	XCAT_rbreast_activity = -1
	XCAT_left_ovary_activity = -1
	XCAT_right_ovary_activity = -1
	XCAT_left_renal_pelvis_activity = -1
	XCAT_right_renal_pelvis_activity = -1
	XCAT_lens_activity = -1
	XCAT_lesn_activity = -1
	XCAT_lymph_abnormal_activity = -1
	XCAT_lymph_activity = -1
	XCAT_Mamillary_bodies_act = -1
	XCAT_Medulla_act = -1
	XCAT_Medullary_pyramids_act = -1
	XCAT_Midbrain_act = -1
	XCAT_myoLA_act = -1
	XCAT_myoRV_act = -1
	XCAT_parathyroid_activity = -1
	XCAT_Periacquaductal_grey_outer_act = -1
	XCAT_Pineal_gland_act = -1
	XCAT_pituitary_activity = -1
	XCAT_Pons_act = -1
	XCAT_Substantia_nigra_act = -1
	XCAT_Superior_cerebellar_peduncle_act = -1
	XCAT_Superior_colliculus_act = -1
	XCAT_Tegmentum_of_midbrain_act = -1
	XCAT_Third_ventricle_act = -1
	XCAT_thymus_activity = -1
	XCAT_trach_bronch_activity = -1
	XCAT_ureter_activity = -1
	XCAT_uterus_activity = -1
	XCAT_vagina_activity = -1
	'''

	#materials found in the current XCAT phantom
	#activity for grey and white matter is in units of kBq/mL
	materials_used = '''XCAT_yellow_bone_marrow_activity = -1
	XCAT_myoLV_act = -1
	XCAT_myoRA_act = -1
	XCAT_bldplLV_act = -1
	XCAT_bldplRV_act = -1
	XCAT_bldplLA_act = -1
	XCAT_bldplRA_act = -1
	XCAT_coronary_art_activity = -1
	XCAT_body_activity = -1
	XCAT_skin_activity = -1
	XCAT_muscle_activity = -1
	XCAT_brain_activity = -1
	XCAT_sinus_activity = -1
	XCAT_liver_activity = -1
	XCAT_gall_bladder_activity = -1
	XCAT_right_lung_activity = -1
	XCAT_left_lung_activity = -1
	XCAT_esophagus_activity = -1
	XCAT_esophagus_contents_activity = -1
	XCAT_laryngopharynx_activity = -1
	XCAT_larynx_activity = -1
	XCAT_st_wall_activity = -1
	XCAT_st_cnts_activity = -1
	XCAT_pancreas_activity = -1
	XCAT_right_kidney_cortex_activity = -1
	XCAT_right_kidney_medulla_activity = -1
	XCAT_left_kidney_cortex_activity = -1
	XCAT_left_kidney_medulla_activity = -1
	XCAT_spleen_activity = -1
	XCAT_rib_activity = -1
	XCAT_cortical_bone_activity = -1
	XCAT_spine_activity = -1
	XCAT_spinal_cord_activity = -1
	XCAT_bone_marrow_activity = -1
	XCAT_art_activity = -1
	XCAT_vein_activity = -1
	XCAT_bladder_activity = -1
	XCAT_prostate_activity = -1
	XCAT_asc_large_intest_activity = -1
	XCAT_trans_large_intest_activity = -1
	XCAT_desc_large_intest_activity = -1
	XCAT_small_intest_activity = -1
	XCAT_rectum_activity = -1
	XCAT_sem_activity = -1
	XCAT_vas_def_activity = -1
	XCAT_test_activity = -1
	XCAT_penis_activity = -1
	XCAT_epididymus_activity = -1
	XCAT_pericardium_activity = -1
	XCAT_cartilage_activity = -1
	XCAT_intest_air_activity = -1
	XCAT_urethra_activity = -1
	XCAT_thyroid_activity = -1
	XCAT_salivary_activity = -1
	XCAT_eye_activity = -1
	XCAT_Corpus_Callosum_act = -1
	XCAT_Putamen_act = -1
	XCAT_Thalamus_act = -1
	XCAT_Periacquaductal_grey_act = -1
	XCAT_Middle_cerebellar_peduncle_act = -1
	XCAT_cerebellum_act = -1
	XCAT_white_matter_act = 8.25
	XCAT_grey_matter_act = 33'''

	#creates the blank topas parameter file
	f = open(os.path.join(ROOT_DIR, 'volumetric_sources_hoffman_brain.topas'), 'w')

	#writes initial comments
	f.write('#this is a helper file composed of only volumetric sources over each of the XCAT phantom materials/tissues\n\n')

	#sets the number of histories in tissues with default -1 ratio
	default_ratio = 0

	#defines the volumes of the tissues
	#uses average brain volume of 1510 mL for males 
	#uses estimate for percentage of grey and white matter from paper by Luders 2002 Brain Size and Grey Matter Volume...
	volume_dict = {
		"XCAT_grey_matter_act": 1510*.5441,
		"XCAT_white_matter_act": 1510*.2773
	}

	

	#defines the time chunk over which the part of the scan takes place in seconds
	time = .000001

	activematerial_values = ""
	numhistories_values = ""
	tf_times = ""
	tf_count = 0

	#begins reading the long string of ratios above and appending corresponding sources to .topas file
	lines = materials_used.splitlines()
	for line in lines:
		segments = line.split('=')
		tissue = segments[0].strip()
		ratio = float(segments[1].strip())
		if ratio < 0:
			ratio = default_ratio
		if tissue in volume_dict:
			histories = int(int((ratio*1000*time*volume_dict[tissue])*100)/100)
		else:
			histories = 0

		if histories > 0:
			tf_count+=1
			activematerial_values = activematerial_values + "\"" + tissue + "\" "
			numhistories_values = numhistories_values + str(histories) + " "
			tf_times = tf_times + str(tf_count*10) + " "
	
	activematerial_values = str(tf_count) + " " + activematerial_values
	numhistories_values = str(tf_count) + " " + numhistories_values
	tf_times = str(tf_count) + " " + tf_times + " ms"

	f.write('''# defines two step functions, one for active materials and one for number of histories
# crucial for proper formatting of tuple outputs
s:Tf/ActiveMaterial/Function = "Step"
dv:Tf/ActiveMaterial/Times = ''' + tf_times + '''
sv:Tf/ActiveMaterial/Values = ''' + activematerial_values + '''

s:Tf/NumHistories/Function = "Step"
dv:Tf/NumHistories/Times = ''' + tf_times + '''
iv:Tf/NumHistories/Values = ''' + numhistories_values + '''\n\n''')


	f.write('''s:So/VaryingSource/Type            = "Volumetric"
s:So/VaryingSource/Component       = "Patient"				# specifies that the source is defined for the Patient geometry
sc:So/VaryingSource/ActiveMaterial = Tf/ActiveMaterial/Value			# specifies which material within the Patient geometry is active i.e. contain radionuclides
s:So/VaryingSource/BeamParticle    = "e+"					# tells which particle will be distributed throughout the active material
ic:So/VaryingSource/NumberOfHistoriesInRun = Tf/NumHistories/Value				# the number of particles that will be randomly distributed throughout the active material
b:So/VaryingSource/RecursivelyIncludeChildren = "True"			
ic:So/VaryingSource/MaxNumberOfPointsToSample = 1000000000			#1e9 points	

s:So/VaryingSource/BeamEnergySpectrumType          = "Discrete"
dv:So/VaryingSource/BeamEnergySpectrumValues       = 1 0 MeV		# currently set to 0 MeV so all the particles are at rest to begin
uv:So/VaryingSource/BeamEnergySpectrumWeights      = 1 1.0		# defines the percentages of the particles at the respective energy value''')

	f.close()

if __name__ == "__main__":
	main()




