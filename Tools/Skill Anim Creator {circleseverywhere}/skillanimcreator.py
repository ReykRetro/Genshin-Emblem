import re, os, sys, subprocess

#TODO: add boolean for defender anim, and sound param
#fix case when txt file is not in same folder

def show_exception_and_exit(exc_type, exc_value, tb):
  import traceback
  traceback.print_exception(exc_type, exc_value, tb)
  input("Press Enter key to exit.")
  sys.exit(-1)

class SkillAnim(object):
  """docstring for SkillAnim"""
  def __init__(self, path):
    super(SkillAnim, self).__init__()
    self.path = path
    self.pathfolder = os.path.dirname(os.path.realpath(self.path))
    self.scriptpath = os.path.dirname(os.path.realpath(sys.argv[0]))
    self.name = os.path.split(path)[1]
    self.name = os.path.splitext(self.name)[0].replace(' ','_').replace('-','_')
    if self.name[0].isdigit():
      self.name = '_'+self.name
    self.frames = "Frames:    //SHORT image duration\n"
    self.frame_end = "SHORT 0xFFFF\nALIGN 4\n"    
    self.tsalist = "TSAList:\n"
    self.graphicslist = "GraphicsList:\n"
    self.paletteslist = "PalettesList:\n"
    self.tsa = ""
    self.graphics = ""
    self.palettes = ""
    self.sound = "0x3d1"
    self.dmp = "skillanimtemplate.dmp"
    self.defend = False
    self.scriptData = []

  def process_script(self):
    """Script format is:
    #frames image.png
    e.g.
    S1234 #play sound 0x1234
    D #is defender anim
    5 frame1.png
    5 frame2.png
    """
    outputpath = os.path.splitext(self.path)[0]+'.event'
    pattern = re.compile(r"""(\d+)                  # duration
                            \s+                 # space
                            ([\w-]+\.[Pp][Nn][Gg]| # filename
                            ".+\.[Pp][Nn][Gg]") # filename with spaces
                      """, re.X)
    with open(self.path, 'r') as script:
      lines = script.readlines()
      script = [line.strip() for line in lines if (line.strip() != "")]
    for line in script:
      if line[0] == "S": #lines beginning with S set the sound
        self.sound = "0x"+line[1:]
      elif line[0] == "D": #line beginning with D means defender anim
        self.defend = True
        self.dmp = "skillanimtemplate_defender.dmp"
      elif line[0].isdigit(): #otherwise format is [duration] [path]
        match = pattern.match(line)
        if match:
          self.scriptData.append(match.group(1,2))
    framesref = {}
    for dat in self.scriptData:
      duration = dat[0]
      path = dat[1]
      basepath = os.path.splitext(path)[0].replace('"','')
      label = basepath.replace(' ','_').replace('-','_')
      try:
        num = framesref[path]
      except KeyError:
        framesref[path] = len(framesref)
        os.chdir(self.pathfolder)
        self.gritify(os.path.join(self.pathfolder, path))
        os.chdir(self.scriptpath)
        num = framesref[path]
        self.tsa += 'TSA_{}:\n#incbin "{}.map.bin"\n'.format(label,basepath)
        self.graphics += 'Graphics_{}:\n#incbin "{}.img.bin"\n'.format(label,basepath)
        self.palettes += 'Pal_{}:\n#incbin "{}.pal.bin"\n'.format(label,basepath)
      self.frames += 'SHORT {} {}\n'.format(num, duration)
      self.tsalist += 'POIN TSA_{}\n'.format(label)
      self.graphicslist += 'POIN Graphics_{}\n'.format(label)
      self.paletteslist += 'POIN Pal_{}\n'.format(label)

    output = """//Generated with Skill Animation Creator.

#incbin {9}
POIN Frames
POIN TSAList
POIN GraphicsList
POIN PalettesList
WORD {8} //sound id

{0}{1}
{2}
{3}
{4}
{5}
{6}
{7}""".format(self.frames,self.frame_end,self.tsalist,self.graphicslist,self.paletteslist,self.tsa,self.graphics,self.palettes,self.sound,self.dmp)
    with open(outputpath,'w') as outfile:
      outfile.write(output)


  def gritify(self, path_):
    grit_path = os.path.join(os.path.join(self.scriptpath, "grit"), 'grit')
    # print(grit_path, path_)
    subprocess.run([grit_path, path_, '-gB', '4', '-gzl', '-m', '-mLf', '-mR4', '-mzl', '-pn', '16', '-ftb', '-fh!'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
  sys.excepthook = show_exception_and_exit
  assert len(sys.argv) > 1, "No script given. Drag and drop a script onto the program to run."
  a = SkillAnim(sys.argv[1])
  a.process_script()

if __name__ == '__main__':
  main()
