from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes


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

  def on_init(self, eventobj: Event):
    pass

  def on_message_from_top(self, eventobj: Event):
    self.send_down(Event(self, EventTypes.MFRT, eventobj))

  def on_message_from_bottom(self, eventobj: Event):
    self.send_up(Event(self, EventTypes.MFRB, eventobj))
