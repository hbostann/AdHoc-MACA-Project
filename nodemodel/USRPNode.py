from nodemodel.ApplicationLayerComponent import AcknowledgingAppLayer
from .GenericNode import GenericNode

from adhoccomputing.Generics import ConnectorTypes
from adhoccomputing.Networking.PhysicalLayer.UsrpB210OfdmFlexFramePhy import UsrpB210OfdmFlexFramePhy
from adhoccomputing.Networking.MacProtocol.CSMA import MacCsmaPPersistent, MacCsmaPPersistentConfigurationParameters


class USRPNode(GenericNode):

  def __init__(self, componentname, componentinstancenumber, *args, **kwargs):
    super.__init__(componentname, componentinstancenumber, *args, **kwargs)
    macconfig = MacCsmaPPersistentConfigurationParameters(0.5)

    self.phy = UsrpB210OfdmFlexFramePhy("UsrpB210OfdmFlexFramePhy",
                                        componentinstancenumber)
    self.mac = MacCsmaPPersistent("MacCsmaPPersistent",
                                  componentinstancenumber,
                                  configurationparameters=macconfig,
                                  uhd=self.phy.ahcuhd)
    self.components.append(self.mac)
    self.components.append(self.phy)

    self.appl.connect_me_to_component(ConnectorTypes.DOWN, self.mac)

    self.mac.connect_me_to_component(ConnectorTypes.UP, self.appl)
    self.mac.connect_me_to_component(ConnectorTypes.DOWN, self.phy)

    self.phy.connect_me_to_component(ConnectorTypes.UP, self.mac)
    self.phy.connect_me_to_component(ConnectorTypes.DOWN, self)

    self.connect_me_to_component(ConnectorTypes.UP, self.phy)