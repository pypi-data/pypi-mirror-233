import pymodd
from caseconverter import camelcase

from pymodd.script import Base, to_dict


class Function(Base):
    def __init__(self):
        self.function = None
        self.options = {}

    def to_dict(self):
        # check for direct values
        if type(self.function) is dict and self.function.get('direct'):
            return self.function.get('value')

        data = {
            'function': self.function
        }
        if self.options is not None:
            data.update(self.options)
        return data

    # calculation functions
    def __add__(self, other):
        if 'string' in [type_of_item(self).lower(), type_of_item(other).lower()]:
            return Concat(self, other)
        else:
            return Calculation(self, '+', other)

    def __sub__(self, other):
        return Calculation(self, '-', other)

    def __mul__(self, other):
        return Calculation(self, '*', other)

    def __truediv__(self, other):
        return Calculation(self, '/', other)

    def __mod__(self, other):
        return Calculation(self, '%', other)

    def __pow__(self, other):
        return Exponent(self, other)

    def __radd__(self, other):
        if 'string' in [type_of_item(self).lower(), type_of_item(other).lower()]:
            return Concat(other, self)
        else:
            return Calculation(other, '+', self)

    def __rsub__(self, other):
        return Calculation(other, '-', self)

    def __rmul__(self, other):
        return Calculation(other, '*', self)

    def __rtruediv__(self, other):
        return Calculation(other, '/', self)

    def __rmod__(self, other):
        return Calculation(other, '%', self)

    def __rpow__(self, other):
        return Exponent(other, self)


# only subclasses of Function requires these types
# (also prevents a circular import)
from .variable_types import (VariableType, AttributeTypeBase, EntityVariableBase, ItemTypeBase, PlayerTypeBase,
                             PlayerVariableBase, ProjectileTypeBase, StateBase, UnitTypeBase, VariableBase)


# ---------------------------------------------------------------------------- #
#                                     Other                                    #
# ---------------------------------------------------------------------------- #


def type_of_item(item):
    primitive_to_type = {
        int: 'number',
        float: 'number',
        complex: 'number',
        bool: 'boolean',
        str: 'string',
    }

    if isinstance(item, Undefined):
        return None
    if (primitive := primitive_to_type.get(type(item))):
        return primitive
    if isinstance(item, VariableBase):
        return item.data_type.value
    if isinstance(item, VariableType):
        base_classes = item.__class__.mro()
        for i, base_class in enumerate(base_classes):
            if base_class.__name__ == 'VariableType':
                return camelcase(base_classes[i-1].__name__)
    if isinstance(item, Function):
        base_classes = item.__class__.mro()
        for i, base_class in enumerate(base_classes):
            if base_class.__name__ == 'Function':
                return camelcase(base_classes[i-1].__name__)
    return None


class Undefined(Function):
    def __init__(self):
        self.function = 'undefinedValue'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Entitys                                   #
# ---------------------------------------------------------------------------- #


class Entity(Function):
    pass


class SelectedEntity(Entity):
    def __init__(self):
        self.function = 'getSelectedEntity'
        self.options = {}


class ThisEntity(Entity):
    def __init__(self):
        self.function = 'thisEntity'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Player                                    #
# ---------------------------------------------------------------------------- #


class Player(Entity):
    pass


class LastPlayerSelectingDialogueOption(Player):
    def __init__(self):
        self.function = 'getLastPlayerSelectingDialogueOption'
        self.options = {}


class LastTriggeringPlayer(Player):
    def __init__(self):
        self.function = 'getTriggeringPlayer'
        self.options = {}


class OwnerOfEntity(Player):
    def __init__(self, entity):
        self.function = 'getOwner'
        self.options = {
            'entity': to_dict(entity),
        }


class SelectedPlayer(Player):
    def __init__(self):
        self.function = 'selectedPlayer'
        self.options = {}


class PlayerFromId(Player):
    def __init__(self, string):
        self.function = 'getPlayerFromId'
        self.options = {
            'string': to_dict(string),
        }


# ---------------------------------------------------------------------------- #
#                                     Units                                    #
# ---------------------------------------------------------------------------- #


class Unit(Entity):
    pass


class LastPurchasedUnit(Unit):
    def __init__(self):
        self.function = 'getLastPurchasedUnit'
        self.options = {}


class LastOverlappingUnit(Unit):
    def __init__(self):
        self.function = 'getLastOverlappingUnit'
        self.options = {}


class LastOverlappedUnit(Unit):
    def __init__(self):
        self.function = 'getLastOverlappedUnit'
        self.options = {}


class LastTouchingUnit(Unit):
    def __init__(self):
        self.function = 'getLastTouchingUnit'
        self.options = {}


class SourceUnitOfProjectile(Unit):
    def __init__(self, entity):
        self.function = 'getSourceUnitOfProjectile'
        self.options = {
            'entity': to_dict(entity),
        }


class LastCastingUnit(Unit):
    def __init__(self):
        self.function = 'getLastCastingUnit'
        self.options = {}


class LastTouchedUnit(Unit):
    def __init__(self):
        self.function = 'getLastTouchedUnit'
        self.options = {}


class LastCreatedUnit(Unit):
    def __init__(self):
        self.function = 'getLastCreatedUnit'
        self.options = {}


class GetPlayerSelectedUnit(Unit):
    def __init__(self, player):
        self.function = 'getPlayerSelectedUnit'
        self.options = {
            'player': to_dict(player),
        }


