import transformation
'''
credit by Alex.V and Jay.S
This is main module that users are going to deal with
Siply running transformation module for users
Easier UI module for users
'''

def print_options():
    print(
        "\nPreprocessing List :\n[ denoise, impute_missing_data, impute_outliers, longest_continuous_run, clip, assign_time, difference, scaling, standardize, logarithm, cubic_root ]")
    print("\nMachine Learning List :\n[ split_models, create_train, forecast ]")
    print("\nAnalizing List :\n[ plot, histogram, box_plot, normality_test, mse, mape, smape ]")
    return


# This is the begging of tree
# preDicTable will offer users functionality'
if __name__ == "__main__":
    '''
    This first initializing tree
    Repeats asking functions until users quit
    '''
    # Initiating tree with user's Time Series
    tree = transformation.tf_tree()

    valid = int(input("0 : New\t\t1 : Load\n"))
    if valid:
        nm = input("Enter name of file : ")
        if not tree.save_load_tree("load", nm):
            print("Invalid Input")
            pass
    else:
        while not valid:
            try:
                address = input("Enter Time Series File Path (CSV Format): ")
                tree.create_tree(address)
                # First to check tree
                print("Current Tree")
                tree.print_tree(1)
                valid = True
            except FileNotFoundError:
                print("File was not found, or the file path was entered incorrectly")
            except AttributeError:
                print("Tree creation was unsuccessful, please enter another file path")

    while tree:
        # Providing User Options
        print('''
            Transformation Number
            0 : Quit
            1 : Add
            2 : Remove Operator
            3 : Replace Process
            4 : Execute
            5 : Save/Load
            ''')
        #print tree
        tree.print_tree(1)

        choice = int(input("\nSelect Transformation Number : "))

        # Exit the program
        if choice == 0:
            print("Exit preDicTable")
            break

        # Adding Options to add funtions from transformation module
        elif choice == 1:
            # Lists of operators
            inp = int(input("\n0 : Operator\t1 : Subtree\n"))
            pnode = int(input("Enter Parent Number : "))
            if inp == 0:
                print_options()
                op = input("\nEnter Operator : ")
                if not tree.add_operator(pnode, op):
                    print("Invalid Input")
                    pass
            elif inp == 1:
                print("Replicate Node")
                tree_type = int(input("0 : Subtree\t1 : Tree Path\n"))
                cnode = int(input("Enter Node Number : "))
                if tree_type == 0:
                    if not tree.add_subtree(tree.replicate_tree_path(cnode), pnode):
                        print("Invalid Input")
                        pass
                elif tree_type == 1:
                    if not tree.add_subtree(tree.replicate_subtree(cnode), pnode):
                        print("Invalid Input")
                        pass
                else:
                    print("Invalid Input")
                    pass
            else:
                print("Invalid Input")
                pass

        # Asking for variable to remove node
        elif choice == 2:
            node = int(input("\nEnter Node Number : "))
            if not tree.remove_operator(node):
                print("Invalid Input")
                pass

        # Asking for variable to replace operator
        elif choice == 3:
            node = int(input("\nEnter Node Number to Replace : "))
            print_options()
            op = input("Enter New Operator : ")
            if not tree.replace_process(node, op):
                print("Invalid Input")
                pass

        # Adding Options to exec funtions from transformation module
        elif choice == 4:
            exec_type = int(input("\n0 : Tree\t1 : Pipeline\n"))
            if exec_type == 0:
                if not tree.exec_tree():
                    print("Invalid Input")
                    pass
            elif exec_type == 1:
                node = int(input("Enter Node Number : "))
                if not tree.exec_pipeline(node):
                    print("Invalid Input")
                    pass
            else:
                print("Invalid Input")
                pass

        # Adding Options to save_load funtions from transformation module
        elif choice == 5:
            sl = int(input("\n0 : Save\t1 : Load\n"))
            sl_type = int(input("0 : Tree\t1 : Pipeline\n"))
            nm = input("Enter File Name : ")
            if sl == 0:
                if sl_type == 0:
                    if not tree.save_load_tree("save", nm):
                        print("Invalid Input")
                        pass
                elif sl_type == 1:
                    if not tree.save_load_pipeline("save", nm):
                        print("Invalid Input")
                        pass
                else:
                    print("Invalid Input")
                    pass
            elif sl == 1:
                if sl_type == 0:
                    if not tree.save_load_tree("load", nm):
                        print("Invalid Input")
                        pass
                elif sl_type == 1:
                    if not tree.save_load_pipeline("load", nm):
                        print("Invalid Input")
                        pass
                else:
                    print("Invalid Input")
                    pass
            else:
                print("Invalid Input")
                pass

        else:
            print("Invalid Input")
            pass
