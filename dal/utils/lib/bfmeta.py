#!/usr/bin/env python
#
# bfmeta.py
# Python class that retrieves header information from a BF.h5 file 
#
# File:         bfmeta.py
# Author:       Sven Duscha (duscha_at_astron.nl)
# Date:         2012-03-02
# Last change:  2012-07-18

import sys
import dal

class bfmeta:
  def __init__(self, fh=0, filename="", tabs=True, color=False, sap="all", beam="all", stokes="all", level=6, verbose=False):
    if fh==0:                       # if no file handle given
      self.fh=dal.BF_File(filename)      # open file    
    else:
      self.fh=fh                        # take handle
      
    # Display attributes
    self.useTabs=tabs
    self.useColor=color
    self.prefix=""
    # Selection of SAP, Beam and Stokes to show
    self.sap=sap  
    self.level=level
    self.beam=beam
    self.stokes=stokes
    self.verbose=verbose
    self.displayInfo()

    print bcolors.ENDC    # End all colourization
    
  # High-level function to display all info, calling display ftns for classes
  #  
  def displayInfo(self):
    self.displayFileInfo()
    self.displaySAP()
    
  # Display information about BF_File
  #
  def displayFileInfo(self):
    #print "displayFileInfo()"       # DEBUG

    if self.level < 1:
      print "ROOT"
      return
    print self.fh.groupType().name(), "\t\t=", self.fh.groupType().value
    print self.fh.fileName().name(), "\t\t=", self.fh.fileName().value
    print self.fh.fileDate().name(), "\t\t=", self.fh.fileDate().value
    print self.fh.fileType().name(), "\t\t=", self.fh.fileType().value
    print self.fh.telescope().name(), "\t\t=", self.fh.telescope().value
    print self.fh.projectID().name(), "\t\t=", self.fh.projectID().value
    print self.fh.projectTitle().name(), "\t\t=", self.fh.projectTitle().value
    print self.fh.projectPI().name(), "\t\t=", self.fh.projectPI().value
    print self.fh.projectCOI().name(), "\t\t=", self.fh.projectCOI().value
    print self.fh.projectContact().name(), "\t=", self.fh.projectContact().value
    print self.fh.observationID().name(), "\t\t=", self.fh.observationID().value
    print self.fh.observationStartUTC().name(), "\t=", self.fh.observationStartUTC().value
    print self.fh.observationEndUTC().name(), "\t=", self.fh.observationEndUTC().value
    if self.fh.observationStartMJD().value != None:
      print self.fh.observationStartMJD().name(), "\t=%(mjd)19.12f" %{'mjd':self.fh.observationStartMJD().value}
    if self.fh.observationEndMJD().value != None:
      print self.fh.observationEndMJD().name(), "\t=%(mjd)19.12f" %{'mjd':self.fh.observationEndMJD().value}
