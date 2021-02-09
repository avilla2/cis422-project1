
import transformation
#This is the begging of tree
#preDicTable will offer users functionalities'
if __name__ == "__main__":
	#Initiating tree with user's Time Series 
	address = input("Enter Time Series Address : ")
	tree = transformation.tf_tree()
	tree.create_tree(address)
	while tree:
		#Providing User Options
		print('''
			Select Transformation Number
			0 : Quit
			1 : Add
			2 : Remove Operator
			3 : Replace Process
			4 : Execute
			5 : Save/Load
			''')
		#First to check tree
		print("Current Tree")
		tree.print_tree(1)

		choice = int(input("\nEnter Number : "))

		#Exit the program
		if choice == 0:
			print("Exit preDicTable")
			break

		#Adding Options to add funtions from transformation module
		elif choice == 1:
			#Lists of operators
			inp = int(input("\n0 : Operator\t1 : Subtree\n"))
			pnode = int(input("Enter Parent Number : "))
			if inp == 0:
				print("\nPreprocessing List :\n[ denoise, impute_missing_data, impute_outliers, longest_continuous_run, clip, assign_time, difference, scaling, standardize, logarithm, cubic_root, ts2db ]")
				print("\nMachine Learning List :\n[ split_models, create_train, forecast ]")
				print("\nAnalizing List :\n[ plot, histogram, box_plot, normality_test, mse, mape, smape ]")
			
				op = input("\nEnter Operator : ")
				tree.add_operator(pnode, op)
			elif inp == 1:
				print("Replicate Node")
				tree_type = int(input("0 : Subtree\t1 : Tree Path\n"))
				cnode = int(input("Enter Node Number : "))
				if tree_type == 0:
					tree.add_subtree(tree.replicate_tree_path(cnode), pnode)
				elif tree_type == 1:
					tree.add_subtree(tree.replicate_subtree(cnode), pnode)

		#Asking for variable to remove node
		elif choice == 2:
			node = int(input("\nEnter Node Number : "))
			tree.remove_operator(node)

		#Asking for variable to replace operator
		elif choice == 3:
			node = int(input("\nEnter Node Number to Replace : "))
			op = input("Enter New Operator : ")
			tree.replace_process(node, op)

		#Adding Options to exec funtions from transformation module
		elif choice == 4:
			exec_type = int(input("\n0 : Tree\t1 : Pipeline\n"))
			if exec_type == 0:
				tree.exec_tree()
			elif exec_type == 1:
				node = int(input("Enter Node Number : "))
				tree.exec_pipeline(node)

		#Adding Options to save_load funtions from transformation module
		elif choice == 5:
			sl = int(input("\n0 : Save\t1 : Load\n"))
			sl_type = int(input("0 : Tree\t1 : Pipeline\n"))
			nm = input("Enter File Name : ")
			if sl == 0:
				if sl_type == 0:
					tree.save_load_tree("save", nm)
				elif sl_type == 1:
					tree.save_load_pipeline("save", nm)
			elif sl == 1:
				if sl_type == 0:
					tree.save_load_tree("load", nm)
				elif sl_type == 1:
					tree.save_load_pipeline("load", nm)
