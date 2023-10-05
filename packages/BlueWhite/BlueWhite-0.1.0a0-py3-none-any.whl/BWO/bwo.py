import json
from abc import abstractmethod

from . import compute
from . import constant
from . import regex

# import compute
# import constant
# import regex


class Types(type):
    class LoggerType(type):
        def __repr__(self):
            return "<class 'logger'>"

    class BlueWhiteType(type):
        def __repr__(self):
            return "<class 'bw'>"

        class LevelType(type):
            def __repr__(self):
                return "<class 'bw.level'>"

        class EffectType(type):
            def __repr__(self):
                return "<class 'bw.effect'>"

        class OperationType(type):
            def __repr__(self):
                return "<class 'bw.operation'>"

        class EventType(type):
            def __repr__(self):
                return "<class 'bw.event'>"

        class EventGroupType(type):
            def __repr__(self):
                return "<class 'bw.event-group'>"

        class ContainerType(type):
            def __repr__(self):
                return "<class 'bw.container(item)'>"

        class ProcedureType(type):
            def __repr__(self):
                return "<class 'bw.procedure'>"

        class SiteType(type):
            def __repr__(self):
                return "<class 'bw.site'>"

        class MemberType(type):
            def __repr__(self):
                return "<class 'bw.member(person)'>"

        class BattleArrayType(type):
            def __repr__(self):
                return "<class 'bw.battle-array(members and items)'>"

        class ContainTaskType(type):
            def __repr__(self):
                return "<class 'bw.container(item)'>"

        class BlueWhiteOrganizationType(type):
            def __repr__(self):
                return "<class 'bw.bwo'>"


class MoYeRanSoft:
    __copyright__ = '墨叶染千枝出品'


class Logger(MoYeRanSoft, metaclass=Types.LoggerType):
    @abstractmethod
    def write(self, tag, data):
        pass

    @abstractmethod
    def flush(self):
        pass


class BlueWhiteBase(MoYeRanSoft):
    __info__ = '此天下之非理者皆因拘之以蓝白'


class BlueWhite(BlueWhiteBase):
    def __init__(self, bwo):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.
        """
        self.bwo = bwo


class LevelBase(BlueWhite, metaclass=Types.BlueWhiteType.LevelType):
    pass


class Level(LevelBase):
    def __init__(self, bwo, level):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            level(str): The level. Must be one of the ('alpha', 'beta', 'gamma', 'delta', 'omega').
        """
        BlueWhite.__init__(self, bwo)

        if level not in constant.levels:
            self.level = constant.levels[0]
        else:
            self.level = level

    def upgrade(self):
        self + 1

    def degrade(self):
        self - 1

    def index(self):
        return constant.levels.index(self.level)

    def toZero(self):
        self.level = constant.levels[0]

    def __repr__(self):
        return f"<Level '{self.level}'>"

    def __str__(self):
        return self.level

    def __add__(self, other):
        if isinstance(other, int):
            self.level = constant.levels[self.index() + other]
            return self.level

    def __sub__(self, other):
        if isinstance(other, int):
            if self.index() - other >= 0:
                self.level = constant.levels[self.index() - other]
        return self.level

    def __eq__(self, other):
        if isinstance(other, Level):
            return self.index() == other.index()
        else:
            return self.index() == constant.levels.index(other)

    def __lt__(self, other):
        if isinstance(other, Level):
            return self.index() < other.index()
        else:
            return self.index() < constant.levels.index(other)

    def __le__(self, other):
        if isinstance(other, Level):
            return self.index() <= other.index()
        else:
            return self.index() <= constant.levels.index(other)

    def __gt__(self, other):
        if isinstance(other, Level):
            return self.index() > other.index()
        else:
            return self.index() > constant.levels.index(other)

    def __ge__(self, other):
        if isinstance(other, Level):
            return self.index() >= other.index()
        else:
            return self.index() >= constant.levels.index(other)


class EffectBase(BlueWhite, metaclass=Types.BlueWhiteType.EffectType):
    pass


