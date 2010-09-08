

import os


macros_fname="/workspace/math/notes/macros.tex"
preamble_fname="/workspace/math/notes/preamble.tex"

analysis_dir="/workspace/math/notes/analysis/"
temp_dir="/workspace/math/notes/temp/"
analysis_chapters=[ 'complex_measures', 'calculus', 'probability', 'topology', 'radon_measures', 'functional_analysis' ]



macros_file=open(macros_fname, 'r')
preamble_file=open(preamble_fname, 'r')
macros = [ line for line in macros_file ]
preamble = [ line for line in preamble_file ]
macros_file.close()
preamble_file.close()


for chapter in analysis_chapters:
    
    lines=[]
    lines.extend(preamble)
    lines.extend(macros)
    lines.append('\n\\begin{document}\n')
    file = open( analysis_dir+chapter+'.tex' , 'r' )
    lines.extend([line for line in file])
    file.close()
    lines.append('\n\\end{document}\n')
    file = open( temp_dir+chapter+'.tex' , 'w' )
    for line in lines:
        file.write(line)
    file.close()
    
    os.system( "pdflatex " + temp_dir+chapter+'.tex' )


lines=[]
lines.extend(preamble)
lines.extend(macros)
lines.append('\n\\begin{document}\n')

for chapter in analysis_chapters:
    
    file = open( analysis_dir+chapter+'.tex' , 'r' )
    lines.extend([line for line in file])
    file.close()

lines.append('\n\\end{document}\n')
file = open( temp_dir+'analysis'+'.tex' , 'w' )
for line in lines:
    file.write(line)
file.close()
os.system( "pdflatex " + temp_dir+'analysis'+'.tex' )
    





os.system("rm *.log")
os.system("rm *.dvi")
os.system("rm *.aux")











