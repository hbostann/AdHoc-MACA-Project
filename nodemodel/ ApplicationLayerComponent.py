from enum import Enum
import logging

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes, GenericMessageHeader, GenericMessage


# define your own message types
class AcknowledgingAppLayerMessageTypes(Enum):
  DAT = "DATA"
  ACK = "ACK"


# define your own message header structure
class AcknowledgingAppLayerMessageHeader(GenericMessageHeader):
  pass


class AcknowledgingAppLayerEventTypes(Enum):
  SENDDAT = "send-data"
  SENDACK = "send-ack"


class AcknowledgingAppLayer(GenericModel):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.eventhandlers[AcknowledgingAppLayerEventTypes.SENDDAT] = self.SendData
    self.eventhandlers[AcknowledgingAppLayerEventTypes.SENDACK] = self.SendAck
    self.received_count = 0
    self.identifier = f"{self.componentname}[{self.componentinstancenumber}]"
    self.id = self.componentinstancenumber

  def on_message_from_top(self, eventobj: Event):
    logging.warn(
        f"{self.identifier} received message from top?! Sending down...")
    self.send_down(eventobj)

  def on_message_from_bottom(self, eventobj: Event):
    from_id = eventobj.eventcontent.header.messagefrom
    dest_id = eventobj.eventcontent.header.messageto
    mesg_type = eventobj.eventcontent.header.messagetype
    content = eventobj.eventcontent.payload

    if dest_id != self.id:
      # Maybe send down as broadcast?
      return
    logging.info(
        f"{self.identifier} received [F:{from_id}][T:{dest_id}][{mesg_type}]['{content}']"
    )
    if mesg_type == AcknowledgingAppLayerMessageTypes.DAT:
      # Craft ack packet
      ack_header = AcknowledgingAppLayerMessageHeader(
          AcknowledgingAppLayerMessageTypes.ACK, self.id, from_id)
      ack_msg = GenericMessage(ack_header, f"{self.id} acknowledges!")
      self.send_self(
          Event(self, AcknowledgingAppLayerEventTypes.SENDACK, ack_msg))
      return

    if mesg_type == AcknowledgingAppLayerMessageTypes.ACK:
      logging.info(f"{self.id} received ACK!")
      return

    logging.error(f"{self.id} received unknown message. Ignoring")

  def SendData(self, eventobj: Event):
    from_id = eventobj.eventcontent.header.messagefrom
    dest_id = eventobj.eventcontent.header.messageto
    mesg_type = eventobj.eventcontent.header.messagetype
    content = eventobj.eventcontent.payload
    logging.info(
        f"{self.identifier} sending DATA [F:{from_id}][T:{dest_id}][{mesg_type}]['{content}']"
    )

    dat_header = AcknowledgingAppLayerMessageHeader(
        AcknowledgingAppLayerMessageTypes.DAT, from_id, dest_id)
    dat_msg = GenericMessage(dat_header, content)
    self.send_down(Event(self, EventTypes.MFRT, dat_msg))

  def SendAck(self, eventobj: Event):
    from_id = eventobj.eventcontent.header.messagefrom
    dest_id = eventobj.eventcontent.header.messageto
    mesg_type = eventobj.eventcontent.header.messagetype
    content = eventobj.eventcontent.payload
    logging.info(
        f"{self.identifier} sending ACK [F:{from_id}][T:{dest_id}][{mesg_type}]['{content}']"
    )
    self.send_down(self, eventobj)
