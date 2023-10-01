from gatingDesign.gatingDesign import CalcArea ,CalcRiser
# from saveFile import savecsv_gating,savecsv_riser
from gatingDesign.saveFile import SaveFile
import easygui

class DesignGUI:
    def __init__(self,inptype="input") -> None:
        self.msg = "Enter your gating information"
        self.title = "\tGating System calculate Application"
        self.mainMsg = "\t\tยินดีต้อนรับสู่โปรแกรมคำนวณระบบ Gating สำหรับงานหล่อ แบบพิมพ์ข้อมูล\n\n\t\t\t...กรุณาเลือกการคำนวณด้านล่าง..."
        self.fieldNamesGating = ["Head", "LossFactor", "FlowRate", "CastingHeight_P", "TotalCasting_C", "Name","GateTH"]
        self.fieldNamesRiser = ["Material", "CastingWt", "CastingMod", "ColdRiser?", "NeckHeight"]
        self.calcGating = CalcArea
        self.calcRiser = CalcRiser
        self.images = ["images/SlimGating.jpg"]
        self.choices = ["GatingSystem","RiserSystem","Exit","Setting"]
        self.inpType = inptype

    def setCalcClass(self,calcGating,calcRiser):
        self.calcGating = calcGating
        self.calcRiser = calcRiser

    def setMsgTitle(self,msg,title):
        self.msg = msg
        self.title = title

    def setFieldGating(self,fieldGating):
        self.fieldNamesGating = fieldGating

    def SetFieldRiser(self,fieldRiser):
        self.fieldNamesRiser = fieldRiser

    def setImages(self,images):
        self.images = images

    def setChoices(self,choices):
        self.choices = choices

    def inputs(self,msg,title,fieldNames):
        fieldValues = easygui.multenterbox(msg, title, fieldNames)
        if fieldValues is None:
            print('no calc')
            return None
        # make sure that none of the fields were left blank
        while 1:
            errmsg = ""
            for i, name in enumerate(fieldNames):
                if fieldValues[i].strip() == "":
                    errmsg += "{} is a required field.\n\n".format(name)
            if errmsg == "":
                break # no problems found
            fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)
            if fieldValues is None:
                break
        print("Data was:{}".format(fieldValues))
        return fieldValues
    
    def selectSetting(self):
        msg ="Select parameter to edit"
        title = "Setting calc parameter"
        choices = ["Molten_density(6.9e-6)", "Iron_density(7.2e-6)", "Hot_riser_eff(0.17)",
                "Cold_riser_eff(0.12)","FC_modulus_ratio(1:0.35:1.2)","FCD_modulus_ratio(1:0.45:1.4)",
                "FC_shrinkage_factor(3%)","FCD_shrinkage_factor(4%)","FC_tensile_str(300)","FCD_tensile_str(550)"]
        choice = easygui.choicebox(msg, title, choices)
        return choice,choices

    def setting(self):
        msg ="Select parameter to edit"
        title = "Setting calc parameter"
        choice,choices = self.selectSetting()
        if choice == choices[0]:
            fieldValues = easygui.multenterbox(msg, title, [choices[0]])
            if fieldValues is not None:
                self.calcGating.density = float(fieldValues[0])
                print('Melt density :',self.calcGating.density)
        if choice == choices[1]:
            fieldValues = easygui.multenterbox(msg, title, [choices[1]])
            if fieldValues is not None:
                self.calcRiser.density = float(fieldValues[0])
                print('Solid density :',self.calcRiser.density)
        if choice == choices[2]:
            fieldValues = easygui.multenterbox(msg, title, [choices[2]])
            if fieldValues is not None:
                self.calcRiser.hot_fac = float(fieldValues[0])
                print('Hot riser :',self.calcRiser.hot_fac)
        if choice == choices[3]:
            fieldValues = easygui.multenterbox(msg, title, [choices[3]])
            if fieldValues is not None:
                self.calcRiser.cold_fac = float(fieldValues[0])
                print('Cold riser :',self.calcRiser.cold_fac)
        if choice == choices[4]:
            feildChoice = ["FC_neck_ratio","FC_riser_ratio"]
            fieldValues = easygui.multenterbox(msg, title, feildChoice)
            if fieldValues is not None:
                self.calcRiser.ratio["FC"]["neck"] = float(fieldValues[0])
                self.calcRiser.ratio["FC"]["riser"] = float(fieldValues[1])
                print('Ratio neck FC :',self.calcRiser.ratio)
        if choice == choices[5]:
            feildChoice = ["FCD_neck_ratio","FCD_riser_ratio"]
            fieldValues = easygui.multenterbox(msg, title, feildChoice)
            if fieldValues is not None:
                self.calcRiser.ratio["FCD"]["neck"] = float(fieldValues[0])
                self.calcRiser.ratio["FCD"]["riser"] = float(fieldValues[1])
                print('Ratio neck FCD :',self.calcRiser.ratio)
        if choice == choices[6]:
            fieldValues = easygui.multenterbox(msg, title, [choices[6]])
            if fieldValues is not None:
                self.calcRiser.ratio["FC"]["casting"] = float(fieldValues[0])
                print('Ratio casting FC :',self.calcRiser.ratio)
        if choice == choices[7]:
            fieldValues = easygui.multenterbox(msg, title, [choices[7]])
            if fieldValues is not None:
                self.calcRiser.ratio["FCD"]["casting"] = float(fieldValues[0])
                print('Ratio casting FCD :',self.calcRiser.ratio)
        if choice == choices[8]:
            fieldValues = easygui.multenterbox(msg, title, [choices[8]])
            if fieldValues is not None:
                self.calcRiser.ratio["FC"]["TS"] = float(fieldValues[0])
                print('Ratio TS FC :',self.calcRiser.ratio)
        if choice == choices[9]:
            fieldValues = easygui.multenterbox(msg, title, [choices[9]])
            if fieldValues is not None:
                self.calcRiser.ratio["FCD"]["TS"] = float(fieldValues[0])
                print('Ratio TS FCD :',self.calcRiser.ratio)

    def run(self):
        i = 0
        image = self.images[0]
        save = SaveFile()

        while True:
            reply = easygui.buttonbox(self.mainMsg,title="Gating System Design", image=image, choices=self.choices)
            # print(reply)
            if reply == self.choices[3]:
                self.setting()

            if reply == self.choices[2]:
                break

            if reply == image:
                # print(image)
                i +=1
                if i >= len(self.images):
                    i = 0
                image = self.images[i]

            if reply == self.choices[0]:
                if self.inpType == "file":
                    fname = easygui.fileopenbox(default="*.csv",title="Open input parameter gating calc file")
                    # open with text file
                    with open(fname, mode ='r',encoding='utf-8') as f: 
                        header = f.readline()
                        lines = [line.strip().split(',') for line in f.readlines()]
                        for line in lines :
                            r = self.calcGating(float(line[0]),float(line[1]),float(line[2]),float(line[3]),float(line[4]),str(line[5]),float(line[6]))
                            r.save()
                if self.inpType == "input":
                    data = self.inputs(self.msg,self.title,self.fieldNamesGating)
                    if data is not None:
                        r = self.calcGating(float(data[0]),float(data[1]),float(data[2]),float(data[3]),float(data[4]),str(data[5]),float(data[6]))
                        r.save()

                disp = str(save.gating_header)+'\n'
                for i,d in enumerate(self.calcGating.data):
                    i +=1
                    disp += str(i)+' : '+str(d)+'\n'
                print(disp)
                yn = easygui.ynbox(disp + "\n\nDo you want to save result","Gating calculate result")
                if yn :
                    fsave = easygui.filesavebox(default="results.csv",title='Save result file name')
                    save.setdata(fsave,self.calcGating.data,"gating")
                    save.save2csv()
                    # easygui.msgbox(f'Success save result to file: {fsave} ')
                    print(f'Success save result to file: {fsave} ')

            if reply == self.choices[1]:
                if self.inpType == "file":
                    fname = easygui.fileopenbox(default="*.csv",title="Open input parameter riser calc file")
                    # open with text file
                    with open(fname, mode ='r',encoding='utf-8') as f: 
                        header = f.readline()
                        lines = [line.strip().split(',') for line in f.readlines()]
                        for line in lines :
                            r = self.calcRiser(str(line[0]),float(line[1]),float(line[2]),int(line[3]),float(line[4]))
                            r.save()
                if self.inpType == "input":
                    data = self.inputs(self.msg,self.title,self.fieldNamesRiser)
                    if data is not None:
                        r = self.calcRiser(str(data[0]),float(data[1]),float(data[2]),int(data[3]),float(data[4]))
                        r.save()

                disp = str(save.riser_header)+'\n'
                for i,d in enumerate(self.calcRiser.data):
                    i +=1
                    disp += f'riser {i} : {d}\n'
                print(disp)
                yn = easygui.ynbox(disp + "\n\nDo you want to save result","Riser calculate result")
                if yn :
                    fsave = easygui.filesavebox(default="results.csv",title='Save result file name')
                    save.setdata(fsave,self.calcRiser.data,"riser")
                    save.save2csv()
                    # easygui.msgbox(f'Success save result to file: {fsave} ')
                    print(f'Success save result to file: {fsave} ')

        print('...ขอบคุณที่ใช้บริการ...')





