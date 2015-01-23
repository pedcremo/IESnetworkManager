import os
#APPLICATION_DIR = os.path.dirname( globals()[ '__file__' ] )
APPLICATION_DIR = os.path.dirname( __file__)
#APPLICATION_DIR = os.path.abspath( __file__)
#APPLICATION_DIR = os.path.basename( __file__)
APPLICATION_DIR= os.path.split(os.path.abspath(__file__))[0]
APPLICATION_DIR= os.path.split(os.path.abspath(APPLICATION_DIR))[0]
APPLICATION_DIR= os.path.split(os.path.abspath(os.path.split(os.path.abspath(__file__))[0]))[0]


print "APP DIR ="+APPLICATION_DIR
print "PPPP "+os.path.join( APPLICATION_DIR,"aules/js/jquery")