#    print self.fh.observationStartTAI().name(), "\t=", self.fh.observationStartTAI().value
#    print self.fh.observationEndTAI().name(), "\t=", self.fh.observationEndTAI().value
    print self.fh.observationNofStations().name(), "=", self.fh.observationNofStations().value
    print self.fh.observationStationsList().name(), "=", self.fh.observationStationsList().value
    print self.fh.observationFrequencyMin().name(), "\t=", self.fh.observationFrequencyMin().value, self.fh.observationFrequencyUnit().value
    print self.fh.observationFrequencyCenter().name(), "\t=", self.fh.observationFrequencyCenter().value, self.fh.observationFrequencyUnit().value
    print self.fh.observationFrequencyMax().name(), "\t=", self.fh.observationFrequencyMax().value, self.fh.observationFrequencyUnit().value
    print self.fh.observationNofBitsPerSample().name(), "=", self.fh.observationNofBitsPerSample().value
    print self.fh.clockFrequency().name(), "\t=", self.fh.clockFrequency().value, self.fh.clockFrequencyUnit().value
    print self.fh.antennaSet().name(), "\t\t=", self.fh.antennaSet().value
    print self.fh.filterSelection().name(), "\t=", self.fh.filterSelection().value
    print self.fh.targets().name(), "\t\t=", self.fh.targets().value
    print self.fh.systemVersion().name(), "\t\t=", self.fh.systemVersion().value
    print self.fh.pipelineName().name(), "\t\t=", self.fh.pipelineName().value
    print self.fh.pipelineVersion().name(), "\t=", self.fh.pipelineVersion().value
    print self.fh.docName().name(), "\t\t=", self.fh.docName().value
    print self.fh.docVersion().name(), "\t\t=", self.fh.docVersion().value
    print self.fh.createOfflineOnline().name(), "\t=", self.fh.createOfflineOnline().value
    print self.fh.BFFormat().name(), "\t\t=", self.fh.BFFormat().value
    print self.fh.BFVersion().name(), "\t\t=", self.fh.BFVersion().value
    if self.fh.totalIntegrationTime().value != None:
      print self.fh.totalIntegrationTime().name(), " = %(ti).2f %(tiu)s" %{'ti':self.fh.totalIntegrationTime().value, 'tiu':self.fh.totalIntegrationTimeUnit().value}
    print self.fh.observationDatatype().name(), "\t=", self.fh.observationDatatype().value
    print self.fh.subArrayPointingDiameter().name(), " =", self.fh.subArrayPointingDiameter().value, self.fh.subArrayPointingDiameterUnit().value
    if self.fh.bandwidth().value != None:
      print self.fh.bandwidth().name(), "\t\t= %(bw).2f %(bwu)s" %{'bw':self.fh.bandwidth().value, 'bwu':self.fh.bandwidthUnit().value}
#    print self.fh.beamDiameter().name(), "\t\t=", self.fh.beamDiameter().value, self.fh.beamDiameterUnit().value
#    print self.fh.weatherTemperature().name(), "\t=", self.fh.weatherTemperature().value, self.fh.weatherTemperatureUnit().value
#    print self.fh.weatherHumidity().name(), "\t=", self.fh.weatherHumidity().value, self.fh.weatherHumidityUnit().value
#    print self.fh.systemTemperature().name(), "\t=", self.fh.systemTemperature().value, self.fh.systemTemperatureUnit().value
    print self.fh.observationNofSubArrayPointings().name(), "=", self.fh.observationNofSubArrayPointings().value
    print self.fh.nofSubArrayPointings().name(), "=", self.fh.nofSubArrayPointings().value
    
    if self.level==1:
      print self.prefix + "--------------------------------------"
  
    self.prefix=bcolors.ENDC      # reset printing options

  
  # Display Sub Array Pointing information for SAPs
  #
  def displaySAP(self):
    if self.sap=="all":
      for nr in range(0, self.fh.nofSubArrayPointings().value):   
        self.displaySAPInfo(nr)
    else:
      if isinstance(self.sap, list):
        for nr in self.sap:
          self.displaySAPInfo(nr)
      else:   # single SAP nr (int)
        self.displaySAPInfo(int(self.sap))
  
  # SAP attributes of individual SAP Nr.
  #
  def displaySAPInfo(self, nr):
    if self.useTabs:
      self.prefix=""    # SAP is high-level doesn't have a tab
    if self.useColor:
      self.prefix=self.prefix + bcolors.SAP

    if self.fh.subArrayPointing(nr).exists():
      if self.level < 2:
        if self.useColor:
          print bcolors.SAP + "   |"
          print bcolors.SAP + "   SAP_%(sap)03d" %{'sap': nr}
        else:
          print "   |"
          print "   SAP_%(sap)03d" %{'sap': nr}

        if self.fh.subArrayPointing(nr).exists():
          sap=self.fh.subArrayPointing(nr)
          self.displayBeam(sap)
        return
      if str(nr) in self.sap or self.sap=="all":
        sap=self.fh.subArrayPointing(nr)
        print self.prefix + "------------------------------------"
        print self.prefix + "SUB_ARRAY_POINTING_%(nr)03d" %{'nr': nr}
      else:
        print self.prefix + "    |"
        print self.prefix + "    SUB_ARRAY_POINTING_%(nr)03d doesn't exist." %{'nr': nr}        
        self.prefix=bcolors.ENDC
        print self.prefix
        return
    else:
      print self.prefix + "   |"
      print self.prefix + "   SUB_ARRAY_POINTING_%(nr)03d doesn't exist." %{'nr': nr}        
      self.prefix=bcolors.ENDC
      print self.prefix
      return    

    print self.prefix + sap.groupType().name() +  "\t\t= " + sap.groupType().value
    print self.prefix + sap.expTimeStartUTC().name() +  "\t= " + str(sap.expTimeStartUTC().value)
    print self.prefix + sap.expTimeEndUTC().name() +  "\t\t= " + str(sap.expTimeEndUTC().value)
    if sap.expTimeStartMJD().value != None:
      print self.prefix + sap.expTimeStartMJD().name() + "\t=%(mjd)19.12f" %{'mjd':sap.expTimeStartMJD().value}
    if sap.expTimeEndMJD().value != None:
      print self.prefix + sap.expTimeEndMJD().name() + "\t\t=%(mjd)19.12f" %{'mjd':sap.expTimeEndMJD().value}
