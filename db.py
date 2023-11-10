def calldb(npl):
    print("function called ")
    f=open('carDBExt.json',encoding='utf-8')
    data=json.load(f)
    passid=next(item for item in data['cardetails'] if item["CarRegistration"] == npl)   
    openNewWindow(passid)
    print(passid)
def openNewWindow(passid):
     
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(top)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
 
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
 
    # A Label widget to show in toplevel
    Label(newWindow,
          text =passid["Username"]).pack() 
    Label(newWindow,
          text =passid["CarRegistration"]).pack() 
    Label(newWindow,
          text =passid["CarMake"]).pack() 
    Label(newWindow,
          text =passid["CarModel"]).pack() 
    Label(newWindow,
          text =passid["CarColour"]).pack() 
    Label(newWindow,
          text =passid["AccountBalance"]).pack() 