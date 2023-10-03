from cltl.brain.infrastructure.rdf_builder import RdfBuilder

from cltl.entity_linking.api import BasicLinker


class LabelBasedLinker(BasicLinker):

    def __init__(self):
        """
        Create URI based on label Object

        Parameters
        ----------
        """

        super(BasicLinker, self).__init__()
        self._rdf_builder = RdfBuilder()

    def link(self, capsule):
        capsule = self.link_entities(capsule)
        capsule = self.link_predicates(capsule)

        return capsule

    def link_entities(self, capsule):
        capsule = self._link_entity(capsule, 'subject')
        capsule = self._link_entity(capsule, 'object')
        capsule = self._link_entity(capsule, 'author')
        capsule = self._link_entity(capsule, 'item')

        return capsule

    def _link_entity(self, capsule, entity_position):
        # Check that the RDF term we are trying to link is in the capsule
        if entity_position not in capsule:
            return capsule

        # Check that there is a  field to fill in
        if 'uri' not in capsule[entity_position].keys():
            capsule[entity_position]['uri'] = None

        # Check that the field is not already filled in
        if capsule[entity_position]['uri']:
            return capsule

        capsule[entity_position]['uri'] = str(
            self._rdf_builder.create_resource_uri('LW', capsule[entity_position]['label'].lower()))

        return capsule

    def link_predicates(self, capsule):
        # Check that there is a  field to fill in
        if 'uri' not in capsule['predicate'].keys():
            capsule['predicate']['uri'] = None

        # Make uri from label
        if 'predicate' in capsule and not capsule['predicate']['uri']:
            capsule['predicate']['uri'] = str(
                self._rdf_builder.create_resource_uri('N2MU', capsule['predicate']['label'].lower()))

        return capsule