class OwnerOfItem(Unit):
    def __init__(self, entity):
        self.function = 'getOwnerOfItem'
        self.options = {
            'entity': to_dict(entity),
        }


class LastTriggeringUnit(Unit):
    def __init__(self):
        self.function = 'getTriggeringUnit'
        self.options = {}


class SelectedUnit(Unit):
    def __init__(self):
        self.function = 'selectedUnit'
        self.options = {}


class LastAttackedUnit(Unit):
    def __init__(self):
        self.function = 'getLastAttackedUnit'
        self.options = {}


class LastAttackingUnit(Unit):
    def __init__(self):
        self.function = 'getLastAttackingUnit'
        self.options = {}


class OwnerUnitOfSensor(Unit):
    def __init__(self, sensor):
        self.function = 'ownerUnitOfSensor'
        self.options = {
            'sensor': to_dict(sensor),
        }


class UnitFromId(Unit):
    def __init__(self, string):
        self.function = 'getUnitFromId'
        self.options = {
            'string': to_dict(string),
        }


class TargetUnit(Unit):
    def __init__(self, unit):
        self.function = 'targetUnit'
        self.options = {
            'unit': to_dict(unit),
        }


# ---------------------------------------------------------------------------- #
#                                     Items                                    #
# ---------------------------------------------------------------------------- #


class Item(Entity):
    pass


class ItemInFrontOfUnit(Item):
    def __init__(self, entity):
        self.function = 'getItemInFrontOfUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class ItemAtSlot(Item):
    def __init__(self, slot, unit):
        self.function = 'getItemAtSlot'
        self.options = {
            'slot': to_dict(slot),
            'unit': to_dict(unit),
        }


class SelectedItem(Item):
    def __init__(self):
        self.function = 'selectedItem'
        self.options = {}


class LastTriggeringItem(Item):
    def __init__(self):
        self.function = 'getTriggeringItem'
        self.options = {}


class ItemCurrentlyHeldByUnit(Item):
    def __init__(self, entity):
        self.function = 'getItemCurrentlyHeldByUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class LastUsedItem(Item):
    def __init__(self):
        self.function = 'lastUsedItem'
        self.options = {}


class SourceItemOfProjectile(Item):
    def __init__(self, entity):
        self.function = 'getSourceItemOfProjectile'
        self.options = {
            'entity': to_dict(entity),
        }


class LastCreatedItem(Item):
    def __init__(self):
        self.function = 'getLastCreatedItem'
        self.options = {}


class LastOverlappingItem(Item):
    def __init__(self):
        self.function = 'getLastOverlappingItem'
        self.options = {}


class ItemInInventorySlot(Item):
    def __init__(self, slot, entity):
        self.function = 'getItemInInventorySlot'
        self.options = {
            'slot': to_dict(slot),
            'entity': to_dict(entity),
        }


class LastTouchedItem(Item):
    def __init__(self):
        self.function = 'getLastTouchedItem'
        self.options = {}


class LastAttackingItem(Item):
    def __init__(self):
        self.function = 'getLastAttackingItem'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                  Projectiles                                 #
# ---------------------------------------------------------------------------- #


class Projectile(Entity):
    pass


class SelectedProjectile(Projectile):
    def __init__(self):
        self.function = 'selectedProjectile'
        self.options = {}


class LastCreatedProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastCreatedProjectile'
        self.options = {}


class LastTriggeringProjectile(Projectile):
    def __init__(self):
        self.function = 'getTriggeringProjectile'
        self.options = {}


class LastTouchedProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastTouchedProjectile'
        self.options = {}


class LastOverlappingProjectile(Projectile):
    def __init__(self):
        self.function = 'getLastOverlappingProjectile'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Debris                                    #
# ---------------------------------------------------------------------------- #


class Debris(Entity):
    pass


class SelectedDebris(Debris):
    def __init__(self):
        self.function = 'selectedDebris'
        self.options = {}


class LastTriggeringDebris(Debris):
    def __init__(self):
        self.function = 'getTriggeringDebris'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                   Positions                                  #
# ---------------------------------------------------------------------------- #


class Position(Function):
    pass


class XyCoordinate(Position):
    def __init__(self, x, y):
        self.function = 'xyCoordinate'
        self.options = {
            'x': to_dict(x),
            'y': to_dict(y),
        }


class PositionOfMouseCursorOfPlayer(Position):
    def __init__(self, player):
        self.function = 'getMouseCursorPosition'
        self.options = {
            'player': to_dict(player),
        }


class CenterOfRegion(Position):
    def __init__(self, region):
        self.function = 'centerOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class EntityLastRaycastCollisionPosition(Position):
    def __init__(self, entity):
        self.function = 'entityLastRaycastCollisionPosition'
        self.options = {
            'entity': to_dict(entity),
        }


class PositionOfEntity(Position):
    def __init__(self, entity):
        self.function = 'getEntityPosition'
        self.options = {
            'entity': to_dict(entity),
        }


class GetPositionInFrontOfPosition(Position):
    def __init__(self, position, distance, angle):
        self.function = 'getPositionInFrontOfPosition'
        self.options = {
            'position': to_dict(position),
            'distance': to_dict(distance),
            'angle': to_dict(angle),
        }


class RandomPositionInRegion(Position):
    def __init__(self, region):
        self.function = 'getRandomPositionInRegion'
        self.options = {
            'region': to_dict(region),
        }


