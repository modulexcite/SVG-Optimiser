#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
import re

# Regex
re_translate = re.compile('\((-?\d+\.?\d*)\s*,?\s*(-?\d+\.?\d*)\)')

def printNode(node):
    print node.tag

def translateRect(rect, (dx, dy)):
    x = float(rect.get('x', 0)) + float(dx)
    y = float(rect.get('y', 0)) + float(dy)
    
    rect.set("x", "%.2f" % x)
    rect.set("y", "%.2f" % y)
    
    del rect.attrib['transform']

class CleanSVG:
    def __init__(self, svgfile=None):
        self.tree = ElementTree()
        self.root = None
        
        if file:
            self.parseFile(svgfile)
            
    def parseFile(self, filename):
        self.tree.parse(filename)
        self.root = self.tree.getroot()
        
    def write(self, filename):
        self.tree.write(filename)
    
    def _traverse(self, node, func=printNode):
        """ Call a passed function with a node and all its descendents. """
        
        func(node)
        
        for child in node.getchildren():
            self._traverse(child, func)

    def findTransforms(self):
        self._traverse(self.root, func=self.handleTransforms)

    def handleTransforms(self, node):
        #printNode(node)
        
        if 'transform' in node.keys():
            print " -transform"
            transform = node.get('transform')
            
            if "translate" in transform:
                print " -translate by:", transform
                translation = re_translate.search(transform).group(1, 2)
                if node.tag.split('}')[1] == 'rect':
                    translateRect(node, translation)

def main():
    import os
    filename = os.path.join('examples', 'translations.svg')
    s = CleanSVG(filename)
    s.findTransforms()
    s.write('%s_test.svg' % filename[:-4])
    
if __name__ == "__main__":
    main()