#    if sap.expTimeStartTAI().value != None:
#      print self.prefix + sap.expTimeStartTAI().name() + "\t= %(tai)s" %{'tai':sap.expTimeStartTAI().value}
#    if sap.expTimeEndTAI().value != None:
#      print self.prefix + sap.expTimeEndTAI().name() + "\t\t= %(tai)s" %{'tai':sap.expTimeEndTAI().value}
    if sap.totalIntegrationTime().value != None and sap.totalIntegrationTimeUnit().value != None: 
      print self.prefix + sap.totalIntegrationTime().name(), " = %(ti).2f %(tiu)s" %{'ti':sap.totalIntegrationTime().value, 'tiu':sap.totalIntegrationTimeUnit().value}
    if sap.pointRA().value != None:
      print self.prefix + sap.pointRA().name() + "\t\t= %(pra)3.10f %(prau)s" %{ 'pra': sap.pointRA().value, 'prau': sap.pointRAUnit().value}
    if sap.pointDEC().value != None:
      print self.prefix + sap.pointDEC().name() + "\t\t= %(decra)4.10f %(decrau)s" %{'decra': sap.pointDEC().value, 'decrau': sap.pointDECUnit().value}
    print self.prefix + sap.pointAltitude().name() + "\t\t=", sap.pointAltitude().value, sap.pointAltitudeUnit().value   # optional attribute
    print self.prefix + sap.pointAltitude().name() + "\t\t=", sap.pointAzimuth().value, sap.pointAzimuthUnit().value      # optional attribute
    print self.prefix + sap.observationNofBeams().name() + "\t=", sap.observationNofBeams().value
    print self.prefix + sap.nofBeams().name() + "\t\t=", sap .nofBeams().value
    if self.level==2:
      print self.prefix + "--------------------------------------"

    # Beams within this SAP
    self.displayBeam(sap)
    self.prefix=bcolors.ENDC
    print self.prefix

  # Display Sub Array Pointing information for Beams
  #  
  def displayBeam(self, sap):
    #print "displayBeam()"               # DEBUG
    if self.beam=="all":
      #for n in range(0, sap.nofBeams().value):
      for n in range(0, sap.observationNofBeams().value):   
          self.displayBeamInfo(sap, int(n))
    elif isinstance(self.beam, list):
      for b in self.beam:
        self.displayBeamInfo(sap, int(b))
    else:   # single beam integer
      self.displayBeamInfo(sap, int(self.beam))

  # Display Beam information
  #  
  def displayBeamInfo(self, sap, nr):
    #print "displayBeamInfo()"
    if self.useTabs:
      self.prefix="\t"
    if self.useColor:
      self.prefix=self.prefix + bcolors.BEAM

    # Check if this beam exists in this SAP
    if sap.beam(nr).exists() and (str(nr) == self.beam or self.beam=="all"):
      beam=sap.beam(nr)
      if self.level < 3:            # display tree
        if self.useColor:
          print bcolors.BEAM + "         |"
          print bcolors.BEAM + "         BEAM_%(beam)03d" %{'beam': nr}
        else:
          print "         |"
          print "         BEAM_%(beam)03d" %{'beam': nr}

        for d in range(0, beam.observationNofStokes().value):
          self.displayStokesDatasetInfo(beam, d)
        self.displayCoordinates(beam)
        return
    else:
      if self.useTabs==False:
        print self.prefix + "                  |"
        print self.prefix + "                  BEAM_%(beam)03d doesn't exist in %(sap)s" %{'beam': self.beam, 'sap': sap.name()}
      else:
        print self.prefix + "         |"
        print self.prefix + "         BEAM_%(beam)s doesn't exist in %(sap)s" %{'beam': self.beam, 'sap': sap.name()}
        self.prefix=bcolors.ENDC
      print self.prefix
      return
    # only display beam if it is in the list to be shown
    if str(nr) not in self.beam and self.beam!="all":    
      return

    print self.prefix + "------------------------------------"
    print self.prefix + "BEAM_%(bnr)03d" %{'bnr': nr}
   
    print self.prefix + beam.groupType().name() + "\t\t= " + beam.groupType().value
    print self.prefix + beam.targets().name() + "\t\t\t=", beam.targets().value
    print self.prefix + beam.nofStations().name() +"\t\t=", beam.nofStations().value
    print self.prefix + beam.stationsList().name() + "\t\t=", beam.stationsList().value
    print self.prefix + beam.nofSamples().name() + "\t\t=", beam.nofSamples().value
    print self.prefix + beam.samplingRate().name() + "\t\t=", beam.samplingRate().value, beam.samplingRateUnit().value
    print self.prefix + beam.samplingTime().name() + "\t\t=", beam.samplingTime().value, beam.samplingTimeUnit().value
    print self.prefix + beam.channelsPerSubband().name() + "\t=", beam.channelsPerSubband().value
    print self.prefix + beam.subbandWidth().name() + "\t\t=", beam.subbandWidth().value, beam.subbandWidthUnit().value
    print self.prefix + beam.channelWidth().name() + "\t\t=", beam.channelWidth().value, beam.channelWidthUnit().value
    print self.prefix + beam.tracking().name() + "\t\t=", beam.tracking().value
    print self.prefix + beam.pointRA().name() + "\t\t=", beam.pointRA().value, beam.pointRAUnit().value
    print self.prefix + beam.pointDEC().name() + "\t\t=", beam.pointDEC().value, beam.pointDECUnit().value
    print self.prefix + beam.pointOffsetRA().name() + "\t\t=", beam.pointOffsetRA().value, beam.pointOffsetRAUnit().value
    print self.prefix + beam.pointOffsetDEC().name() + "\t=", beam.pointOffsetDEC().value, beam.pointOffsetDECUnit().value
    print self.prefix + beam.beamDiameterRA().name() + "\t=", beam.beamDiameterRA().value, beam.beamDiameterRAUnit().value
    print self.prefix + beam.beamDiameterDEC().name() + "\t=", beam.beamDiameterDEC().value, beam.beamDiameterDECUnit().value
    print self.prefix + beam.beamFrequencyCenter().name() + "\t=", beam.beamFrequencyCenter().value, beam.beamFrequencyCenterUnit().value
    print self.prefix + beam.foldedData().name() + "\t\t=", beam.foldedData().value
    print self.prefix + beam.foldPeriod().name() + "\t\t=", beam.foldPeriod().value, beam.foldPeriodUnit().value
    print self.prefix + beam.dedispersion().name() + "\t\t=", beam.dedispersion().value