# ---------------------------------------------------------------------------- #
#                                  Attributes                                  #
# ---------------------------------------------------------------------------- #


class Attribute(Function):
    pass


class LastTriggeringAttribute(Attribute):
    def __init__(self):
        self.function = 'getTriggeringAttribute'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    Sensor                                    #
# ---------------------------------------------------------------------------- #


class Sensor(Function):
    pass


class SensorOfUnit(Sensor):
    def __init__(self, unit):
        self.function = 'getSensorOfUnit'
        self.options = {
            'unit': to_dict(unit),
        }


class LastTriggeringSensor(Sensor):
    def __init__(self):
        self.function = 'getTriggeringSensor'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                    States                                    #
# ---------------------------------------------------------------------------- #


class CurrentStateOfEntity(StateBase):
    def __init__(self, entity):
        self.function = 'getEntityState'
        self.options = {
            'entity': to_dict(entity),
        }


# ---------------------------------------------------------------------------- #
#                                    Numbers                                   #
# ---------------------------------------------------------------------------- #


class Number(Function):
    def __init__(self, number):
        self.function = {
            'direct': True,
            'value': number,
        }


class RandomNumberBetween(Number):
    def __init__(self, min, max):
        self.function = 'getRandomNumberBetween'
        self.options = {
            'min': to_dict(min),
            'max': to_dict(max),
        }


class UnitsFacingAngle(Number):
    def __init__(self, unit):
        self.function = 'unitsFacingAngle'
        self.options = {
            'unit': to_dict(unit),
        }


class HeightOfMap(Number):
    def __init__(self):
        self.function = 'getMapHeight'
        self.options = {}


class ToFixed(Number):
    def __init__(self, value, precision):
        self.function = 'toFixed'
        self.options = {
            'value': to_dict(value),
            'precision': to_dict(precision),
        }


class ItemQuantity(Number):
    def __init__(self, item):
        self.function = 'getItemQuantity'
        self.options = {
            'item': to_dict(item),
        }


class Cos(Number):
    def __init__(self, angle):
        self.function = 'cos'
        self.options = {
            'angle': to_dict(angle),
        }


class HeightOfEntity(Number):
    def __init__(self, entity):
        self.function = 'entityHeight'
        self.options = {
            'entity': to_dict(entity),
        }


class AttributeMaxOfPlayer(Number):
    def __init__(self, attribute, entity):
        self.function = 'playerAttributeMax'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class ValueOfPlayerAttribute(Number):
    def __init__(self, attribute, entity):
        self.function = 'getPlayerAttribute'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class WidthOfMap(Number):
    def __init__(self):
        self.function = 'getMapWidth'
        self.options = {}


class WidthOfEntity(Number):
    def __init__(self, entity):
        self.function = 'entityWidth'
        self.options = {
            'entity': to_dict(entity),
        }


class NumberOfPlayers(Number):
    def __init__(self):
        self.function = 'getPlayerCount'
        self.options = {}


class Arctan(Number):
    def __init__(self, number):
        self.function = 'arctan'
        self.options = {
            'number': to_dict(number),
        }


class MathFloor(Number):
    def __init__(self, value):
        self.function = 'mathFloor'
        self.options = {
            'value': to_dict(value),
        }


class YCoordinateOfRegion(Number):
    def __init__(self, region):
        self.function = 'getYCoordinateOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class SquareRoot(Number):
    def __init__(self, number):
        self.function = 'squareRoot'
        self.options = {
            'number': to_dict(number),
        }


class UnitCount(Number):
    def __init__(self):
        self.function = 'getUnitCount'
        self.options = {}


class AngleBetweenPositions(Number):
    def __init__(self, position_a, position_b):
        self.function = 'angleBetweenPositions'
        self.options = {
            'positionA': to_dict(position_a),
            'positionB': to_dict(position_b),
        }


class WidthOfRegion(Number):
    def __init__(self, region):
        self.function = 'getWidthOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class AttributeMinOfEntity(Number):
    def __init__(self, attribute, entity):
        self.function = 'entityAttributeMin'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class StringToNumber(Number):
    def __init__(self, value):
        self.function = 'stringToNumber'
        self.options = {
            'value': to_dict(value),
        }


class QuantityOfUnitTypeInUnitTypeGroup(Number):
    def __init__(self, unit_type, unit_type_group):
        self.function = 'getQuantityOfUnitTypeInUnitTypeGroup'
        self.options = {
            'unitType': to_dict(unit_type),
            'unitTypeGroup': to_dict(unit_type_group),
        }


class YCoordinateOfPosition(Number):
    def __init__(self, position):
        self.function = 'getPositionY'
        self.options = {
            'position': to_dict(position),
        }


class DistanceBetweenPositions(Number):
    def __init__(self, position_a, position_b):
        self.function = 'distanceBetweenPositions'
        self.options = {
            'positionA': to_dict(position_a),
            'positionB': to_dict(position_b),
        }


class AttributeMaxOfEntity(Number):
    def __init__(self, attribute, entity):
        self.function = 'entityAttributeMax'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class AttributeMinOfPlayer(Number):
    def __init__(self, attribute, entity):
        self.function = 'playerAttributeMin'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class Sin(Number):
    def __init__(self, angle):
        self.function = 'sin'
        self.options = {
            'angle': to_dict(angle),
        }


