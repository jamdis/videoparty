#! /usr/bin/python

#
# Based on Qt example for VLC Python bindings
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import os.path
import vlc
import random
import math
from PyQt4 import QtGui, QtCore
import sqlite3

class ClipDb(object):
    """The sqlite3 database that records all clips
    """
    
    def __init__(self):
        print "connecting to database"
        self.conn = sqlite3.connect("clips.db")
        self.cursor = self.conn.cursor()
        self.newClip("test2",1000,2000)
    
    def  newClip(self, title, inpoint, outpoint):
        print "adding test record"
        self.cursor.execute("INSERT INTO clips (title, inpoint, outpoint) VALUES('test', 100, 200)")
        self.conn.commit()
        self.conn.close()
        

class MediaFile(object):
    """Represents a single video file.
    """
    def __init__(self, filename = None):
        print "I'm a new mediaFile!"
        if (filename == None):
            print "No Filename"
            self.openFile()
        else:
            print "filename defined!"
            self.filename = filename
    
    def openFile(self):
        global player
        self.filename = QtGui.QFileDialog.getOpenFileName(player, "Open File", os.path.expanduser('~/Videos'))
        

class Player(QtGui.QMainWindow): #player extends the QT mainWindow Object
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        
        # create a list of media files
        self.playlist = []

        self.createUI()
        self.isPaused = False
    
    def keyPressEvent(self, event):
        key_pressed = event.text()
        print "You pressed..." + key_pressed
        print event.key()
        if(key_pressed == " "):
            self.PlayPause()
        elif(key_pressed == "i"):
            self.setInpoint(self.mediaplayer.get_time())
        elif(key_pressed == "o"):
            self.setOutpoint(self.mediaplayer.get_time())
        elif(key_pressed == "x"):
            self.mediaplayer.next_frame()
        elif(key_pressed == "z"):
            fps = self.mediaplayer.get_fps()
            frame_duration = round((1 / fps) * 1000) 
            self.mediaplayer.set_time(self.mediaplayer.get_time() - int(frame_duration))
    
    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette() #palette is where the video is drawn?  Not currently used bc video plays in its own box.
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.hbuttonbox = QtGui.QHBoxLayout() #button box is where the buttons live.
        self.playbutton = QtGui.QPushButton("Play") #Create the play button
        self.hbuttonbox.addWidget(self.playbutton) #add the play button to the button box.
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"), #connect clicking button to the playpause function.
                     self.PlayPause)

        self.stopbutton = QtGui.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)
                     
        #New Clip Button
        self.new_clipbutton = QtGui.QPushButton("New Clip")
        self.hbuttonbox.addWidget(self.new_clipbutton)
        self.connect(self.new_clipbutton, QtCore.SIGNAL("clicked()"), self.newClip)
        
        #media title label
        self.media_title_label = QtGui.QLabel("MEDIA-TITLE")
        self.hbuttonbox.addWidget(self.media_title_label)
        
        #media inpoint label
        self.inpoint_label = QtGui.QLabel("IN:0")
        self.hbuttonbox.addWidget(self.inpoint_label)
        
        #media outpoint label
        self.outpoint_label = QtGui.QLabel("OUT:0")
        self.hbuttonbox.addWidget(self.outpoint_label)
        

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open = QtGui.QAction("&Open", self)
        self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self) #every 200 ms(?) update the UI
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)
                         
    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile() #if the player has no video, call openFile.
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False
            #self.mediaplayer.toggle_fullscreen(); #doesn't work!
            print "You are pressing a button!"

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def showMediaTitle(self, newTitle):
        """Change the text that shows the media title
        """
        self.media_title_label.setText(newTitle)
        
    def setInpoint(self, new_inpoint):
        """Change the text that shows the inpoint
        """
        self.inpoint_label.setText("IN: " + str(new_inpoint))
    
    def setOutpoint(self, new_outpoint):
        """Change the text that shows the outpoint
        """
        self.outpoint_label.setText("OUT: " + str(new_outpoint))
        
    def showMediaTitle(self, new_outpoint):
        """Change the text that shows the media title
        """
        self.media_title_label.setText(str(new_outpoint))
        
    def newClip(self):
        """make a new clip
        """
        print "You clicked it!"
        self.playlist.append(MediaFile())
        self.showMediaTitle("Fart")
        

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~/Videos'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))
        
        self.showMediaTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()
    
    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)
    
    
    def updateUI(self):
        """updates the user interface"""
        #John's weird random looping:
        #print self.mediaplayer.get_time()
        #if(self.mediaplayer.get_time() > 5000):
        #   self.mediaplayer.set_time(random.randint(0,5000))
        
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

from videopartyui import Ui_MainWindow
__version__ = "0.0.00"
import sys
from PyQt4.QtGui import (QMainWindow, QApplication)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)                                         
        self.setupUi(self)

if __name__ == "__main__": #run the player
    #clipDb = ClipDb()
    app = QtGui.QApplication(sys.argv) #create the QT app
    frame = MainWindow()
    frame.show()
    app.exec_()
    #player = Player() #instantiate a player
    #player.show() #tell the player to show.  This method is inherited from the QT object
    #player.resize(640, 480) #set the size of the window
    #if sys.argv[1:]: #get the name of a file from the CLI argument to play
    #    player.OpenFile(sys.argv[1])
    #sys.exit(app.exec_())
    app = QtGui.Qapplication(sys.argv)
    




