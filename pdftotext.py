import tkinter as tk
from tkinter import filedialog as f
from tkinter import messagebox as msg
import PyPDF2
import webbrowser
import re

app = tk.Tk()# main process
app.title('PDF Tools')

def convert():
    text = []
    file_path = f.askopenfilename()
    # Open the PDF file
    with open(file_path, 'rb') as file:

    # Create a PDF reader object
        reader = PyPDF2.PdfFileReader(file)
        

    # Iterate over the pages
        for i in range(reader.getNumPages()):

        # Get the page object
            page = reader.getPage(i)

        # Extract the text and append it to the string variable
            text.append(page.extractText())
            

# Print the entire text
    
    texts = ""
    for i in text:
        texts += i
    
    texts = texts.replace('\n','<br>')
    # print(texts)

    refIndex = -2
    refText = ["REFERENCES","References","references"]

    for ref in refText:
        refIndex = texts.find(ref)
        if refIndex != -1:
            break
    
    if refIndex == -1:
        msg.showerror('Error', 'No Reference point found')
        app.destroy()
    
    para_text = texts[:refIndex]
    ref_text = texts[refIndex:]

    print(ref_text)
    # Define the regular expression pattern to find pattern with "[ ]" with string inside
    pattern = r'\[(\d+(?:[\s,]+\d+)*)\]'

    def replace(match):
    # Get the citation numbers as a list by splitting using , 
      citations = match.group(1).split(',')
    # We then Generate the HTML code for each citation # {cite.strip()} and put in proper format
      html_citations = [f"<a href='#ref{cite.strip()}' rid='ref{cite.strip()}' class='bibr popnode' role='button' aria-expanded='false' aria-haspopup='true'>{cite.strip()}</a>" for cite in citations]
    # Join the HTML code with commas and return it as the replacement string
      return '[' + ', '.join(html_citations) + ']'

    # Use re.sub() to replace the matches with the replacement string
    para_text = re.sub(pattern, replace, para_text)
    
    citations = re.findall(r'\[(\d+)\] (.*?)\[', ref_text)

    # Loop over the citations and wrap each one in a div tag
    output_str = ""
    for index, citation in enumerate(citations):
        ref_id = "ref" + citation[0]
        output_str += f'<div class="ref-cit-blk half_rhythm" id="{ref_id}">[{citation[0]}] {citation[1]}</div><br>'

    headContent = """
    <!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

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
  </head>

        """

    bodyContent = """
  <!-- End of References -->
  <div id="body-link-poppers"><span></span></div>
  <script type="text/javascript">
    var nwds_version = "1.1.9-2";

    var meta_nwds_ver = document.createElement('meta');
    meta_nwds_ver.name = 'ncbi_nwds_ver';
    meta_nwds_ver.content = nwds_version;
    document.getElementsByTagName('head')[0].appendChild(meta_nwds_ver);

    var meta_nwds = document.createElement('meta');
    meta_nwds.name = 'ncbi_nwds';
    meta_nwds.content = 'yes';
    document.getElementsByTagName('head')[0].appendChild(meta_nwds);

    var alertsUrl = "js/alerts.js";
    if (typeof ncbiBaseUrl !== 'undefined') {
      alertsUrl = ncbiBaseUrl + alertsUrl;
    }
  </script>


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
 </body>
</html>
        """
    
    finalDoc = headContent+para_text+output_str+bodyContent
    
    f2 = open("file7.html", "w", encoding='utf-8')
    f2.write(finalDoc)
    f2.close()

    url = "file7.html"
    webbrowser.open(url,new=2)

    app.destroy()
    return

def tutorial(): # Tutorial Page
    tu = tk.Tk()
    tu.title('Tutorial')

    tu.mainloop()

def about(): # About Page
    ab = tk.Tk()
    ab.title('About')

    ab.mainloop()



button0 = tk.Button(app, text="Get Started", command=convert)
button0.pack()
button1 = tk.Button(app, text="Tutorial", command=tutorial)
button1.pack()
button2 = tk.Button(app, text="About", command=about)
button2.pack()

app.mainloop()