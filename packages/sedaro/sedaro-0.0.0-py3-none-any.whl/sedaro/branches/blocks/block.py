import copy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict

from pydash import is_empty

from ...exceptions import NonexistantBlockError
from ...settings import (BLOCKS, CRUD, DATA_SIDE, ID, MANY_SIDE, ONE_SIDE,
                         RELATIONSHIPS, TYPE)

if TYPE_CHECKING:
    from ...sedaro_api_client import SedaroApiClient
    from ..branch import Branch
    from .block_type import BlockType


@dataclass
class Block:
    id: str
    _block_type: 'BlockType'
    '''Class for interacting with all Blocks of this class type'''

    def __str__(self) -> str:
        return f'{self.data[TYPE]}(id={self.id})'

    def __repr__(self):
        attrs = ''
        for k, v in self.data.items():
            if type(v) is str:
                v = f"'{v}'"
            attrs += f'\n   {k}={v}'
        return f'\n{self.data[TYPE]}({attrs}\n)\n'

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        # allows a Block instance to be a key in a dictionary
        return hash(self.__class__.__name__ + self.id)

    def __getattr__(self, key: str) -> any:
        """Allows for dotting into the `Block` instance to access keys on the referenced Sedaro Block. Additionally,
        makes it so dotting into relationship fields returns `Block`s corresponding to the related Sedaro Blocks.

        Args:
            key (str): attribute being keyed into

        Raises:
            AttributeError: if the attribute doesn't exist on the refrenced Sedaro Block

        Returns:
            any: the value of the corresponding attribute on the referenced Sedaro Block
        """
        if key not in self.data:
            raise make_attr_error(key, self.data[TYPE])
        val = self.data[key]

        if not self.is_rel_field(key):
            return val

        side_type = self.get_rel_field_type(key)

        if side_type == MANY_SIDE:
            return [self._branch.block(id) for id in val]

        if side_type == DATA_SIDE:
            return {self._branch.block(id): data for id, data in val.items()}

        if side_type == ONE_SIDE:
            return self._branch.block(val)

        raise NotImplementedError(
            f'Unsupported relationship type on "{self.data[TYPE]}", attribute: "{key}".'
        )

    @property
    def type(self) -> str:
        '''Name of the class of the Sedaro Block this `Block` instance is set up to interact with'''
        return self._block_type.type

    @property
    def data(self) -> Dict:
        '''The properties of the corresponding Sedaro Block as a dictionary'''
        self.enforce_still_exists()
        return self._branch.data[BLOCKS][self.id]

    @property
    def _branch(self) -> 'Branch':
        '''The `Branch` this `Block` instance is connected to'''
        return self._block_type._branch

    def check_still_exists(self) -> bool:
        """Checks whether the Sedaro Block this `Block` instance references still exists.

        Returns:
            bool: indication of whether or not the referenced Sedaro Block still exists
        """
        return self.id in self._branch.data[BLOCKS]

    def enforce_still_exists(self) -> None:
        """Raises and error if the Sedaro Block this `Block` instance references no longer exists.

        Raises:
            NonexistantBlockError: indication that the Block no longer exists.
        """
        if not self.check_still_exists():
            raise NonexistantBlockError(
                f'The referenced "{self.type}" (id: {self.id}) no longer exists.'
            )

    def clone(self) -> 'Block':
        """Creates a copy of the Sedaro Block corresponding to the `Block` instance this method is called on.

        Note:
        - if there is a name attribute, the name of the created `Block`s will have `'(clone)'` appended to it.
        - this will not work if the resulting clone violates unique constraints.

        Returns:
            Block: `Block` associated with the created Sedaro `Block`
        """
        new_block = copy.deepcopy(self.data)
        del new_block[ID]

        if 'name' in new_block:
            new_block['name'] = f'{new_block["name"]} (clone)'

        res = self._branch.crud(
            blocks=[new_block]
        )

        return self._branch.block(res[CRUD][BLOCKS][0])

    def update(self, **fields) -> 'Block':
        """Update attributes of the corresponding Sedaro Block

        Args:
            **fields (Dict): desired attributes to update on the Sedaro Block

        Raises:
            SedaroApiException: if there is an error in the response

        Returns:
            Block: updated `Block` (Note: the previous `Block` reference is also updated)
        """
        if is_empty(fields):
            raise ValueError(f'Must provide fields to update on the {self.type}.')

        if ID in fields and fields[ID] != self.id:
            raise ValueError(f'Invalid value for "{ID}". Omit or ensure it is the same as this Block\'s {ID}.')

        # NOTE: `self.data` calls `self.enforce_still_exists()`, so don't need to call here
        self._branch.crud(blocks=[{**self.data, **fields}])
        return self

    def delete(self) -> str:
        """Deletes the associated Sedaro Block

        Raises:
            SedaroApiException: if there is an error in the response

        Returns:
            str: `id` of the deleted Sedaro Block
        """
        self.enforce_still_exists()
        self._branch.crud(delete=[self.id])
        return self.id

    def is_rel_field(self, field: str) -> bool:
        """Checks if the given `field` is a relationship field on the associated Sedaro Block.

        Args:
            field (str): field to check

        Raises:
            TypeError: if the value of `field` is not a string

        Returns:
            bool: indicates if the given `field` is a relationship field on the Sedaro Block or not.
        """
        return field in self._branch.data[RELATIONSHIPS][self.data[TYPE]]

    def get_rel_field_type(self, field: str) -> str:
        """Get the type of relationship of the field. Note: first call `is_rel_field` if you need to confirm `field` is
        a relationship field.

        Args:
            field (str): the field to get the relationship type for

        Raises:
            TypeError: if the value of `field` is not a string or not a relationship field on this type of Sedaro Block
            KeyError: if the value of `field` does not correspond to any field on the associated Sedaro Block

        Returns:
            str: a string indicating the type of relationship field
        """
        if not self.is_rel_field(field):
            raise TypeError(
                f'The given field "{field}" is not a relationship field on "{self.data[TYPE]}".')

        return self._branch.data[RELATIONSHIPS][self.data[TYPE]][field][TYPE]


# ------ helper function and vars for this file only ------
def make_attr_error(field: str, block_name: str) -> str:
    return AttributeError(f'There is no "{field}" attribute on "{block_name}"')
