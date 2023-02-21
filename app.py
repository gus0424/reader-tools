import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
# import json as w
debug = True
# Create the tkinter window
window = tk.Tk()

# Set the window title
window.title("PDF Tools")
# list = {
#     "welcome_JPN": "ようこそ",
#     "err_JPN": "エラーが発生しました。",
#     "notFound_JPN":"が見つかりませんでした",
#     "continueWith_JPN":"続けてはよろしいですか？"
# }
# Function to open a file

# print(w.dump(list))
def open_file():
    contents = ""
    file_path = filedialog.askopenfilename()
    with open(file_path, "r", encoding='cp932', errors='ignore') as file:
        contents = file.read()
    
    index = contents.find("</head>")
    if index != -1:
        headContent = """
<!-- Mobile properties -->
  <meta name="HandheldFriendly" content="True">
  <meta name="MobileOptimized" content="320">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">


  <!-- Stylesheets -->
  <link rel="stylesheet" href="css/output.68349477b267.css" type="text/css">

  <link rel="stylesheet" href="css/output.e1a9b6ead5ea.css" type="text/css">
  <link rel="stylesheet" href="css/output.ee7723a5b71e.css" type="text/css">
  <link rel="stylesheet" href="css/output.3766d7ad0d2d.css" type="text/css">
  <link rel="stylesheet" href="css/output.e3c3c2c84eb3.css" type="text/css">


  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" />

  <link type="text/css" href="css/base.6539a0a78536cfdc1fa6.css" rel="stylesheet" />


  <link rel="stylesheet" href="css/fonts/stix/stixfonts.css" type="text/css" />
  <link rel="stylesheet" href="css/3.18/pmcrefs1.min.css" type="text/css" />
  <link rel="stylesheet" href="css/pmc2020_1.1/ncbi_web.min.css?_=a" type="text/css" />
  <style type="text/css">
    .pmc-wm {
      background: transparent repeat-y top left;
      background-size: auto, contain
    }
  </style>
  <style type="text/css">
    .print-view {
      display: block
    }
  </style>

  <link type="text/css" href="css/article.053deb6b9728571514ad.css" rel="stylesheet" />
  <link type="text/css" href="css/cite-box.css" rel="stylesheet" />

        """
        contents = contents[:index] + headContent + contents[index:]
    else:
        messagebox.showerror('Error', 'Incorrect File format : Missing </head>')
        window.destroy()

    index = contents.find("</body>")
    if index != -1:
        bodyContent = """



  <!-- JavaScript -->
  <script src="js/output.0f72d6a64937.js"></script>


  <script src="https://code.jquery.com/jquery-3.5.0.min.js"
    integrity="sha256-xNzN2a4ltkB44Mc/Jz3pT4iU1cmeR0FkXs4pru/JxaQ=" crossorigin="anonymous">
    </script>
  <script>
    var fallbackJquery = "js/jquery-3.5.0.min.js";
    window.jQuery || document.write("<script src=" + fallbackJquery + ">\x3C/script>")
  </script>


  <script src="js/output.a212a9fcf845.js"></script>
  <script src="js/output.7999321d1aac.js"></script>
  <script src="js/output.7ca436b2ea51.js"></script>
  <script src="js/output.f8422046fbe0.js"></script>
  <script src="js/output.ff40c7d85ff8.js"></script>
  <script src="js/output.a6a84a0ad361.js"></script>

  <script type="text/javascript" src="js/base.54110350c77632754ed7.js"></script>

  <script type="text/javascript">
    if (typeof jQuery !== 'undefined') {
      jQuery.migrateMute = true;
    }
  </script>
  <script type="text/javascript" src="js/content0.js"></script>
  <script type="text/javascript" src="js/jig.nojquery.min.js">//</script>
  <script type="text/javascript" src="js/common.min.js?_=3.18">//</script>
  <script type="text/javascript" src="js/NcbiTagServer.min.js?_=3.18">//</script>
  <script type="text/javascript" src="js/crb.min.js?_=3.18">//</script>
  <script type="text/javascript" src="js/jactions.min.js?_=3.18">//</script>
  <script type="text/javascript"
    src="js/content1.js">//</script>
  <link rel="stylesheet" href="css/content0.css" type="text/css" />
  <script type="text/javascript">window.name = "mainwindow";</script>

  <script type="text/javascript">var exports = {};</script>
  <script src="js/output.340a3b9cce7f.js"></script>
  <script src="js/output.6cf6664daa2b.js"></script>
  <script type="text/javascript" src="js/article.e0db9c31af5bbd095194.js"></script>
  <script type="text/javascript">
    window.ncbi.pmc.articlePage.init({ pageURL: '/pmc/articles/PMC8193482/', citeCookieName: 'pmc-cf' });
  </script>
  <script type="text/javascript" src="js/content2.js"> </script>

        """
        contents = contents[:index] + bodyContent + contents[index:]
    else:
        messagebox.showerror('Error', 'Incorrect File format : Missing </body>')
        window.destroy()
    refIndex = -2
    refText = ["REFERENCES","References","references"]

    for ref in refText:
        refIndex = contents.find(ref)
        if refIndex != -1:
            break
    
    if refIndex == -1:
        messagebox.showerror('Error', 'No Reference point found')
        window.destroy()
    
    
    head = contents[:contents.find("</head>")]
    body = contents[contents.find("</head>"):refIndex]
    refContent = contents[refIndex:contents.find("</body>")]
    theRest = contents[contents.find("</body>"):]



    i = 0
    
    lastRef = False
    refSkip = False
    while 1:
        i+=1
        strI = str(i)
        strNextI = str(i+1)
        refContentIndexBegin = refContent.find("""<li data-list-text="["""+strI+"""]">""")
        if debug : print("Iteration : "+strI+",  refContentIndexBegin :"+str(refContentIndexBegin))
        if body.find("["+strI+"]") == -1: #no more ref
            if i == 1:
                messagebox.showerror("Error","Reference format is incorrect or is init with more than [1]")
                window.destroy()
            break
          
        elif body.find("["+strNextI+"]") == -1:
            lastRef = True
        

        if refContentIndexBegin == -1 and i == 1:
            if messagebox.askyesno("Error","Cannot phase given reference format /n Do you want to continue without reference POP-UP"):
                refSkip = True
            else:
                window.destroy()
        
        if not refSkip:
          injectRef = "[<a href='#ref"+strI+"' rid='ref"+strI+"' class='bibr popnode' role='button' aria-expanded='false' aria-haspopup='true'>"+strI+"</a>]"

          body.replace("["+strI+"]",injectRef)

          refPlaceHolder1 = "<div class='ref-cit-blk half_rhythm' id='ref"+strI+"'>"+strI+". <span class='element-citation'>"
          refPlaceHolder2 = "</span></div><br>"
          refCollector = ""
          if lastRef:
              lastRefPart = refContent[refContentIndexBegin:]
              lastRefPart = lastRefPart[:lastRefPart.find("</li>")]

              refContent.replace(lastRefPart,refPlaceHolder1+lastRefPart+refPlaceHolder2)
              refCollector = refPlaceHolder1+lastRefPart+refPlaceHolder2 # for debugging purpose
          else:
              refContentIndexEnd = refContent.find("""</li><li data-list-text="["""+strNextI+"""]">""")
              if debug : print(" refContentIndexEnd :"+str(refContentIndexEnd))
              refPart = refContent[refContentIndexBegin:refContentIndexEnd]
              refContent.replace(refPart,refPlaceHolder1+refPart+refPlaceHolder2)

              refCollector = refPlaceHolder1+refPart+refPlaceHolder2 # for debugging purpose


          if debug:
            if lastRef: messagebox.showinfo("Debug","Current index : "+strI+", \n This is the last reference index  \n\n ref text point preview from : "+str(body.find(injectRef)-5)+" to "+str(body.find(injectRef)+5)+":\n\n"+body[body.find(injectRef)-5:body.find(injectRef)+5]+"\n\n the ref collection preview : \n\n"+refCollector)
            else: messagebox.showinfo("Debug","Current index : "+strI+" \n ref text point preview: :\n\n"+body[body.find(injectRef)-5:body.find(injectRef)+5]+"\n\n the ref collection preview : \n\n"+refCollector)



    finalDoc = head+body+refContent+theRest
    print(finalDoc)

    print("header : "+head)
    print("body :"+body)
    print("refPart :"+refContent)
    print("the rest"+theRest)

    f = open("file.html", "a")
    f.write(finalDoc)
    f.close()

    url = "file.html"
    webbrowser.open(url,new=2)

# Create a button to open a file
button = tk.Button(window, text="Get Started", command=open_file)
button.pack()

# Run the window loop
window.mainloop()
