


#Creating a pdf report of the results
def make_pdf_report(n):

    header = r"""
    \documentclass[a4paper,english,12pt]{article}
    \usepackage[latin1]{inputenc}
    \usepackage[T1]{fontenc}
    \usepackage[T1]{url}
    \usepackage{amssymb, amsmath, graphicx, listings}
    \usepackage[pagebackref=true]{hyperref}
    \usepackage{verbatim}
    \urlstyle{sf}
    \begin{document}
    \title{Report iteration no %d}
    \author{Kristoffer H. Ring \\
    kristohr@ifi.uio.no}
    \date{\today}
    \maketitle{}
    \newpage
    """ % n


    tex_doc = header
    
    plot = (str(n) + "iterMin.eps", str(n) + "iterMax.eps", str(n) + "iterPre.eps")
    
    for i in range(0, 3):
        tex_doc += r"""
        \section*{Plot of %s}
        \begin{figure}[h!!]
        \centering
        \includegraphics[width=13cm]{%s}
        \caption{Bayes factor}
        \end{figure}
        \newpage""" % (plot[i], plot[i]) #Figures

    text_report = (str(n) + "orderMin.txt", str(n) + "orderMax.txt", \
                   str(n) + "orderPre.txt")

    for i in range(0, 3):
        tex_doc += r"""
        \section*{%s}
        \verbatiminput{%s}
        \newpage""" % (text_report[i], text_report[i])#Text



    tex_doc += """
    \end{document}"""

    tex_file = "result" + str(n) +".tex"
    FILE = open(tex_file, 'w')
    FILE.write(tex_doc)
    FILE.close()
    cmd = "python tex2pdf.py %s" % tex_file
    print "Converting to pdf..."
    sys.stdout.flush()
    failure, output = commands.getstatusoutput(cmd)
    print "done."
    
    if failure:
        print output
        sys.exit(1)
