# -*- coding: utf-8 -*-

import sys
import os


class FileRecord:
    def __init__(self, key):
        self._key = key
        self._paths = []

    def addPath(self, path):
        if path is not None:
            self._paths.append(path)

    def getPaths(self):
        return self._paths

    def getKey(self):
        return self._key

    def isHit(self):
        return len(self._paths) > 0

def parse_ext_list(line, spliter=' '):
    if line is None:
        return None

    line = line.strip()
    l = line.split(spliter)
    if len(l) > 0:
        if l[0] != 'ext':
            return None
        del l[0]

    if len(l) <= 0:
        return None

    return l

def read_name_list(inputfile):
    if not os.path.exists(inputfile):
        return None, None, None

    e = None
    d = {}
    l = []
    with open(inputfile, 'r') as f:
        for line in f:
            if e is None:
                e = parse_ext_list(line)
                if e is None:
                    return None, None, None
                continue
            if line.endswith('\n'):
                line = line.strip()
            d[line] = FileRecord(line)
            l.append(line)

    return d, e, l

def peel_file_name(name):
    sep = os.path.splitext(name)
    
    return sep[0], sep[1]

def is_ext_hit(ext, extList):
    src = ext.lower()
    for e in extList:
        if src == e.lower():
           return True
    return False

def record_file(name, fullPath, targetDict, extList):
    basename = os.path.basename(name)

    rawName, ext = peel_file_name(name)

    if is_ext_hit(ext, extList):
        record = targetDict.get(rawName)

        if record is not None:
            record.addPath(fullPath)
            return True

    return False

def search_and_copy(targetDict, extList, srcDir, outputPath):
    import shutil

    if targetDict is None or extList is None or not os.path.isdir(outputPath):
        return

    for (root, dirs, files) in os.walk(srcDir):
        for f in files:
            basename = os.path.basename(f)
            fullpath = os.path.join(root, f)
            if record_file(f, fullpath, targetDict, extList):
                targetPath = os.path.join(outputPath, f)
                shutil.copy(fullpath, targetPath)


def generate_report(targetList, targetDict, outputPath):

    f = open(outputPath, 'w')

    f.write('missing items:')

    for name in targetList:
        record = targetDict.get(name)
        if record is not None:
            if not record.isHit():
                f.write('\n' + name)

    f.close()


def help():
    appName = sys.argv[0]
    print()
    print('Dear Guliang:')
    print('this app reads target file list from the specified name-list file, searches them in src dir,')
    print('then copies hit files into output path, it also lists those were missing.')
    print('the content of name-list should be:')
    print('    ext .png .jpg .mpeg .txt // the file extens you are interested in, \'ext\' is preserved.')
    print('    name0')
    print('    name1')
    print('    name2')
    print('    name3')
    print('    ...')
    print('by default, the ourput dir is ./nepular_result.')
    print()
    print('usage:')
    print('' + appName + ' {list_file} {dir_you_want_to_search} [output_path]')
    print()
    print('good luck')

def main():
    argLen = len(sys.argv)
    inputFile = None
    srcDir = None
    outputDir = 'nepular_result'
    targetList = None
    targetDict = None
    extList = None

    if argLen > 1:
        inputFile = sys.argv[1]
        targetDict, extList, targetList = read_name_list(inputFile)
        if extList is None:
            print('you should specify extens at the first line of name-list like \'ext .jpg .png\'')
            help()
            return
        if targetList is None:
            print('invalid input list file: \'' + inputFile + '\'')
            help()
            return
            
    else:
        print('you should specify name-list')
        help()
        return

    if argLen > 2:
        srcDir = sys.argv[2]
        if not os.path.isdir(srcDir):
            print('dir not exists: ' + srcDir)
            help()
            return
    else:
        print('you should specify src dir')
        help()
        return

    if argLen > 3:
        outputDir = sys.argv[3]

    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    search_and_copy(targetDict, extList, srcDir, outputDir)

    reportPath = os.path.join(outputDir, 'report.txt')
    generate_report(targetList, targetDict, reportPath)

    print('done! result locates in ' + reportPath)

if __name__ == '__main__':
    main()