#   if beam.dispersionMeasure().value != None:
#    print self.prefix + beam.dispersionMeasure().name() + "\t= %(dm) %(dmu)" %{'dm': beam.dispersionMeasure().value, 'dmu': beam.dispersionMeasureUnit().value}
    print self.prefix + beam.dispersionMeasure().name() + "\t=", beam.dispersionMeasure().value, beam.dispersionMeasureUnit().value
    print self.prefix + beam.barycentered().name() + "\t\t=", beam.barycentered().value
    print self.prefix + beam.observationNofStokes().name() + "\t=", beam.observationNofStokes().value
    print self.prefix + beam.nofStokes().name() + "\t\t=", beam.nofStokes().value
    print self.prefix + beam.stokesComponents().name() + "\t= ", beam.stokesComponents().value
    print self.prefix + beam.complexVoltage().name() + "\t\t=", beam.complexVoltage().value
    print self.prefix + beam.signalSum().name() + "\t\t=", beam.signalSum().value

    # Only beams with selected Stokes components
    if self.stokes not in beam.stokesComponents().value and self.stokes!="all":
      #print self.prefix
      self.prefix=self.prefix + bcolors.DATASET
      if self.level < 3:
        print self.prefix + "                  |"
        print self.prefix + "                  STOKES_COMPONENT_%(stokes)s doesn't exist in BEAM_%(nr)03d" %{'stokes': self.stokes, 'nr': nr}
      else:
        print self.prefix + "STOKES_COMPONENT_%(stokes)s doesn't exist in BEAM_%(nr)03d" %{'stokes': self.stokes, 'nr': nr}
        self.prefix=bcolors.ENDC
      print self.prefix
      return

    if self.level==3:
      print self.prefix + "--------------------------------------"

    # Display Stokes datasets
    for d in range(0, beam.observationNofStokes().value):
      self.displayStokesDatasetInfo(beam, d)
    self.displayCoordinates(beam)
    self.prefix=bcolors.ENDC          # reset printing options
    print self.prefix
    
  # Display info of Stokes dataset
  #
  def displayStokesDataset(self, beam, nr="all"):
    if nr=="all":
      for n in range(0, beam.observationNofStokes().value):
        self.displayStokesDatasetInfo(n)
    else:
      self.displayStokesDatasetInfo(nr)

  def displayStokesDatasetInfo(self, beam, nr):
    if self.useTabs==True:
      self.prefix="\t\t"
    if self.useColor==True:
      self.prefix=self.prefix + bcolors.DATASET

    if beam.stokes(nr).exists():
      stokes=beam.stokes(nr)
      if self.stokes == "all" or stokes.stokesComponent().value == self.stokes:
        if self.level < 4:
          if self.useTabs:
            print self.prefix + "|"
            print self.prefix + "STOKES_%(stokes)03d" %{'stokes': nr}
          else:    
            print self.prefix + "                |"
            print self.prefix + "                STOKES_%(stokes)03d" %{'stokes': nr}
          return
        else:
          stokes=beam.stokes(nr)
          print self.prefix + "------------------------------------"
          print self.prefix + stokes.stokesComponent().name() + "\t=", stokes.stokesComponent().value    
          print self.prefix + stokes.dataType().name() + "\t\t=", stokes.dataType().value    
          print self.prefix + stokes.nofSamples().name() + "\t\t=", stokes.nofSamples().value    
          print self.prefix + stokes.nofSubbands().name() + "\t\t=", stokes.nofSubbands().value    
          print self.prefix + stokes.nofChannels().name() + "\t\t=", stokes.nofChannels().value        
          self.prefix=bcolors.ENDC        # reset printing options     
          print self.prefix
      if self.level==4:
        print self.prefix + "--------------------------------------"
    else:
      return
    
  # Display coordinategroup info (only in verbose mode)
  #
  def displayCoordinates(self, beam):
    if self.useTabs==True:
      self.prefix="\t\t\t"
    if self.useColor==True:
      self.prefix=self.prefix + bcolors.COORD

    if self.level < 5:
      if self.useTabs:
        print "\t\t|"
        print "\t\tCOORDINATES"
      else:    
        print bcolors.COORD + "                |"
        print bcolors.COORD + "                COORDINATES"
      coords=beam.coordinates()
      for c in range(0, coords.nofCoordinates().value):
        self.displayCoordinate(coords, c)
      return
    print self.prefix + "----------------------------------"
    #print self.prefix + "Coordinates"
    if beam.coordinates().exists()==False:
      return
    else:
      coords=beam.coordinates()
      # This is buggy in the Swig bindings
      print self.prefix + coords.groupType().name() + "\t\t=", coords.groupType().value
      print self.prefix + coords.refLocationValue().name() + "\t=", coords.refLocationValue().value, coords.refLocationUnit().value
      print self.prefix + coords.refLocationFrame().name() + "\t=", coords.refLocationFrame().value
      print self.prefix + coords.refTimeValue().name() + "\t\t=", coords.refTimeValue().value, coords.refTimeUnit().value
      print self.prefix + coords.refTimeFrame().name() + "\t\t=", coords.refTimeFrame().value
      print self.prefix + coords.nofCoordinates().name() + "\t\t=", coords.nofCoordinates().value
      print self.prefix + coords.nofAxes().name() + "\t\t=", coords.nofAxes().value
      print self.prefix + coords.coordinateTypes().name() + "\t=", coords.coordinateTypes().value

      if self.level==5:
        print self.prefix + "--------------------------------------"

      for c in range(0, coords.nofCoordinates().value):
        self.displayCoordinate(coords, c)
        if self.useTabs==True:
          self.prefix="\t\t\t"
        else:
          self.prefix=""
      self.prefix=bcolors.ENDC
      print self.prefix

  # Display a particular coordinate
  #
  def displayCoordinate(self, coords, nr):
    if self.level < 6:
      if self.useTabs==True:
        print "\t\t" + "          |"
        print "\t\t" + "          COORDINATE_" + str(nr)
      else:
        print "                          |"
        print "                          COORDINATE_" + str(nr)
      return
    print self.prefix + "--------------------------------"
    print self.prefix + "COORDINATE_"+ str(nr)
    if coords.coordinate(nr).exists()==False:
      print bcolors.FAIL + "COORDINATE_" + str(nr) + " does not exist."
      self.prefix=bcolors.ENDC
      return
    else:
      coord=coords.coordinate(nr)         # pick coordinate
      # Common coordinate attributes
      print self.prefix + coord.groupType().name() + "\t\t=", coord.groupType().value
      print self.prefix + coord.coordinateType().name() + "\t\t=", coord.coordinateType().value
      print self.prefix + coord.storageType().name() + "\t\t=", coord.storageType().value
      print self.prefix + coord.nofAxes().name() + "\t\t=", coord.nofAxes().value
      print self.prefix + coord.axisNames().name() + "\t\t=", coord.axisNames().value
      print self.prefix + coord.axisUnits().name() + "\t\t=", coord.axisUnits().value

      # Now identify coordinate
      if coord.groupType().value == "TimeCoord":
        timeCoord=dal.TimeCoordinate(coords, coord.name())   # create a TimeCoord from the generic coord
        print self.prefix + timeCoord.referenceValue().name() + "\t\t=", timeCoord.referenceValue().value
        print self.prefix + timeCoord.referencePixel().name() + "\t\t=", timeCoord.referencePixel().value
        print self.prefix + timeCoord.increment().name() + "\t\t=", timeCoord.increment().value     
        print self.prefix + timeCoord.pc().name() + "\t\t\t=", timeCoord.pc().value     
        print self.prefix + timeCoord.axisValuesPixel().name() + "\t=", timeCoord.axisValuesPixel().value     
        print self.prefix + timeCoord.axisValuesWorld().name() + "\t=", timeCoord.axisValuesWorld().value     
      elif coord.groupType().value == "SpectralCoord":
        spectralCoord=dal.SpectralCoordinate(coords, coord.name())   # create a SpectralCoord from the generic coord
        print self.prefix + spectralCoord.referenceValue().name() + "\t\t=", spectralCoord.referenceValue().value
        print self.prefix + spectralCoord.referencePixel().name() + "\t\t=", spectralCoord.referencePixel().value
        print self.prefix + spectralCoord.increment().name() + "\t\t=", spectralCoord.increment().value     
        print self.prefix + spectralCoord.pc().name() + "\t\t\t=", spectralCoord.pc().value     
        print self.prefix + spectralCoord.axisValuesPixel().name() + "\t=", spectralCoord.axisValuesPixel().value     
        print self.prefix + spectralCoord.axisValuesWorld().name() + "\t=", spectralCoord.axisValuesWorld().value
      else:
        print coord.name() + " is of type " + coord.groupType()
        self.prefix=bcolors.ENDC
        return
      self.prefix=bcolors.ENDC
          
  # Time coordinate information
  #
  def displayTimeCoordinate(self, coord):
    print "displayTimeCoordinate()"     # DEBUG

  # Spectral coordinate information
  #
  def displaySpectralCoordinate(self, coord):
    print self.prefix + "Reference frame    = ", coord.referenceFrame().value
    print self.prefix + "Rest frequency     = ", coord.restFrequency().value
    print self.prefix + "Rest frequency unit = ", coord.restFrequencyUnit().value
    print self.prefix + "Rest wavelength    = ", coord.restWavelength().value
    print self.prefix + "Rest wavelength unit = ", coord.restWavelengthUnit().value

  def handleArg(self, arg):     # experimental to disect python arg
    print "handleArg()"
    if "[" in arg and "]" in arg:    
      handleList(arg)
    else:
      return(int(arg))  # treat as integer

  # Handle command line options supplied as list
  #
  def handleList(self, list):  # experimental to disect python list
    print "handleList()"
    
    # strip off [ and ]
    # separate on ,
    # Detect ~ for ranges

  # Handle command line options supplied as a range
  #
  def handleRange(self, range):
    print "handleList()"
  

