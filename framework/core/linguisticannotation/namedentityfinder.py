"""Defines a class for searching named entities associated with a specific token."""
from typing import Iterable
from spacy.tokens.span import Span


class NamedEntityFinder:
    """Finds the named entities associated with a token."""

    def __init__(self, named_entities: Iterable[Span]):
        """Initialize a new instance of the class.

        Parameters
        ----------
        named_entities: iterable of spacy Span, required
            The collection of named entities to search.
        """
        self.__named_entities = {
            tok.i: ne
            for ne in named_entities for tok in ne
        }

    def search_named_entity(self, token: any) -> Span | None:
        """Search the named entity for the provided token.

        Parameters
        ----------
        token: CoNLL-U token, required
            The token to check if it's part of a named entity.

        Returns
        -------
        named_entity: Span
            The named entity of the provided token if found; otherwise None.
        """
        if token.Index in self.__named_entities:
            return self.__named_entities[token.Index]
        return None