class XCoordinateOfRegion(Number):
    def __init__(self, region):
        self.function = 'getXCoordinateOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class YVelocityOfEntity(Number):
    def __init__(self, entity):
        self.function = 'getEntityVelocityY'
        self.options = {
            'entity': to_dict(entity),
        }


class XCoordinateOfPosition(Number):
    def __init__(self, position):
        self.function = 'getPositionX'
        self.options = {
            'position': to_dict(position),
        }


class LastPlayedTimeOfPlayer(Number):
    def __init__(self, player):
        self.function = 'lastPlayedTimeOfPlayer'
        self.options = {
            'player': to_dict(player),
        }


class MaxBetweenTwoNumbers(Number):
    def __init__(self, num_a, num_b):
        self.function = 'getMax'
        self.options = {
            'num1': to_dict(num_a),
            'num2': to_dict(num_b),
        }


class RotationSpeedOfUnitType(Number):
    def __init__(self, unit_type):
        self.function = 'getRotateSpeed'
        self.options = {
            'unitType': to_dict(unit_type),
        }


class CurrentAmmoOfItem(Number):
    def __init__(self, item):
        self.function = 'getCurrentAmmoOfItem'
        self.options = {
            'item': to_dict(item),
        }


class HeightOfRegion(Number):
    def __init__(self, region):
        self.function = 'getHeightOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class MaxQuantityOfItem(Number):
    def __init__(self, item):
        self.function = 'getItemMaxQuantity'
        self.options = {
            'item': to_dict(item),
        }


class AbsoluteValueOfNumber(Number):
    def __init__(self, number):
        self.function = 'absoluteValueOfNumber'
        self.options = {
            'number': to_dict(number),
        }


class ValueOfEntityAttribute(Number):
    def __init__(self, attribute, entity):
        self.function = 'getEntityAttribute'
        self.options = {
            'attribute': to_dict(attribute),
            'entity': to_dict(entity),
        }


class CurrentUnixTimeStamp(Number):
    def __init__(self):
        self.function = 'currentTimeStamp'
        self.options = {}


class XVelocityOfEntity(Number):
    def __init__(self, entity):
        self.function = 'getEntityVelocityX'
        self.options = {
            'entity': to_dict(entity),
        }


class DefaultQuantityOfItemType(Number):
    def __init__(self, item_type):
        self.function = 'defaultQuantityOfItemType'
        self.options = {
            'itemType': to_dict(item_type),
        }


class QuantityOfItemTypeInItemTypeGroup(Number):
    def __init__(self, item_type, item_type_group):
        self.function = 'getQuantityOfItemTypeInItemTypeGroup'
        self.options = {
            'itemType': to_dict(item_type),
            'itemTypeGroup': to_dict(item_type_group),
        }


class NumberOfItems(Number):
    def __init__(self):
        self.function = 'getNumberOfItemsPresent'
        self.options = {}


class Min(Number):
    def __init__(self, num_a, num_b):
        self.function = 'getMin'
        self.options = {
            'num1': to_dict(num_a),
            'num2': to_dict(num_b),
        }


class MaxValueOfItemType(Number):
    def __init__(self, item_type):
        self.function = 'maxValueOfItemType'
        self.options = {
            'itemType': to_dict(item_type),
        }


class AngleBetweenMouseAndWindowCenter(Number):
    def __init__(self, player):
        self.function = 'angleBetweenMouseAndWindowCenter'
        self.options = {
            'player': to_dict(player),
        }


class Exponent(Number):
    def __init__(self, base, power):
        self.function = 'getExponent'
        self.options = {
            'base': to_dict(base),
            'power': to_dict(power),
        }


class NumberOfUnitsOfUnitType(Number):
    def __init__(self, unit_type):
        self.function = 'getNumberOfUnitsOfUnitType'
        self.options = {
            'unitType': to_dict(unit_type),
        }


class NumberOfPlayersOfPlayerType(Number):
    def __init__(self, player_type):
        self.function = 'getNumberOfPlayersOfPlayerType'
        self.options = {
            'playerType': to_dict(player_type),
        }


class LengthOfString(Number):
    def __init__(self, string):
        self.function = 'getLengthOfString'
        self.options = {
            'string': to_dict(string),
        }


class StringArrayLength(Number):
    def __init__(self, string):
        self.function = 'getStringArrayLength'
        self.options = {
            'string': to_dict(string),
        }


class SelectedInventorySlot(Number):
    def __init__(self, unit):
        self.function = 'selectedInventorySlot'
        self.options = {
            'unit': to_dict(unit),
        }


class LogBase10(Number):
    def __init__(self, value):
        self.function = 'log10'
        self.options = {
            'value': to_dict(value),
        }


class UnitSensorRadius(Number):
    def __init__(self, unit):
        self.function = 'unitSensorRadius'
        self.options = {
            'unit': to_dict(unit),
        }


class NumberToDegrees(Number):
    def __init__(self, number):
        self.function = 'toDegrees'
        self.options = {
            'number': to_dict(number),
        }


class NumberToRadians(Number):
    def __init__(self, number):
        self.function = 'toRadians'
        self.options = {
            'number': to_dict(number),
        }


class GetMapTileId(Number):
    def __init__(self, x, y, layer):
        self.function = 'getMapTileId'
        self.options = {
            'x': to_dict(x),
            'y': to_dict(y),
            'layer': to_dict(layer),
        }


class ElementCount(Number):
    def __init__(self, object):
        self.function = 'elementCount'
        self.options = {
            'object': to_dict(object),
        }