#############################################
#
# Helper class for color terminal printing
#
#############################################

        
class bcolors:
    BACKGROUND="dark"       # background scheme of terminal (dark or bright)
    HEADER = '\033[95m'
    SAP = '\033[94m'        # blue
#    BEAM = '\033[92m'       # green
    BEAM = '\033[32m'       # dark green
    #DATASET = '\033[93m'   # yellow
    DATASET= '\033[91m'     # red
    COORD = '\033[0m'       # fat white
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def switch(self):
      if self.BACKGROUND=="dark": # switch to bright background scheme
        BACKGROUND="bright"     # background scheme of terminal (dark or bright)
        HEADER = '\033[95m'
        SAP = '\033[94m'        # blue
#        BEAM = '\033[92m'       # green
        BEAM = '\033[32m'       # green
        DATASET = '\033[93m'    # yellow
        COORD = '\033[0m'       # fat white
        FAIL = '\033[91m'
        ENDC = '\033[0m'
      else:                     # switch to dark background scheme
        BACKGROUND="dark"
        HEADER = '\033[95m'
        SAP = '\033[94m'        # blue
#        BEAM = '\033[92m'       # green
        BEAM = '\033[32m'       # green
        DATASET = '\033[93m'    # yellow
        COORD = '\033[0m'       # fat white
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.SAP = ''
        self.BEAM = ''
        self.DATASET = ''
        self.FAIL = ''
        self.ENDC = ''      

