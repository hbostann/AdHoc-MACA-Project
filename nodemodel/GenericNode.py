from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import (ConnectorTypes, Event, EventTypes,
                                     GenericMessage, GenericMessageHeader)

from .ApplicationLayerComponent import (AcknowledgingAppLayer,
                                        AcknowledgingAppLayerEventTypes,
                                        AcknowledgingAppLayerMessageTypes)


class GenericNode(GenericModel):

  def __init__(self,
               componentname,
               componentinstancenumber,
               context=None,
               configurationparameters=None,
               num_worker_threads=1,
               topology=None):
    super().__init__(componentname, componentinstancenumber, context,
                     configurationparameters, num_worker_threads, topology)
    # Setup layers and connect them
    # application
    # phy
    # mac
    self.application = AcknowledgingAppLayer("AckAppLayer",
                                             componentinstancenumber)
    self.components.append(self.application)
    self.application.connect_me_to_component(ConnectorTypes.DOWN, self)
    self.connect_me_to_component(ConnectorTypes.UP, self.application)

  def on_init(self, eventobj: Event):
    pass

  def on_message_from_top(self, eventobj: Event):
    self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

  def on_message_from_bottom(self, eventobj: Event):
    self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

  def SendMessage(self, dest_id, data):
    header = GenericMessageHeader(AcknowledgingAppLayerMessageTypes.DAT,
                                  self.componentinstancenumber, dest_id)
    message = GenericMessage(header, data)
    self.application.send_self(
        Event(self, AcknowledgingAppLayerEventTypes.SENDDAT, message))
