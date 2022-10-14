import os
import subprocess
import itertools

#add folder name to this and save those stats.txt etc int that folder
rootoutput = '/home/eng/m/mks200001/CAproj/Project2_outputs/Outputs_470_2'

#shell script paths
runG51 = '/home/eng/m/mks200001/CAproj/benchmarks/470.lbm/runGem5.sh'
runG5template1 = '/home/eng/m/mks200001/CAproj/Auto2/runGem5temp1.sh'

#the scons command to rebuild
#sconspath = 'build/X86/gem5.opt'

L1i_sizes = L1d_sizes = [2**i for i in range(6,8)]
L2_sizes = [2**i for i in range(8,11)]
#L1i_assoc = L1d_assoc = [1,2,4]
L1_assoc = [1,2,4]
L2_assoc = [1,2]
cache_block_size = [32, 64]

def runconfigs():

	#make all the changes in the ".sh" file
	#calling rewrite function
	l = [L1d_sizes, L1i_sizes, L2_sizes, L1_assoc, L2_assoc, cache_block_size]
	combos = list(itertools.product(*l))

	for c in combos[len(combos)//2:]:
		tempfolder2 = '/470L1S_' + str(c[0]) + '_' + str(c[1]) + '_L2S_' + str(c[2]) + '_L1a_'+str(c[3]) + '_L2a_' + str(c[4]) + '_cbs_' + str(c[5])
		outloc2 = rootoutput + tempfolder2

		#edit the shell script of 458.sjeng before running subprocess
		f2 = open(runG5template1, "r")
		lines = f2.readlines()
		f2.close()
		f2 = open(runG51, "w")
		for line in lines:
			if('~/m5out' in line):
				line = line.replace('~/m5out', outloc2)
			if('L1d_size' in line):
				line = line.replace('L1d_size', str(c[0])+'kB')
			if('L1i_size' in line):
				line = line.replace('L1i_size', str(c[1])+'kB')
			if('L2_size' in line):
				if(c[2] == 1024):
					line = line.replace('L2_size', str(1)+'MB')
				else:
					line = line.replace('L2_size', str(c[2])+'kB')
			if('L1d_assoc' in line):
				line = line.replace('L1d_assoc', str(c[3]))
			if('L1i_assoc' in line):
				line = line.replace('L1i_assoc', str(c[3]))
			if('L2_assoc' in line):
				line = line.replace('L2_assoc', str(c[4]))
			if('cache_block_size' in line):
				line = line.replace('cache_block_size', str(c[5]))			
			f2.write(line)
		f2.close()

		#subprocess call to run shell script
		subprocess.call(['sh', runG51], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print("Completed iteration of " + tempfolder2)
	




if __name__ == '__main__':
	print("##############################Starting the Automation#########################")
	print("------------------------------------------------------------------------------")

	print("Running second half of all the cache configurations on 470.lbm")
	print("------------------------------------------------------------------------------")
	runconfigs()

	print("###########################All Simulations completed##########################")