class Effect(EffectBase):
    def __init__(self, bwo, name, power=0, resource=0):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the effect.

            power(int): The effect of the power.

            resource(int): The effect of the resource.
        """
        BlueWhite.__init__(self, bwo)

        self.name = name
        self.power = power
        self.resource = resource

    def execute(self):
        self.bwo.log('daily', f'受到影响: {self.name} 力量{self.power} 资源{self.resource}')
        self.bwo.power += self.power
        self.bwo.resource += self.resource


class OperationBase(BlueWhite, metaclass=Types.BlueWhiteType.OperationType):
    @abstractmethod
    def execute(self):
        pass


class Operation(OperationBase):
    def __init__(self, bwo, operations: tuple):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            operations(tuple): The operations which cannot be changed.
                eg. (
                        (lambda: True, lambda: print('Hello World')),
                        (lambda: True, lambda: input('password:'))
                    )
        """
        BlueWhite.__init__(self, bwo)

        self.operations = operations

    def execute(self):
        for operation in self.operations:
            if operation[0]():
                operation[1]()


class MutableOperation(OperationBase):
    def __init__(self, bwo, operations: list):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            operations(list): The operations which can be changed.
                eg. [lambda: print('Hello World'), lambda: input('password:')]
        """
        BlueWhite.__init__(self, bwo)

        self.operations = operations

    def add(self, operation):
        """
        Parameters:
            operation(lambda or list): One or more operations.
                eg. lambda: print('Hello World')
        """
        if isinstance(operation, list):
            for o in operation:
                self.operations.append(o)
        else:
            self.operations.append(operation)

    def execute(self):
        for operation in self.operations:
            if operation[0]:
                operation[1]()


class EventBase(BlueWhite, metaclass=Types.BlueWhiteType.EventType):
    pass


class Event(EventBase):
    def __init__(self, bwo, name, content, operation, effect):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the event.

            content(str): The content of the event.

            operation(OperationBase): The operations of the event.
                If the event is happened, the operations which can be changed or cannot be changed will be done.

            effect(Effect): The effect of the event.
        """
        BlueWhite.__init__(self, bwo)

        self.name = name
        self.content = content
        self.operation = operation
        self.effect = effect

    def execute(self):
        self.operation.execute()
        self.effect.execute()


class EventGroupBase(BlueWhite, metaclass=Types.BlueWhiteType.EventGroupType):
    pass


class EventGroup(EventGroupBase):
    events = dict()

    def __getitem__(self, item):
        if item in self.events:
            return self.events[item]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex0.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex0.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex1.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex1.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex2.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex2.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex3.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex3.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex4.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex4.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex5.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex5.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex6.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex6.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex7.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex7.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex8.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex8.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex9.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex9.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex10.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex10.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex11.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex11.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex12.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex12.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex13.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex13.match(item)[1]]
        elif regex.Compiles.BlueWhite.EventGroup.indexRegex14.match(item) is not None:
            return self[regex.Compiles.BlueWhite.EventGroup.indexRegex14.match(item)[1]]
        else:
            return None


class MemberEventGroup(EventGroup):
    def __init__(self, bwo, bornEvent=None, dieEvent=None, inEvent=None, outEvent=None):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            bornEvent(Event): The event when the member born.

            dieEvent(Event): The event when the member die.

            inEvent(Event): The event when the member join the BWO.

            outEvent(Event): The event when the member exit the BWO.
        """
        BlueWhite.__init__(self, bwo)

        self.bronEvent = bornEvent
        self.dieEvent = dieEvent
        self.inEvent = inEvent
        self.outEvent = outEvent

        self.events.update(
            {
                'bron': bornEvent,
                'diet': dieEvent,
                'in': inEvent,
                'out': outEvent,
            }
        )


class ContainerEventGroup(EventGroup):
    def __init__(self, bwo, foundEvent=None, inEvent=None, outEvent=None):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            foundEvent(Event): The event when the container is found.

            inEvent(Event): The event when the container join the BWO.

            outEvent(Event): The event when the container exit the BWO.
        """
        BlueWhite.__init__(self, bwo)

        self.foundEvent = foundEvent
        self.inEvent = inEvent
        self.outEvent = outEvent

        self.events.update(
            {
                'found': foundEvent,
                'in': inEvent,
                'out': outEvent,
            }
        )


