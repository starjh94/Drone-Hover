import os
import sys
import glob

print len(glob.glob("./TF_Data/"+sys.argv[1]+".*")) 

if len(sys.argv) == 2 :

	if os.path.exists("./TF_Data/"+sys.argv[1]) is False :
		print "'%s' is Not exist file\n" %(sys.argv[1])
		exit()
	else:
		print "'%s' model will be restored!\n" %(sys.argv[1])
while True:
	learning_model_name= raw_input("Model name for save(<ex> *.ckpt) : ")

	if learning_model_name[-5:] != ".ckpt":
		print "\nPlease write correctly!"
	elif os.path.exists("./TF_Data/"+learning_model_name) is True:	
		
		while True:
			same_name_answer = raw_input("\nThe file name already exists.\nDo you want to overwrite?(Y / N): ")
		
			if same_name_answer.upper() == "Y":
				print "\nIt will be saved as '%s'" % (learning_model_name)
				break
			elif same_name_answer.upper() == "N":
				print "\nEnter the model name again"
				break
			else:
				print "\nPleas write correctly!"

		if same_name_answer.upper() == "Y":
			break
	else:	
		print "\nIt will be saved as '%s'" % (learning_model_name)
		break



