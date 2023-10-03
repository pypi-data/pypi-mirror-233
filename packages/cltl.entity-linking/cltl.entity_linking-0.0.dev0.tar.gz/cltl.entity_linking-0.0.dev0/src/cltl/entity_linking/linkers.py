"""
Upon encountering NE do:
1) select NE token text as name
2) Query brain to find URI's with name (entities_with_label.rq)
3) if multiple URI's found:
    4) Query brain to count number of denotedBy links for each URI
    5) Rank URI's by number of links
    6) Select highest ranking URI
    7) Add URI to Annotation
3) if one URI found:
    4) Add URI to Annotation
3) if no URI's found:
    4) Add URI to brain
    5) Add URI to Annotation
"""

import jellyfish
from cltl.brain.infrastructure.rdf_builder import RdfBuilder

from cltl.entity_linking.api import BasicLinker
from cltl.entity_linking.entity_querying import EntitySearch


class NamedEntityLinker(BasicLinker):
    """
    Used for disambiguation of Named Entities in text. Call when the part of speech tag of a label is 'NNP'
    Connection with GraphDB is needed to run the linker, since it queries the brain
    Input: capsule without url
    Output: capsule with url
    """

    def __init__(self, address, log_dir):

        super(NamedEntityLinker, self).__init__()
        self._rdf_builder = RdfBuilder()
        self._entity_search = EntitySearch(address, log_dir)

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
        if entity_position not in capsule or capsule[entity_position]['uri']:
            return capsule

        if 'person' in capsule[entity_position]['type']:
            uri = self._entity_search.search_entities_by_label(capsule[entity_position]['label'])
            if uri:
                capsule[entity_position]['uri'] = uri
            else:
                uri = self.fuzzy_label_match(capsule[entity_position]['label'])
            if uri:
                capsule[entity_position]['uri'] = uri
            else:
                # person_id = f"{capsule[entity_position]['label'].lower()}_{timestamp_now()}"
                person_id = f"{capsule[entity_position]['label'].lower()}"
                capsule[entity_position]['uri'] = str(self._rdf_builder.create_resource_uri('LW', person_id))
        elif capsule[entity_position]['label']:
            capsule[entity_position]['uri'] = str(
                self._rdf_builder.create_resource_uri('LW', capsule[entity_position]['label'].lower()))

        return capsule

    def link_predicates(self, capsule):
        if 'predicate' in capsule and not capsule['predicate']['uri']:
            capsule['predicate']['uri'] = str(
                self._rdf_builder.create_resource_uri('N2MU', capsule['predicate']['label'].lower()))

        return capsule

    def fuzzy_label_match(self, label, algorithm='popularity'):
        scored_matches = [(jellyfish.levenshtein_distance(label, entity['label']), entity['uri'])
                          for entity in self._entity_search.search_entities(algorithm)]
        scored_matches = list(filter(lambda match: match[0] < len(label) // 4, scored_matches))

        if not scored_matches:
            return None

        _, uri = scored_matches[0]

        return uri


class PronounLinker(BasicLinker):
    """
        Used for disambiguation of pronouns in text. Call when the part of speech tag of a label is 'PRP'
        Connection with GraphDB is needed to run the linker, since it queries the brain
        Input: capsule without url
        Output: capsule with url
        """

    def __init__(self, address, log_dir):

        super(PronounLinker, self).__init__()
        self._rdf_builder = RdfBuilder()
        self._entity_search = EntitySearch(address, log_dir)

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

        # Specific logic to link people
        if 'person' in capsule[entity_position]['type']:
            entity_label = capsule[entity_position]['label']
            uri = self._entity_search.search_entities_by_label(entity_label, algorithm='recency')
            if uri:
                capsule[entity_position]['uri'] = uri
            else:
                entity_list = self._entity_search.search_entities(algorithm='recency')
            if entity_list:
                uri = entity_list[0]['uri']
                capsule[entity_position]['uri'] = uri
            else:
                capsule[entity_position]['uri'] = str(
                    self._rdf_builder.create_resource_uri('LW', capsule[entity_position]['label'].lower()))

        # For anything else, create the uri from the label
        elif capsule[entity_position]['label']:
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