# ---------------------------------------------------------------------------- #
#                                    Strings                                   #
# ---------------------------------------------------------------------------- #


class String(Function):
    def __init__(self, string):
        self.function = {
            'direct': True,
            'value': string,
        }


class EntityTypeOfEntity(String):
    def __init__(self, entity):
        self.function = 'getEntityType'
        self.options = {
            'entity': to_dict(entity),
        }


class LastCustomInputOfPlayer(String):
    def __init__(self, player):
        self.function = 'playerCustomInput'
        self.options = {
            'player': to_dict(player),
        }


class NameOfPlayer(String):
    def __init__(self, entity):
        self.function = 'getPlayerName'
        self.options = {
            'entity': to_dict(entity),
        }


class NameOfUnitType(String):
    def __init__(self, unit_type):
        self.function = 'getUnitTypeName'
        self.options = {
            'unitType': to_dict(unit_type),
        }


class NameOfRegion(String):
    def __init__(self, region):
        self.function = 'nameOfRegion'
        self.options = {
            'region': to_dict(region),
        }


class NameOfItemType(String):
    def __init__(self, item_type):
        self.function = 'getItemTypeName'
        self.options = {
            'itemType': to_dict(item_type),
        }


class SubstringOf(String):
    def __init__(self, string, from_index, to_index):
        self.function = 'substringOf'
        self.options = {
            'string': to_dict(string),
            'fromIndex': to_dict(from_index),
            'toIndex': to_dict(to_index),
        }


class LastChatMessageSentByPlayer(String):
    def __init__(self, player):
        self.function = 'getLastChatMessageSentByPlayer'
        self.options = {
            'player': to_dict(player),
        }


class ToLowerCase(String):
    def __init__(self, string):
        self.function = 'toLowerCase'
        self.options = {
            'string': to_dict(string),
        }


class ReplaceValuesInString(String):
    def __init__(self, source_string, match_string, new_string):
        self.function = 'replaceValuesInString'
        self.options = {
            'matchString': to_dict(match_string),
            'sourceString': to_dict(source_string),
            'newString': to_dict(new_string),
        }


class UnixTimeToFormattedString(String):
    def __init__(self, seconds):
        '''formats to (hh::mm:ss)'''
        self.function = 'getTimeString'
        self.options = {
            'seconds': to_dict(seconds),
        }


class DescriptionOfItem(String):
    def __init__(self, item):
        self.function = 'getItemDescription'
        self.options = {
            'item': to_dict(item),
        }


class DataOfUnit(String):
    def __init__(self, unit):
        self.function = 'getUnitData'
        self.options = {
            'unit': to_dict(unit),
        }


class DataOfPlayer(String):
    def __init__(self, player):
        self.function = 'getPlayerData'
        self.options = {
            'player': to_dict(player),
        }


class IdOfUnit(String):
    def __init__(self, unit):
        self.function = 'getUnitId'
        self.options = {
            'unit': to_dict(unit),
        }


class IdOfPlayer(String):
    def __init__(self, player):
        self.function = 'getPlayerId'
        self.options = {
            'player': to_dict(player),
        }


class StringArrayElement(String):
    def __init__(self, number, string):
        self.function = 'getStringArrayElement'
        self.options = {
            'number': to_dict(number),
            'string': to_dict(string),
        }


class InsertStringArrayElement(String):
    def __init__(self, value, string):
        self.function = 'insertStringArrayElement'
        self.options = {
            'value': to_dict(value),
            'string': to_dict(string),
        }


class UpdateStringArrayElement(String):
    def __init__(self, number, string, value):
        self.function = 'updateStringArrayElement'
        self.options = {
            'number': to_dict(number),
            'string': to_dict(string),
            'value': to_dict(value),
        }


class RemoveStringArrayElement(String):
    def __init__(self, number, string):
        self.function = 'removeStringArrayElement'
        self.options = {
            'number': to_dict(number),
            'string': to_dict(string),
        }


class NameOfEntity(String):
    def __init__(self, entity):
        self.function = 'entityName'
        self.options = {
            'entity': to_dict(entity),
        }


class NumberToString(String):
    def __init__(self, value):
        self.function = 'numberToString'
        self.options = {
            'value': to_dict(value),
        }


class GetMapJson(String):
    def __init__(self, ):
        self.function = 'getMapJson'
        self.options = {
        }


class LastReceivedPostResponse(String):
    def __init__(self, ):
        self.function = 'lastReceivedPostResponse'
        self.options = {
        }


class LastUpdatedVariableName(String):
    def __init__(self, ):
        self.function = 'lastUpdatedVariableName'
        self.options = {
        }


class ObjectToString(String):
    def __init__(self, object):
        self.function = 'objectToString'
        self.options = {
            'object': to_dict(object),
        }

# ---------------------------------------------------------------------------- #
#                                   Booleans                                   #
# ---------------------------------------------------------------------------- #


class Boolean(Function):
    def __init__(self, boolean):
        self.function = {
            'direct': True,
            'value': boolean,
        }


class IsPlayerLoggedIn(Boolean):
    def __init__(self, player):
        self.function = 'isPlayerLoggedIn'
        self.options = {
            'player': to_dict(player),
        }


class PlayerIsCreator(Boolean):
    def __init__(self, player):
        self.function = 'playerIsCreator'
        self.options = {
            'player': to_dict(player),
        }


