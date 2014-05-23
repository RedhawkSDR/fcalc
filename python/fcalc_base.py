#!/usr/bin/env python
#
# This file is protected by Copyright. Please refer to the COPYRIGHT file distributed with this 
# source distribution.
# 
# This file is part of REDHAWK Basic Components fcalc.
# 
# REDHAWK Basic Components fcalc is free software: you can redistribute it and/or modify it under the terms of 
# the GNU Lesser General Public License as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later version.
# 
# REDHAWK Basic Components fcalc is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License along with this 
# program.  If not, see http://www.gnu.org/licenses/.
#
#
# AUTO-GENERATED CODE.  DO NOT MODIFY!
#
# Source: fcalc.spd.xml
from ossie.cf import CF
from ossie.cf import CF__POA
from ossie.utils import uuid

from ossie.resource import Resource
from ossie.threadedcomponent import *
from ossie.properties import simple_property
from ossie.properties import simpleseq_property

import Queue, copy, time, threading
from ossie.resource import usesport, providesport
import bulkio

class fcalc_base(CF__POA.Resource, Resource, ThreadedComponent):
        # These values can be altered in the __init__ of your derived class

        PAUSE = 0.0125 # The amount of time to sleep if process return NOOP
        TIMEOUT = 5.0 # The amount of time to wait for the process thread to die when stop() is called
        DEFAULT_QUEUE_SIZE = 100 # The number of BulkIO packets that can be in the queue before pushPacket will block

        def __init__(self, identifier, execparams):
            loggerName = (execparams['NAME_BINDING'].replace('/', '.')).rsplit("_", 1)[0]
            Resource.__init__(self, identifier, execparams, loggerName=loggerName)
            ThreadedComponent.__init__(self)

            # self.auto_start is deprecated and is only kept for API compatibility
            # with 1.7.X and 1.8.0 components.  This variable may be removed
            # in future releases
            self.auto_start = False
            # Instantiate the default implementations for all ports on this component
            self.port_a = bulkio.InDoublePort("a", maxsize=self.DEFAULT_QUEUE_SIZE)
            self.port_b = bulkio.InDoublePort("b", maxsize=self.DEFAULT_QUEUE_SIZE)
            self.port_out = bulkio.OutDoublePort("out")

        def start(self):
            Resource.start(self)
            ThreadedComponent.startThread(self, pause=self.PAUSE)

        def stop(self):
            if not ThreadedComponent.stopThread(self, self.TIMEOUT):
                raise CF.Resource.StopError(CF.CF_NOTSET, "Processing thread did not die")
            Resource.stop(self)

        def releaseObject(self):
            try:
                self.stop()
            except Exception:
                self._log.exception("Error stopping")
            Resource.releaseObject(self)

        ######################################################################
        # PORTS
        # 
        # DO NOT ADD NEW PORTS HERE.  You can add ports in your derived class, in the SCD xml file, 
        # or via the IDE.

        port_a = providesport(name="a",
                              repid="IDL:BULKIO/dataDouble:1.0",
                              type_="data")

        port_b = providesport(name="b",
                              repid="IDL:BULKIO/dataDouble:1.0",
                              type_="data")

        port_out = usesport(name="out",
                            repid="IDL:BULKIO/dataDouble:1.0",
                            type_="control")

        ######################################################################
        # PROPERTIES
        # 
        # DO NOT ADD NEW PROPERTIES HERE.  You can add properties in your derived class, in the PRF xml file
        # or by using the IDE.
        equation = simple_property(id_="equation",
                                   type_="string",
                                   mode="readwrite",
                                   action="external",
                                   kinds=("configure",),
                                   description="""A string representing an equation you want to implement in this component.  "a" represents the data on input a and "b" represents the data on b.  Calculation is performed on a sample by sample basis.
        
                                   An example equation would be "math.sin(a+b)+random.random()"
        
                                   Any operation which is supported in python is supported here.  Furthermore, use the import property to import more modules (including perhpase custom modules with custom functions) """)
        
        useAsri = simple_property(id_="useAsri",
                                  type_="boolean",
                                  defvalue=True,
                                  mode="readwrite",
                                  action="external",
                                  kinds=("execparam",),
                                  description="""Use input's A sri as the output sri. False = B""")
        
        import_ = simpleseq_property(id_="import",
                                     type_="string",
                                     defvalue=[
                                                      "math",
                                                      "random",
                                                      ],
                                     mode="readwrite",
                                     action="external",
                                     kinds=("configure",),
                                     description="""python modules (including perhapse custom modules) you want to import to use in your equation""")
        

