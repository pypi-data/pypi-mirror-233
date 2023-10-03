import logging
from typing import List

from cltl.combot.infra.config import ConfigurationManager
from cltl.combot.infra.event import Event, EventBus
from cltl.combot.infra.resource import ResourceManager
from cltl.combot.infra.topic_worker import TopicWorker

from cltl.entity_linking.api import BasicLinker
from cltl_service.entity_linking.leolani import AgentLinker

logger = logging.getLogger(__name__)

CONTENT_TYPE_SEPARATOR = ';'


class DisambiguationService:
    @classmethod
    def from_config(cls, linkers: List[BasicLinker], event_bus: EventBus,
                    resource_manager: ResourceManager,
                    config_manager: ConfigurationManager):
        config = config_manager.get_config("cltl.entity_linking")

        return cls(config.get("topic_input"), config.get("topic_output"), config.get("topic_scenario"),
                   linkers, event_bus, resource_manager)

    def __init__(self, input_topic: str, output_topic: str, scenario_topic: str, linkers: List[BasicLinker],
                 event_bus: EventBus, resource_manager: ResourceManager):
        self._linkers = linkers
        self._agent_linker = AgentLinker()

        self._event_bus = event_bus
        self._resource_manager = resource_manager

        self._input_topic = input_topic
        self._output_topic = output_topic
        self._scenario_topic = scenario_topic

        self._topic_worker = None

    @property
    def app(self):
        return None

    def start(self, timeout=30):
        self._topic_worker = TopicWorker([self._input_topic, self._scenario_topic], self._event_bus,
                                         provides=[self._output_topic],
                                         resource_manager=self._resource_manager, processor=self._process,
                                         name=self.__class__.__name__)
        self._topic_worker.start().wait()

    def stop(self):
        if not self._topic_worker:
            pass

        self._topic_worker.stop()
        self._topic_worker.await_stop()
        self._topic_worker = None

    def _process(self, event: Event[List[dict]]):
        if event.metadata.topic == self._scenario_topic:
            self._process_scenario(event)
        if event.metadata.topic == self._input_topic:
            self._process_input(event)

    def _process_scenario(self, event: Event[List[dict]]):
        if event.payload.scenario.context.speaker and event.payload.scenario.context.speaker.uri:
            speaker = event.payload.scenario.context.speaker
            self._agent_linker.set_speaker(speaker.name, ['person'], speaker.uri)
            logger.debug("Set speaker to %s", speaker)

    def _process_input(self, event: Event[List[dict]]):
        try:
            logger.debug("Linking capsules for event %s: (%s)", event.id, event.payload)
            linked_capsule = [self._link_capsule(capsule) for capsule in event.payload]
            linked_capsule = [caps for caps in linked_capsule if caps is not None]

            if linked_capsule:
                logger.debug("Linked capsules for event %s: (%s)", event.id, linked_capsule)
                self._event_bus.publish(self._output_topic, Event.for_payload(linked_capsule))
        except:
            logger.exception("Error during linking (%s)", event.payload)

    def _link_capsule(self, capsule):
        self._agent_linker.link(capsule)

        for linker in self._linkers:
            capsule = linker.link(capsule)

        return capsule