class ContainTaskEventGroup(EventGroup):
    def __init__(self, bwo, executeEvent=None, successEvent=None, failureEvent=None):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            executeEvent(Event): The event when the contain task execute.

            successEvent(Event): The event when the contain task is successful.

            failureEvent(Event): The event when the contain task is failed.
        """
        BlueWhite.__init__(self, bwo)

        self.executeEvent = executeEvent
        self.successEvent = successEvent
        self.failureEvent = failureEvent

        self.events.update(
            {
                'execute': executeEvent,
                'success': successEvent,
                'failure': failureEvent,
            }
        )


class Item:
    pass


class ContainerBase(BlueWhite, Item, metaclass=Types.BlueWhiteType.ContainerType):
    def __init__(self, bwo, name, quantity, ability, events):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the container.

            quantity(int): The quantity of the container.

            ability(str): The ability of the container.

            events(ContainerEventGroup): The events of the container.
        """
        BlueWhite.__init__(self, bwo)

        self.name = name
        self.quantity = quantity
        self.ability = ability
        self.events = events


class SingleContainer(ContainerBase):
    def __init__(self, bwo, name, ability, events):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the container.

            ability(str): The ability of the container.

            events(ContainerEventGroup): The events of the container.
        """
        ContainerBase.__init__(self, bwo, name, 1, ability, events)


class MultipleContainer(ContainerBase):
    def __init__(self, bwo, name, quantity, ability, events):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the container.

            quantity(int): The quantity of the container.

            ability(str): The ability of the container.

            events(ContainerEventGroup): The events of the container.
        """
        ContainerBase.__init__(self, bwo, name, quantity, ability, events)


class ProcedureBase(BlueWhite, metaclass=Types.BlueWhiteType.ProcedureType):
    pass


class Procedure(ProcedureBase):
    pass


class SiteBase(BlueWhite, metaclass=Types.BlueWhiteType.SiteType):
    pass


class Site(SiteBase):
    pass


class Person:
    def __init__(self, name, sex, birth):
        self.name = name
        self.sex = sex
        self.birth = birth

        self.exist = True

    @abstractmethod
    def die(self):
        pass

    def __bool__(self):
        return self.exist


class MemberBase(BlueWhite, Person, metaclass=Types.BlueWhiteType.MemberType):
    @abstractmethod
    def die(self):
        pass


class Member(MemberBase):
    def __init__(self, bwo, name, sex, birth, ability, level, events):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the member.

            sex(str): The sex of the member.

            birth(str): The birth of the member.

            ability(str): The ability of the member.

            level(str or Level): The level of the member.

            events(MemberEventGroup): The events of the member.
        """
        BlueWhite.__init__(self, bwo)
        Person.__init__(self, name, sex, birth)

        self.ability = ability
        self.events = events

        if isinstance(level, Level):
            self.level = level
        else:
            self.level = Level(bwo, level)

    def upgrade(self):
        self.level + 1

    def die(self):
        self.exist = False
        self.bwo.members.remove(self)
        self.bwo.log('danger', f'{self.name}, {self.level}级社员, 壮烈牺牲, 实乃悲天悯人, 天妒英才也')

    def __str__(self):
        return json.dumps(
            {
                'name': str(self.name),
                'sex': str(self.sex),
                'birth': str(self.birth),
                'ability': str(self.ability),
                'level': str(self.level),
                'exist': str(self.exist),
                'events': str(self.events)
            },
            indent=4
        )

    def __bool__(self):
        return self.exist


class BattleArrayBase(BlueWhite, metaclass=Types.BlueWhiteType.BattleArrayType):
    pass


class BattleArray(BattleArrayBase):
    def __init__(self, bwo, name, people, items):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the battle array.

            people(set[Person]): The people of the battle array.

            items(set[Item]): The items of the battle array.
        """
        BlueWhite.__init__(self, bwo)

        self.name = name
        self.people = people
        self.items = items

    def checkSurvival(self):
        for person in self.people.copy():
            if not person:
                self.people.remove(person)
                self.bwo.log('warning', f'{person.name}已死, 无法继续跟随大部队, 颇为可惜')


