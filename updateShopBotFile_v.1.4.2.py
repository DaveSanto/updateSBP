import sys
import os
import re
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from datetime import date
import shutil

class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            today1 = datetime.datetime.now()
            todayDate = today1.strftime("%m/%d/%Y %H:%M:%S")
        
            print(f"****************************BEGIN Update ShopBot File on: {todayDate}****************************")
            
            self.setupVariables()
            # Define button properties
            buttonWidth = 100
            buttonHeight = 50
            buttonX = 50
            buttonY = 50

            # create window size variables
            windowX = int(200)
            windowY = int(200)
            windowWidth = int(600)
            windowHeight = int(400)

            buttonWidth = int(round(windowWidth*0.3,0))
            buttonHeight = int(round(windowHeight*0.3,0))

            button1X = int(round(((windowWidth/2) - buttonWidth)/2,0))
            button2X = int(round(((windowWidth/2) + float(button1X))))
            buttonY = int(50)

            # Create the label to display the location name and variables
            self.label = QLabel(self)
            self.label.setText("Here is the label\n Many lines of text \n many many things to say\n say them here or go away \n about a boy \n and a girl")
            self.label.setFont(QFont("Arial", 12))
            self.label.setFixedSize(windowWidth,windowHeight)

            # self.label.setBaseSize(500,500)
            # Create the button for 1
            self.button_1 = QPushButton("1180 Beacon", self)
            self.button_1.setGeometry(buttonX, buttonY, buttonWidth, buttonHeight)
            #self.button_1.clicked.connect(lambda machineID=1: self.select_file(str(machineID)))
        # self.button_1.clicked.connect(lambda machineID=2: self.select_file(machineID))
            self.button_1.clicked.connect(lambda: self.select_file("1"))
        
            # Create the button for 2
            self.button_2 = QPushButton("8 Hidden Brick", self)
            self.button_2.setGeometry(buttonX + buttonWidth + 50, buttonY, buttonWidth, buttonHeight)
            #self.button_2.clicked.connect(lambda machineID=2: self.select_file(str(machineID)))
            #self.button_2.clicked.connect(lambda machineID=2: self.select_file(machineID))
            self.button_2.clicked.connect(lambda: self.select_file("2"))

            # Set the main window properties
            self.setWindowTitle("Update ShopBot File")
            self.setGeometry(windowX, windowY, windowWidth, windowHeight)
            self.show()
            print("finished setup")

        # Define select file function:
    
        def select_file(self, machineID):
            print(f"machineID type: {type(machineID)}")
        
        
            print(f"machineID: {type(machineID)}")
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("ShopBot part files (*.sbp)")
            file_dialog.setOptions(options)
            print(f"options: {options}")
            initial_dir = 'G:\My Drive\PostFiles'

            filepath, _ = file_dialog.getOpenFileName(self, "Select ShopBot part file", initial_dir, "ShopBot Part Files (*.sbp)")
            print("machineID: ", machineID)
    
            if machineID == "1": 
                self.machineName = "ShopBot PRS Alpha Buddy"
                self.homeXY = "0, -8"
                self.location = "1180 Beacon St. Lab"
            elif machineID == "2":
                self.machineName = "ShopBot PRT Alpha"
                self.homeXY = "9.6, -2.35"
                self.location = "8 Hidden Brick Rd. Lab"
            else: 
                self.machineName = "machine undefined"
                print("error: machine Undefined")
            
            print(f"machineID: {str(machineID)}")

                
            if filepath:
                print("File Selected: ", filepath)
                self.copy_file(filepath)
                
        # Define file copy function
        def copy_file(self, filepath):
            # Get the directory and filename of the original file
            directory = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            
            # Create a copy of the original file with "OriginalCopy" appended to the end
            new_filename = os.path.splitext(filename)[0] + "_OriginalCopy" + os.path.splitext(filename)[1]
            print(f"new file name:{new_filename}")

            self.parse_filename(filename)

            self.name = self.parsed_data["name"]
            self.shoe_type = self.parsed_data["shoe_type"]
            self.material_type = self.parsed_data["material_type"]
            self.block_size = self.parsed_data["block_size"]
            self.order_date = self.parsed_data["order_date"]
            self.left_x = self.parsed_data["left_x"]
            self.left_y = self.parsed_data["left_y"]
            self.left_angle = self.parsed_data["left_angle"]
            self.right_x = self.parsed_data["right_x"]
            self.right_y = self.parsed_data["right_y"]
            self.right_angle = self.parsed_data["right_angle"]
            profileVar = self.parsed_data["profile_type"]
            self.profile_type = profileVar.replace(".sbp", "")

            
            labelText = f"{self.name}\n{self.shoe_type}\n{self.material_type}\n{self.block_size}\n{self.order_date}\n {self.profile_type}"
            
            print(labelText)
            self.label.setText = "labelText"

            # Copy the original file and rename it with the new filename
            new_filepath2 = os.path.join(directory, new_filename)
            #os.system("copy " + filepath + " " + new_filepath)
            shutil.copyfile(filepath, new_filepath2)

            if new_filepath2:
                with open(new_filepath2, "r+") as update_file:
                    update_lines = update_file.readlines()
                    update_file.seek(0)
                    update_file.truncate()
                # fileType = profileType_var.get()
                    
                    # endBit = endBit_var.get()
                    machine = self.machineName

                    #what do we need from bit 
                    # 
                    fileType = self.profile_type 
                    print(f"Key1 before bitDict: {fileType}")
                    bitDict = {
                        #[name of bit, bit difference to 1/2" bit]
                        "Parallel": ["1/2\" 2 Flute Ball End Mill","0"],
                        "ProfileBit": ["1/8\" 2 Flute End Mill 3in","0" ],
                        "ProfileBit2": ["1/8\" 2 Flute End Mill 1in","1.5"],
                        "PROFILE": ["Drag Knife","0.94"]
                    }

                    for key1, values in bitDict.items():

                        bitDifference = bitDict[key1][1]
                        print(f"bictDict[key1][1]: {bitDict[key1][1]}")
                        bitUsed = bitDict[key1][0]
                        # print(f"bit used: {bitUsed}")
                        # print("bitUsed: ",bitUsed)
                        # print(f"bitdifferce: {bitDifference}")
                    bitDifference = bitDict[fileType][1]
                    bitUsed = bitDict[fileType]
                    print(f"bitdifference: {bitDifference}")
                    material = {
                    "E40": ['1', '0.75', 'EVA WWF 40'],
                    "E60": ['2', '0.75', 'EVA WWF 60'],
                    "E40 (C)": ['3', '0.75', 'EVA WWF 40 - Custom top'],
                    "E60 (C)": ['4', '0.75', 'EVA WWF 60 - Custom top'],
                    "E40 (L)": ['5', '0.76', 'EVA WWF 40 - Leather top'],
                    "E60 (L)": ['6', '0.76', 'EVA WWF 60 - Leather top'],
                    '1': ['7', '0.9375', 'ACOR PZ1'],
                    "26": ['8', '1.25', 'ACOR PZ26'],
                    "C2" : ['9', '0.630921', 'Nora Combi2'],
                    "SLW" : ['10', '0.787402', 'Nora Lunatec SLW'],
                    }

                    
                    key = self.material_type
                    print(f"material key: {key}")
                    print(f"material[key][2]: {material[key][2]}")
                    

                    # for key, values in material.items():
                    #     print(f"{key}: {values}")
                    
                    #if the command is going to be in both Profile and ProfileBit file types
                    # then set it as is for those files here and update it in 
                    # the Parallel Section of If statment

                    #Set up Profile Types
                    thickness = material[self.material_type][1]
                    useSpindle = ""
                    moveZComment =  "'move the z to "f"{bitDifference}\" inch - difference between bit and {bitUsed}]"
                    moveZbitDiff ="MZ, "f"{bitDifference}" 
                    zZeroforBitDiff = "ZZ"
                    useThickCommand = f"MZ, {thickness}"
                    reZeroForThickCommand = "ZZ"
                    startBit = bitDict["Parallel"][0]
                    endBit = bitDict["Parallel"][0]
                    useChangeBitComment = f"'Change {startBit} to {endBit}"
                    jogZHeight = "1.5"
                    
                    if self.profile_type == "PROFILE":
                        startBit = "Drag Knife"
                        endBit = "1/2\" 2 Flute Bit"
                        moveZComment = "'move the z to "f"{bitDifference}\" inch - difference between bit and {bitUsed}]"
                        moveZbitDiff ="MZ, "f"{bitDifference}" 
                        zZeroforBitDiff = "ZZ"
                        useSpindle = "#"
                        jogZHeight = "0.5"
                        
                    
                    elif self.profile_type == "ProfileBit":
                        startBit = "1/8\" bit" 
                        endBit = "1/2\" 2 Flute Bit"
                        
                        #We use the Spindle in the Profle bit so useSpindle should have no comment in this profile file type
                        useSpindle = ""
                        jogZHeight = "2"

                    elif self.profile_type == "Parallel":
                        startBit = "1/2\" 2 Flute Bit"
                        endBit = "1/2\" 2 Flute Bit"
                        moveZComment = "not necessary to move Z"
                        moveZbitDiff = ""
                        zZeroforBitDiff = ""
                        useThickCommand = ""
                        reZeroForThickCommand = ""
                        useSpindle = ""
                        jogZHeight = "2"
                        useChangeBitComment = ""


                    else: 
                        startBit = "error!"
                        endBit = "errorEndBit"
                        moveZComment = ""
                        useSpindle = "\'"
                        useThicknessDiff = "'"
                        jogZHeight = "error"
                        


                

                    today = date.today().strftime("%Y-%m-%d")
                   
                    new_linesTop = [f"'{self.profile_type} Ready at Top\n"]
                    if self.location: 
                        new_linesTop.append(f"'location: {self.location}\n")
                    if machine:
                        new_linesTop.append(f"'machine: {machine}\n")
                    if thickness:
                        new_linesTop.append(f"'material thickness: {thickness}\n")
                    if today:
                        new_linesTop.append(f"'date postfile updated: {today}\n")
                    new_linesTop.append("SA\n")
                    new_linesTop.append("'C2\n")
                    if moveZComment:
                        new_linesTop.append(f"{moveZComment}")
                    if moveZbitDiff:
                        new_linesTop.append(f"{moveZbitDiff}\n")
                    if zZeroforBitDiff:
                        new_linesTop.append(f"{zZeroforBitDiff}\n")
                    if useThickCommand:
                        new_linesTop.append(f"{useThickCommand}\n")
                    if reZeroForThickCommand:
                        new_linesTop.append(f"{reZeroForThickCommand}\n")
                    if useChangeBitComment:
                        new_linesTop.append(f"{useChangeBitComment}\n")
                    new_linesTop.append("Pause\n")
                    new_linesTop.append(f"{useSpindle}SO,1,1\n")
                    new_linesTop.append(f"'bit used: {bitUsed}\n")





                    #BOTTOM LINES:
                    new_linesBottom = [ "JZ,.1\n",
                                        f"JZ,{jogZHeight}\n",
                                        f"{useSpindle}SO,1,0\n",
                                        f"J2,{self.homeXY}\n",
                                        "Pause\n",
                                         ]
                    if useChangeBitComment: 
                        new_linesBottom.append(useChangeBitComment)
                    if useThickCommand:
                        new_linesBottom.append(f"MZ, {thickness}\n")
                    if reZeroForThickCommand:
                        new_linesBottom.append(f"{reZeroForThickCommand}\n")
                    new_linesBottom.append("Pause")
                    if moveZbitDiff:
                        new_linesBottom.append( f"MZ, -{bitDifference}\n")
                    if zZeroforBitDiff:
                        new_linesBottom.append(f"{zZeroforBitDiff}\n")
                    new_linesBottom.append(f"MZ, {jogZHeight}")
                    new_linesBottom.append("'END\n")
                    new_linesBottom.append(f"'{self.profile_type} is Ready at Bottom")
                    

                    
                    # MZ,-0.75
                    # ZZ
                    # Pause
                    # 'SafetyCheck - you're about to zero - check if you look too low
                    # MZ,-0.94
                    # ZZ
                    # 0.5
                    # 'ShopBot PRS Alpha Buddy
                    # '0.75 inch material thickness
                    
                    

                    

                    # Profile
                    #Profile Ready at Top
                    # 'location:
                    # 'machine:
                    # 'material thickness
                    # 'Assume at the start of a Profile file that the Parallel was set 
                    # last with 1/2" bit zeroed and safely at 1.75
                    # but do not change bit until prompted.
                    # SA
                    # 'C2
                    # 'move the Z to 0.95" inch - difference between bit and drag knife
                    # MZ, 0.95 { }
                    # ZZ
                    # MZ, 1.0 (MAT THICKNESS!)
                    # ZZ
                    # MZ, 0.25
                    # 'SO, 1,1 (do not turn on bit it is a drag knife profile)
                    # JS,10.0,2.0,
                    # JZ,1.25
                    # 'Do not turn on Spindle, this is a drag knife profile
                    # Pause
                    # 'SO,1,1 (commented out but left there for now)
                    # ' 1/32 EM CRB 2FL 5/64 LOC bit name (change to Drag Knife)


                    # new_linesTop = [f"'{self.profile_type} Ready at Top\n",
                    #                 f"'location: {self.location}"
                    #                 f"'machine: {machine}\n", 
                    #                 f"'material thickness: {thickness}\n", 
                    #                 f"'date post file updated: {today}\n", 
                    #                 "SA\n",
                    #                 "'C2\n",
                    #                 f"{moveZComment}\n",
                    #                 f"{moveZbitDiff}\n",
                    #                 f"{zZeroforBitDiff}\n",
                    #                 f"{useThickCommand}\n",
                    #                 f"{reZeroForThickCommand}\n",
                    #                 "JS,10.0,2.0,\n",
                    #                 f"JZ, {jogZHeight}\n"
                    #                 f"{useChangeBitComment}\n"
                    #                 "Pause\n",
                    #                 f"{useSpindle}SO,1,1\n",
                    #                 f"'{bitUsed}\n"
                    #                 ]
                    
                    # new_linesBottom = [ "JZ,.1\n",
                    #                     f"JZ,{jogZHeight}\n",
                    #                     f"{useSpindle}SO,1,0\n",
                    #                     f"J2,{self.homeXY}\n",
                    #                     "Pause\n",
                    #                     "'Change Bit to 1/2\" 4 Flute\n",
                    #                     f"{useThicknessDiff}MZ,-"f"{thickness}\n",
                    #                     "ZZ\n",
                    #                     "Pause\n",
                    #                     "'SafetyCheck - you're about to zero - check if you look too low\n",
                    #                     f"MZ,-{bitDifference}\n",
                    #                     "ZZ\n",
                    #                     f"{jogZHeight}\n"
                    #                     f"'{machine}\n",
                    #                     f"'{thickness} inch material thickness\n", 
                    #                     f"'{today}\n",
                    #                     "'End\n",
                    #                     f"'{self.profile_type} is Ready at Bottom"]

                    update_lines[:8] = new_linesTop
                    update_lines[-8:] = new_linesBottom
                    print(f"new_linesBottom: {new_linesBottom}")
                    update_file.writelines(update_lines)


        
            # Modify the original file with new variables
            modified_filename = f"{self.name}_{self.shoe_type}_{self.material_type}_{self.block_size}_{self.order_date}_{self.profile_type}.sbp"
            modified_filepath = os.path.join(directory, modified_filename)
            os.rename(new_filepath2, modified_filepath)


            
            print("File Modified: ", modified_filepath)

        def setupVariables(self):
        
            # Initialize variables
            # Define Variables
            self.name ="name"
            self.shoe_type ="shoe_type"
            self.material_type ="material_type"
            self.block_size ="block_size"
            self.order_date ="order_date"
            self.left_x ="left_x"
            self.left_y ="left_y"
            self.left_angle ="left_angle"
            self.right_x ="right_x"
            self.right_y ="right_y"
            self.right_angle ="right_angle"
            self.profile_type =""

            self.homeXY = ""
            self.machineName = ""
            self.zMaxDepth = ""
            self.filepath = ""
            print(f"{self.name}, {self.shoe_type}, {self.material_type}, {self.block_size}, {self.order_date}, {self.profile_type}, ")
            
        def parse_filename(self, filename):
            print("do I get to parse_filename???")
            # Set default values
            self.parsed_data = {
                "name": "Unknown",
                "shoe_type": "Unknown",
                "material_type": "Unknown",
                "block_size": "Unknown",
                "order_date": "Unknown",
                "left_x": "Unknown",
                "left_y": "Unknown",
                "left_angle": "Unknown",
                "right_x": "Unknown",
                "right_y": "Unknown",
                "right_angle": "Unknown",
                "profile_type": "Unknown"
            }
            
            # Parse filename for relevant information
            parts = re.findall(r"[^_]+", filename)
            if len(parts) >= 10:
                self.parsed_data["name"] = f"{parts[0]}_{parts[1]}"
                self.parsed_data["shoe_type"] = parts[2]
                self.parsed_data["material_type"] = parts[3]
                self.parsed_data["block_size"] = parts[4]
                self.parsed_data["order_date"] = parts[5]
                self.parsed_data["left_x"] = parts[6]
                self.parsed_data["left_y"] = parts[7]
                self.parsed_data["left_angle"] = parts[8]
                self.parsed_data["right_x"] = parts[9]
                self.parsed_data["right_y"] = parts[10]
                self.parsed_data["right_angle"] = parts[11]
                self.parsed_data["profile_type"] = parts[12]

                # self.label.setText(self.parsed_data["name"])

            return self.parsed_data
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