class AreBothPlayersFriendly(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreFriendly'
        self.options = {
            'playerA': to_dict(player_a),
            'playerB': to_dict(player_b),
        }


class IsPlayerControlledByHuman(Boolean):
    def __init__(self, player):
        self.function = 'playerIsControlledByHuman'
        self.options = {
            'player': to_dict(player),
        }


class AreBothPlayersHostile(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreHostile'
        self.options = {
            'playerA': to_dict(player_a),
            'playerB': to_dict(player_b),
        }


class RegionOverlapsWithRegion(Boolean):
    def __init__(self, region_a, region_b):
        self.function = 'regionOverlapsWithRegion'
        self.options = {
            'regionA': to_dict(region_a),
            'regionB': to_dict(region_b),
        }


class AreBothPlayersNeutral(Boolean):
    def __init__(self, player_a, player_b):
        self.function = 'playersAreNeutral'
        self.options = {
            'playerA': to_dict(player_a),
            'playerB': to_dict(player_b),
        }


class PlayerHasAdblockEnabled(Boolean):
    def __init__(self, player):
        self.function = 'playerHasAdblockEnabled'
        self.options = {
            'player': to_dict(player),
        }


class EntityExists(Boolean):
    def __init__(self, entity):
        self.function = 'entityExists'
        self.options = {
            'entity': to_dict(entity),
        }


class IsPositionInWall(Boolean):
    def __init__(self, positionx, positiony):
        self.function = 'isPositionInWall'
        self.options = {
            'position.x': to_dict(positionx),
            'position.y': to_dict(positiony),
        }


class StringContainsString(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'subString'
        self.options = {
            'sourceString': to_dict(source_string),
            'patternString': to_dict(pattern_string),
        }


class StringStartsWith(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'stringStartsWith'
        self.options = {
            'sourceString': to_dict(source_string),
            'patternString': to_dict(pattern_string),
        }


class StringEndsWith(Boolean):
    def __init__(self, source_string, pattern_string):
        self.function = 'stringEndsWith'
        self.options = {
            'sourceString': to_dict(source_string),
            'patternString': to_dict(pattern_string),
        }


class IsAIEnabled(Boolean):
    def __init__(self, unit):
        self.function = 'isAIEnabled'
        self.options = {
            'unit': to_dict(unit),
        }


class IsPlayerABot(Boolean):
    def __init__(self, player):
        self.function = 'isBotPlayer'
        self.options = {
            'player': to_dict(player),
        }


class IsPlayerAComputer(Boolean):
    def __init__(self, player_is_a_computer):
        self.function = 'isComputerPlayer'
        self.options = {
            'player is a computer': to_dict(player_is_a_computer),
        }


class RoleExistsForPlayer(Boolean):
    def __init__(self, name, player):
        self.function = 'roleExistsForPlayer'
        self.options = {
            'name': to_dict(name),
            'player': to_dict(player),
        }


class StringIsANumber(Boolean):
    def __init__(self, string_is_a_number):
        self.function = 'stringIsANumber'
        self.options = {
            'string_is_a_number': to_dict(string_is_a_number),
        }


# ---------------------------------------------------------------------------- #
#                                    Objects                                   #
# ---------------------------------------------------------------------------- #


class Object(Function):
    pass


class StringToObject(Object):
    def __init__(self, string):
        self.function = 'stringToObject'
        self.options = {
            'string': to_dict(string),
        }


class ElementFromObject(Object):
    def __init__(self, key, object):
        self.function = 'elementFromObject'
        self.options = {
            'key': to_dict(key),
            'object': to_dict(object),
        }


class EmptyObject(Object):
    def __init__(self, ):
        self.function = 'emptyObject'
        self.options = {
        }


# ---------------------------------------------------------------------------- #
#                                   Particles                                  #
# ---------------------------------------------------------------------------- #


class Particle(Function):
    pass


class ItemParticle(Particle):
    def __init__(self, particle_type, entity):
        self.function = 'getItemParticle'
        self.options = {
            'particleType': to_dict(particle_type),
            'entity': to_dict(entity),
        }


class SelectedParticle(Particle):
    def __init__(self):
        self.function = 'selectedParticle'
        self.options = {}


class UnitParticle(Particle):
    def __init__(self, particle_type, entity):
        self.function = 'getUnitParticle'
        self.options = {
            'particleType': to_dict(particle_type),
            'entity': to_dict(entity),
        }


# ---------------------------------------------------------------------------- #
#                                   Variables                                  #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                               Entity Variables                               #
# ---------------------------------------------------------------------------- #


class ValueOfEntityVariable(EntityVariableBase):
    def __init__(self, entity_variable_type, entity):
        self.function = 'getValueOfEntityVariable'
        self.data_type = entity_variable_type.data_type
        self.options = {
            'variable': to_dict(entity_variable_type),
            'entity': to_dict(entity)
        }


# ---------------------------------------------------------------------------- #
#                               Player Variables                               #
# ---------------------------------------------------------------------------- #


class ValueOfPlayerVariable(PlayerVariableBase):
    def __init__(self, player_variable_type, player):
        self.function = 'getValueOfPlayerVariable'
        self.data_type = player_variable_type.data_type
        self.options = {
            'variable': to_dict(player_variable_type),
            'player': to_dict(player)
        }


# ---------------------------------------------------------------------------- #
#                                    Regions                                   #
# ---------------------------------------------------------------------------- #


class Region(Function):
    pass


class LastTriggeringRegion(Region):
    def __init__(self):
        self.function = 'getTriggeringRegion'
        self.options = {}


class EntireMapRegion(Region):
    def __init__(self):
        self.function = 'getEntireMapRegion'
        self.options = {}


class SelectedRegion(Region):
    def __init__(self):
        self.function = 'selectedRegion'
        self.options = {}


class EntityBounds(Region):
    def __init__(self, entity):
        self.function = 'entityBounds'
        self.options = {
            'entity': to_dict(entity),
        }


class DynamicRegion(Region):
    def __init__(self, x, y, width, height):
        self.function = 'dynamicRegion'
        self.options = {
            'x': to_dict(x),
            'y': to_dict(y),
            'width': to_dict(width),
            'height': to_dict(height),
        }


# ---------------------------------------------------------------------------- #
#                                  Unit Types                                  #
# ---------------------------------------------------------------------------- #


class UnitTypeOfUnit(UnitTypeBase):
    def __init__(self, entity):
        self.function = 'getUnitTypeOfUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class IdOfLastPurchasedUnitTypet(UnitTypeBase):
    def __init__(self):
        self.function = 'lastPurchasedUnitTypetId'
        self.options = {}


class RandomUnitTypeFromUnitTypeGroup(UnitTypeBase):
    def __init__(self, unit_type_group):
        self.function = 'getRandomUnitTypeFromUnitTypeGroup'
        self.options = {
            'unitTypeGroup': to_dict(unit_type_group),
        }


class SelectedUnitType(UnitTypeBase):
    def __init__(self):
        self.function = 'selectedUnitType'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                  Item Types                                  #
# ---------------------------------------------------------------------------- #


class SelectedItemType(ItemTypeBase):
    def __init__(self):
        self.function = 'selectedItemType'
        self.options = {}


class ItemTypeOfItem(ItemTypeBase):
    def __init__(self, entity):
        self.function = 'getItemTypeOfItem'
        self.options = {
            'entity': to_dict(entity),
        }


class RandomItemTypeFromItemTypeGroup(ItemTypeBase):
    def __init__(self, item_type_group):
        self.function = 'getRandomItemTypeFromItemTypeGroup'
        self.options = {
            'itemTypeGroup': to_dict(item_type_group),
        }


# ---------------------------------------------------------------------------- #
#                               Projectile Types                               #
# ---------------------------------------------------------------------------- #


class ProjectileTypeOfProjectile(ProjectileTypeBase):
    def __init__(self, entity):
        self.function = 'getProjectileTypeOfProjectile'
        self.options = {
            'entity': to_dict(entity),
        }


# ---------------------------------------------------------------------------- #
#                                 Player Types                                 #
# ---------------------------------------------------------------------------- #


class PlayerTypeOfPlayer(PlayerTypeBase):
    def __init__(self, player):
        self.function = 'playerTypeOfPlayer'
        self.options = {
            'player': to_dict(player),
        }


# ---------------------------------------------------------------------------- #
#                                Attribute Types                               #
# ---------------------------------------------------------------------------- #


class AttributeTypeOfAttribute(AttributeTypeBase):
    def __init__(self, entity):
        self.function = 'getAttributeTypeOfAttribute'
        self.options = {
            'entity': to_dict(entity),
        }


# ---------------------------------------------------------------------------- #
#                                    Groups                                    #
# ---------------------------------------------------------------------------- #


class Group(Function):
    def _get_iterating_action(self):
        raise NotImplementedError('_get_iteration_object not implemented')

    def _get_iteration_object(self):
        raise NotImplementedError('_get_iteration_object not implemented')


# ---------------------------------------------------------------------------- #
#                                 Entity Groups                                #
# ---------------------------------------------------------------------------- #


class EntityGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_entities_in

    def _get_iteration_object(self):
        return SelectedEntity()


class AllEntitiesCollidingWithLastRaycast(EntityGroup):
    def __init__(self):
        self.function = 'entitiesCollidingWithLastRaycast'
        self.options = {}


class AllEntitiesInTheGame(EntityGroup):
    def __init__(self):
        self.function = 'allEntities'
        self.options = {}


class AllEntitiesInRegion(EntityGroup):
    def __init__(self, region):
        self.function = 'entitiesInRegion'
        self.options = {
            'region': to_dict(region),
        }


class AllEntitiesInFrontOfEntityInDynamicRegionAtDistance(EntityGroup):
    def __init__(self, entity, width: Number, height: Number, distance: Number):
        self.function = 'entitiesInRegionInFrontOfEntityAtDistance'
        self.options = {
            'width': to_dict(width),
            'height': to_dict(height),
            'entity': to_dict(entity),
            'distance': to_dict(distance),
        }


class AllEntitiesBetweenTwoPositions(EntityGroup):
    def __init__(self, position_a, position_b):
        self.function = 'entitiesBetweenTwoPositions'
        self.options = {
            'positionA': to_dict(position_a),
            'positionB': to_dict(position_b),
        }


# ---------------------------------------------------------------------------- #
#                                  Unit Groups                                 #
# ---------------------------------------------------------------------------- #


class UnitGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_units_in

    def _get_iteration_object(self):
        return SelectedUnit()


class AllUnitsOwnedByPlayer(UnitGroup):
    def __init__(self, player):
        self.function = 'allUnitsOwnedByPlayer'
        self.options = {
            'player': to_dict(player),
        }


class AllUnitsAttachedToUnit(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsAttachedToUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class AllUnitsInTheGame(UnitGroup):
    def __init__(self):
        self.function = 'allUnits'
        self.options = {}


class AllUnitsAttachedToItem(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsAttachedToItem'
        self.options = {
            'entity': to_dict(entity),
        }


class AllUnitsMountedOnUnit(UnitGroup):
    def __init__(self, entity):
        self.function = 'allUnitsMountedOnUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class AllUnitsInRegion(UnitGroup):
    def __init__(self, region):
        self.function = 'allUnitsInRegion'
        self.options = {
            'region': to_dict(region),
        }


# ---------------------------------------------------------------------------- #
#                               Projectile Groups                              #
# ---------------------------------------------------------------------------- #


class ProjectileGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_projectiles_in

    def _get_iteration_object(self):
        return SelectedProjectile()


class AllProjectilesAttachedToUnit(ProjectileGroup):
    def __init__(self, entity):
        self.function = 'allProjectilesAttachedToUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class AllProjectilesInTheGame(ProjectileGroup):
    def __init__(self):
        self.function = 'allProjectiles'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                  Item Groups                                 #
# ---------------------------------------------------------------------------- #


class ItemGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_items_in

    def _get_iteration_object(self):
        return SelectedItem()


class AllItemsDroppedOnGround(ItemGroup):
    def __init__(self):
        self.function = 'allItemsDroppedOnGround'
        self.options = {}


class AllItemsInTheGame(ItemGroup):
    def __init__(self):
        self.function = 'allItems'
        self.options = {}


class AllItemsAttachedToUnit(ItemGroup):
    def __init__(self, entity):
        self.function = 'allItemsAttachedToUnit'
        self.options = {
            'entity': to_dict(entity),
        }


class AllItemsOwnedByUnit(ItemGroup):
    def __init__(self, entity):
        self.function = 'allItemsOwnedByUnit'
        self.options = {
            'entity': to_dict(entity),
        }


# ---------------------------------------------------------------------------- #
#                                 Player Groups                                #
# ---------------------------------------------------------------------------- #


class PlayerGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_players_in

    def _get_iteration_object(self):
        return SelectedPlayer()


class AllHumanPlayersInTheGame(PlayerGroup):
    def __init__(self):
        self.function = 'humanPlayers'
        self.options = {}


class AllComputerPlayersInTheGame(PlayerGroup):
    def __init__(self):
        self.function = 'computerPlayers'
        self.options = {}


class AllPlayersInTheGame(PlayerGroup):
    def __init__(self):
        self.function = 'allPlayers'
        self.options = {}


class AllBotPlayersInTheGame(PlayerGroup):
    def __init__(self):
        self.function = 'botPlayers'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                               Item Type Groups                               #
# ---------------------------------------------------------------------------- #


class ItemTypeGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_item_types_in

    def _get_iteration_object(self):
        return SelectedItemType()


class AllItemTypesInTheGame(ItemTypeGroup):
    def __init__(self):
        self.function = 'allItemTypesInGame'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                               Unit Type Groups                               #
# ---------------------------------------------------------------------------- #


class UnitTypeGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_unit_types_in

    def _get_iteration_object(self):
        return SelectedUnitType()


class AllUnitTypesInTheGame(UnitTypeGroup):
    def __init__(self):
        self.function = 'allUnitTypesInGame'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                 Debris Groups                                #
# ---------------------------------------------------------------------------- #


class DebrisGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_debris_in

    def _get_iteration_object(self):
        return SelectedDebris()


class AllDebrisInTheGame(DebrisGroup):
    def __init__(self):
        self.function = 'allDebris'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                 Region Groups                                #
# ---------------------------------------------------------------------------- #


class RegionGroup(Group):
    def _get_iterating_action(self):
        return pymodd.actions.for_all_regions_in

    def _get_iteration_object(self):
        return SelectedRegion()


class AllRegionsInTheGame(RegionGroup):
    def __init__(self):
        self.function = 'allRegions'
        self.options = {}


# ---------------------------------------------------------------------------- #
#                                     Shops                                    #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                  Animations                                  #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                     Music                                    #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                    Sounds                                    #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                   Dialogues                                  #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                              Deprecated Actions                              #
# ---------------------------------------------------------------------------- #


class Condition(Function):
    '''Deprecated, use python comparison operators instead'''

    def __init__(self, item_a: Base, operator: str, item_b: Base):
        self.item_a = item_a
        self.operator = operator.upper()
        self.item_b = item_b
        if self.operator == 'AND' or self.operator == 'OR':
            self.comparison = operator.lower()
        else:
            self.comparison = type_of_item(item_a) or type_of_item(item_b)

    def to_dict(self):
        return [
            {
                'operandType': self.comparison,
                'operator': self.operator,
            },
            to_dict(self.item_a),
            to_dict(self.item_b)
        ]


class Calculation(Number):
    '''Deprecated, use python arithmetic operators instead'''

    def __init__(self, item_a: Number, operator: str, item_b: Number):
        self.function = 'calculate'
        self.options = {
            'items': [
                {
                    'operator': operator
                },
                to_dict(item_a),
                to_dict(item_b),
            ]
        }


class Concat(String):
    '''Deprecated, use python `+` operator instead'''

    def __init__(self, text_a, text_b):
        self.function = 'concat'
        self.options = {
            'textA': to_dict(text_a),
            'textB': to_dict(text_b),
        }