class ContainTaskBase(BlueWhite, metaclass=Types.BlueWhiteType.ContainTaskType):
    def __init__(self, bwo, name, description, content, battleArray):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the contain task.

            description(str): The description of the contain task.

            content(str): The content of the contain task.

            battleArray(BattleArray): The battle array of the contain task.
        """
        BlueWhite.__init__(self, bwo)

        self.name = name
        self.description = description
        self.content = content
        self.battleArray = battleArray

    @abstractmethod
    def execute(self):
        pass


class ContainTask(ContainTaskBase):
    def __init__(self, bwo, name, description, content, battleArray, events):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the contain task.

            description(str): The description of the contain task.

            content(str): The content of the contain task.

            battleArray(BattleArray): The battle array of the contain task.

            events(EventGroup): The events of the contain task.
        """
        ContainTaskBase.__init__(self, bwo, name, description, content, battleArray)

    def execute(self):
        pass


class FakeContainTask(ContainTaskBase):
    def __init__(self, bwo, name, description, content, battleArray, event):
        """
        Parameters:
            bwo(BlueWhiteOrganization): Blue White Organization.

            name(str): The name of the contain fake task.

            description(str): The description of the fake contain task.

            content(str): The content of the fake contain task.

            battleArray(BattleArray): The battle array of the fake contain task.

            event(Event): The event of the fake contain task.
        """
        ContainTaskBase.__init__(self, bwo, name, description, content, battleArray)

        self.event = event

    def execute(self):
        self.bwo.log('danger', self.content)
        self.battleArray.checkSurvival()
        self.event.execute()


class Organization:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exist = True

    def destroy(self):
        self.exist = False


class BlueWhiteOrganizationBase(BlueWhiteBase, Organization, metaclass=Types.BlueWhiteType.BlueWhiteOrganizationType):
    pass


class BlueWhiteOrganization(BlueWhiteOrganizationBase):
    def __init__(self, logger):
        """
        The BWO.
        """
        Organization.__init__(self, '蓝白社', '至高蓝白社下属, 宇宙最强收容组织, 此天下之非理者皆因拘之以蓝白')
        self._logger = logger

        self._power = compute.Random.ZeroToHundred()
        self._resource = compute.Random.ZeroToHundred()
        self._members = set()

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value
        self.log('info', f'力量更新为:{self.power}')

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value
        self.log('info', f'资源更新为:{self.resource}')

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, value):
        self._members = value

    def log(self, tag, data):
        self.logger.write(tag, data + '\n')
        self.logger.flush()

    def addMember(self, member: Member):
        self.members.add(member)
        self.log('warning', f'新人{member.name}入社, 心性出色, 能力经天纬地, 实乃蓝白社之大幸')

    def destroy(self):
        super().destroy()
        self.log(
            'danger',
            '蓝白社在你的英明领导下, 于此时此刻正式解散, 彻底毁灭, 实乃惊天地泣鬼神之壮举, 真乃天妒英才也, '
            '作为领袖与蓝白社集体意志统合体, 你无疑是失败的, 但作为收容者, 此举引发未知之规则, 使天下非理者皆死尽, 实乃功德无量, '
            '得至高蓝白社之青睐也, 非蓝牧与白歌之流可比, 墨穷与黄极不及汝之万一, 炎奴与沧月, 亦惊叹汝之所为'
        )

    def __str__(self):
        return json.dumps(
            {
                'power': str(self.power),
                'resource': str(self.resource)
            },
            indent=4
        )


if __name__ == '__main__':
    _bwo = BlueWhiteOrganization(Logger())
    # l = Level(_bwo, 'alpha')
    # _bwo.addMember(
    #     Member(
    #         _bwo, '', '', '', '', l
    #     )
    # )

    # l + 2
    print(_bwo)
    print(_bwo.power)
    print(_bwo.members)
    e = Effect(_bwo, '', -10, -20)
    e.execute()
    print(_bwo)
