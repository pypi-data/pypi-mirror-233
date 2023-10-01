from typing import *
import asyncio
import logging
import traceback
import sys
import json
import copy
from copy import deepcopy
from .utils import getLang
# from .objects import removeAttributesOfObject

log = logging.getLogger(__name__)

def InitialMapFunct(value: any):
    return value

def ValidatorElement(valueVE: any, rule):
    try:
        resVE = valueVE
        
        if(
            (
                rule is not None and
                type(rule) == dict
            ) and resVE['valid'] == True
        ):
            if(
                'init' in rule.keys() and
                rule['init'] and
                callable(rule['init']) and
                rule['init'] is not None
            ):
                resVE['data'] = rule['init'](resVE['data'])
            if(
                'rule' in rule.keys() and
                rule['rule'] and
                callable(rule['rule']) and
                rule['rule'] is not None
            ):
                resVE = rule['rule'](resVE['data'])
            resVE['data'] = rule['sanitize']( resVE['data']) if (
                type(rule) == dict and
                'sanitize' in rule.keys() and
                rule['sanitize'] and
                callable(rule['sanitize']) and
                rule['sanitize'] is not None
            ) else  resVE['data']
            # print("-- JON - ValidatorElement | resVE['data']:: ", resVE['data'])
            # resVE['data'] = removeAttributesOfObject(resVE['data'])

        return resVE
    except Exception as err:
        stack = traceback.format_exc()
        log.error(stack)
        return {
            'data': None,
            'valid': False,
            'error': 'unknown error',
        }

class JONDefaultSchema():
    _label: str = None
    _lang: str = 'fr'
    _options: dict = {
        'validationType': 'any',
        'type': 'any',
        'instance': None,
        'rules': [],
    }
    _defaultValue = None
    _finalError: Exception = None
    _customError: Exception = None
    map = None

    _rule__init = None
    _rule__required = None
    _rule__enum = None
    _rule__enumNot = None
    _rule__applyApp = None
    _rule__applyApp2 = None
    _rule__applyApp3 = None
    _rule__applyApp4 = None
    _rule__applyApp5 = None
    _rule__applyApp6 = None
    _rule__applyApp7 = None
    _rule__applyApp8 = None
    _rule__applyApp9 = None
    _rule__applyApp10 = None
    _rule__applyApp11 = None
    _rule__applyApp12 = None
    _rule__applyApp13 = None
    _rule__applyApp14 = None
    _rule__applyApp15 = None
    _rule__applyApp16 = None
    _rule__applyApp17 = None
    _rule__applyApp18 = None
    _rule__applyApp19 = None
    _rule__applyApp20 = None

    def __init__(self, lang: str = 'fr'):
        self.set_lang(lang)
        self.set_finalError()
        # print(('-- JONDefaultSchema --')
        # print(('-- JONDefaultSchema | self._lang:: ', self._lang)


    def JONApplyAppValidator(self,
        resValidator_: any
    ) -> dict:
        try:
            # --<- applyApp
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp)
            # --<- applyApp2
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp2)
            # --<- applyApp3
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp3)
            # --<- applyApp4
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp4)
            # --<- applyApp5
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp5)
            # --<- applyApp6
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp6)
            # --<- applyApp7
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp7)
            # --<- applyApp8
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp8)
            # --<- applyApp9
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp9)
            # --<- applyApp10
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp10)
            # --<- applyApp11
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp11)
            # --<- applyApp12
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp12)
            # --<- applyApp13
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp13)
            # --<- applyApp14
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp14)
            # --<- applyApp15
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp15)
            # --<- applyApp16
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp16)
            # --<- applyApp17
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp17)
            # --<- applyApp18
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp18)
            # --<- applyApp19
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp19)
            # --<- applyApp20
            resValidator_ = ValidatorElement(resValidator_, rule=self._rule__applyApp20)
        except Exception as err:
            stack = traceback.format_exc()
            resValidator_ = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            
            log.error(stack)

        # print(("> JONschemas | JONDefaultSchema - JONApplyAppValidator - resValidator_:: ", resValidator_)
        return resValidator_
    def JONvalidator(self,
        value: any
    ) -> dict:
        # value = deepcopy(value)
        resValidator = {
            'data': None,
            'valid': None,
            'error': None
        }

        try:
            if(value is None):
                value = self._defaultValue
            # print(("> JONDefaultSchema.JONvalidator ", self.get_label(), " self._defaultValue : ", self._defaultValue)
            # print(("> JONDefaultSchema.JONvalidator ", self.get_label(), " value : ", value)
            if(self._rule__init is not None and type(self._rule__init) == dict):
                if(
                    'init' in self._rule__init.keys() and
                    self._rule__init['init'] and
                    callable(self._rule__init['init'])
                ):
                    resValidator['data'] = self._rule__init['init'](value)
                else:
                    resValidator['data'] = value
                resValidator = self._rule__init['rule'](resValidator['data'])
                resValidator['data'] = self._rule__init['sanitize']( resValidator['data']) if (
                    'sanitize' in self._rule__init.keys() and
                    callable(self._rule__init['sanitize'])
                ) else  resValidator['data']
            # --> OTHERS RULES
            # --<- required
            resValidator = ValidatorElement(resValidator, rule=self._rule__required)
            """if(
                'init' in self._rule__required.keys() and
                self._rule__required['init'] and
                callable(self._rule__required['init'])
            ):
                resValidator['data'] = self._rule__required['init'](resValidator['data'])
            resValidator = self._rule__required['rule'](resValidator['data'])
            resValidator['data'] = self._rule__required['sanitize']( resValidator['data']) if (
                type(self._rule__required) == dict and
                'sanitize' in self._rule__required.keys() and
                self._rule__required['sanitize'] and
                callable(self._rule__required['sanitize'])
            ) else  resValidator['data']"""
            # --<- enum
            resValidator = ValidatorElement(resValidator, rule=self._rule__enum)
            # --<- enumNot
            resValidator = ValidatorElement(resValidator, rule=self._rule__enumNot)

            if(resValidator['valid'] is None):
                resValidator = {
                    'data': None,
                    'valid': False,
                    'error': str({
                        'fr': "aucune règle n'est appliquée",
                        'en': "no rule is applied",
                    }[self._lang]),
                }
        except Exception as err:
            stack = traceback.format_exc()
            resValidator = {
                'data': None,
                'valid': False,
                'error': str(stack),
            }
            
            log.error(stack)

        # print(("> JONschemas | JONDefaultSchema - JONvalidator - resValidator:: ", resValidator)

        return resValidator
    def validator(self,
        value: any
    ) -> dict:
        # value = deepcopy(value)
        return self.JONvalidator(value)
    def validate(self, value: any) -> dict :
        # value = deepcopy(value)
        try:
            # self.init()
            # print(("""> JONschemas | JONDefaultSchema - validate - self._options['validationType']:: """, self._options['validationType'])
            # print(("""> JONschemas | JONDefaultSchema - validate - self._options['type']:: """, self._options['type'])
            # print(("""> JONschemas | JONDefaultSchema - validate - self._options['instance']:: """, self._options['instance'])
            # print(("""> JONschemas | JONDefaultSchema - validate - self._options['rules']:: """, self._options['rules'])

            if(self._options['validationType'] in ['number', 'string', 'boolean', 'date', 'file', 'enum', 'notInEnum', 'chosenType', 'object']):
                resV = self.validator(value)
                # print("""> JONschemas | JONDefaultSchema - validate - self.validator(value):: """, resV)
                resV = self.JONApplyAppValidator(deepcopy(resV))
                # print("""> JONschemas | JONDefaultSchema - validate - self.JONApplyAppValidator(deepcopy(resV)):: """, resV)
                resV['data'] = None if (
                    (
                        (
                            type(resV['data']) == dict and
                            len(resV['data'].keys()) <= 0
                        ) or 
                        (
                            type(resV['data']) in (list, tuple) and
                            len(resV['data']) <= 0
                        )
                    ) and not(resV['valid'] == True)
                ) else resV['data']
                resV['error'] = str(resV['error']) if resV['error'] is not None else None
                if(resV['valid'] == True and self.map is not None and callable(self.map)):
                    # print(("---- ICI ----")
                    resV['data'] = self.map(resV['data'])
                return resV

            return {
                'data': None,
                'valid': False,
                'error': str(self.get_error()),
            }
        except Exception as err:
            code = str(type(err))
            msg = str(err)
            stack = str(traceback.format_exc())
            
            log.error(stack)
            return {
                'data': None,
                'valid': False,
                'error': 'unknown error during validation',
            }

    def ruleNames(self,) -> list:
        return list(
            map(
                lambda data: data['name'],
                self._options['rules'],
            )
        )
        
    def error(self, value: any) -> Exception:
        return (self.validate(value))['error']
    def isValid(self, value: any) -> bool :
        return (self.validate(value))['valid']
    def sanitize(self, value: any) -> any :
        return (self.validate(value))['data']

    def get_rules(self,):
        return self._options['rules']
    def set_rules(self, rules: list):
        self._options['rules'] = rules
    def get_lang(self,):
        return self._lang
    def set_lang(self, lang: str):
        self._lang = getLang(lang)
    def get_label(self,):
        return self._label if (
            type(self._label) in [str] and
            len(self._label) > 0
        ) else {
            'fr': 'l\'element',
            'en': 'the element'
        }[self._lang]
    def set_label(self, label: any):
        self._label = label if (
            type(label) in [str] and
            len(label) > 0
        ) else None
    def get_error(self,):
        return self._finalError
    def set_finalError(self, finalError: any = None):
        try:
            self._finalError = Exception(
                finalError[self._lang] if(
                    type(finalError) == dict
                ) else finalError
            ) if type(finalError) is not Exception else finalError
        except:
            self._finalError = Exception(
                {
                    'fr': 'erreur interne inconnue',
                    'en': 'unknown internal error',
                }[self._lang]
            )
    def set_error(self, errorValue: any = None):
        try:
            self._customError = Exception(
                errorValue[self._lang] if(
                    type(errorValue) == dict
                ) else errorValue
            )
        except:
            self._customError = Exception(
                {
                    'fr': 'erreur interne inconnue',
                    'en': 'unknown internal error',
                }[self._lang]
            ) if type(errorValue) is not Exception else errorValue
    def get_defaultValue(self,):
        return self._defaultValue
    def set_defaultValue(self, defaultValue: any):
        self._defaultValue = defaultValue

    def lang(self, value: str):
        self.set_lang(value)
        return self
    def label(self, value: any):
        self.set_label(value)
        return self
    def default(self, value: any):
        self.set_defaultValue(value)
        return self
    def defaultError(self, defaultErr: any):
        self.set_error(defaultErr)
        return self
    def required(self,):
        def ruleFunct(value: any) -> dict:
            data: any = None
            valid: bool = False
            error: any = None

            valid = True if (
                value is not None
            ) else False

            if(valid == True):
                error = None
                data = value
            else:
                labelSTR = json.dumps(self.get_label() if (
                    type(self.get_label()) == str and
                    len(self.get_label()) > 0
                ) else {
                    'fr': 'l\'element',
                    'en': 'the element'
                }[self._lang])
                err = Exception({
                    'fr': "{label} est requis".format(
                        label = labelSTR,
                    ),
                    'en': "{label} is required".format(
                        label = labelSTR,
                    ),
                }[self._lang])
                self.set_finalError(err)
                error = self.get_error()
                data = None

            return {
                'data': data,
                'valid': valid,
                'error': error,
            }

        self._rule__required = {
            'name': 'required',
            'rule': ruleFunct,
            'schema': self._options['instance'],
        }

        return self
    def enum(self, *choices: any):
        choices = choices if type(choices) in (list, tuple) else None
        choiceIsNone = choices is None
        def ruleFunct(value: any) -> dict:
            data: any = None
            valid: bool = False
            error: any = None

            valid = True if (
                (
                    value is None or (
                        value in choices
                    )
                ) and (
                    self._rule__init is not None
                ) and not(choiceIsNone == True)
            ) else False

            if(valid == True):
                error = None
                data = value
            else:
                labelSTR = json.dumps(self.get_label())
                self.set_finalError({
                    'fr': "{label} correspond à aucun choix défini".format(
                        label = labelSTR,
                    ),
                    'en': "{label} correspond to any defined choice".format(
                        label = labelSTR,
                    ),
                })
                error = self.get_error()
                data = None

            return {
                'data': data,
                'valid': valid,
                'error': error,
            }

        self._rule__enum = {
            'name': 'enum',
            'rule': ruleFunct,
            'schema': self._options['instance'],
        }

        return self
    def enumNot(self, *choices: any):
        choices = choices if type(choices) in (list, tuple) else []
        choiceIsNone = choices is None
        def ruleFunct(value: any) -> dict:
            data: any = None
            valid: bool = False
            error: any = None

            valid = True if (
                (
                    value is None or (
                        not(value in choices)
                    )
                ) and (
                    self._rule__init is not None
                ) and not(choiceIsNone == True)
            ) else False

            if(valid == True):
                error = None
                data = value
            else:
                labelSTR = json.dumps(self.get_label())
                self.set_finalError({
                    'fr': "{label} ne correspond à aucun choix défini".format(
                        label = labelSTR,
                    ),
                    'en': "{label} does not correspond to any defined choice".format(
                        label = labelSTR,
                    ),
                })
                error = self.get_error()
                data = None

            return {
                'data': data,
                'valid': valid,
                'error': error,
            }

        self._rule__enumNot = {
            'name': 'enumNot',
            'rule': ruleFunct,
            'schema': self._options['instance'],
        }

        return self
    def applyAppInit(self,
        name: str = 'applyApp',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        def ruleF(value: any) -> dict:
            data: any = None
            valid: bool = False
            error: any = None

            # print(("> JONschemas | defaultSchema - applyAppInit - ruleF - value:: ", value)
            # print(("> JONschemas | defaultSchema - applyAppInit - ruleF - rule:: ", rule)
            # print(("> JONschemas | defaultSchema - applyAppInit - ruleF - value['password']:: ", value['password'])
            # print(("> JONschemas | defaultSchema - applyAppInit - ruleF - value['confirmpassword']:: ", value['confirmpassword'])
            # print(("> JONschemas | defaultSchema - applyAppInit - ruleF - (value['password'] == value['confirmpassword']):: ", (value['password'] == value['confirmpassword']))

            valid = True if (
                (
                    value == None or (
                        callable(rule) and
                        rule(value) == True
                    )
                ) and (
                    self._rule__init is not None
                )
            ) else False

            if(valid == True):
                error = None
                data = value
            else:
                labelSTR = json.dumps(self.get_label())
                self.set_finalError({
                    'fr': "la condition appliquéé à {label} est invalide".format(
                        label = labelSTR,
                    ),
                    'en': "the condition applied to {label} is invalid".format(
                        label = labelSTR,
                    ),
                } if exception is None else exception)
                error = self.get_error()
                data = None

            return {
                'data': data,
                'valid': valid,
                'error': error,
            }

        return {
            'name': name if (
                type(name) == str and
                len(name) > 0
            ) else 'applyApp',
            'rule': ruleF,
            'sanitize': sanitize if callable(sanitize) else None,
            'init': init if callable(init) else None,
        }
    def applyApp(self,
        name: str = 'applyApp',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        self._rule__applyApp = self.applyAppInit(
            name=name,
            init=init,
            rule=rule,
            sanitize=sanitize,
            exception=exception,
        )

        return self
    def applyApp2(self,
        name: str = 'applyApp2',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        self._rule__applyApp2 = self.applyAppInit(
            name=name,
            init=init,
            rule=rule,
            sanitize=sanitize,
            exception=exception,
        )

        return self
    def applyApp3(self,
        name: str = 'applyApp3',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        self._rule__applyApp3 = self.applyAppInit(
            name=name,
            init=init,
            rule=rule,
            sanitize=sanitize,
            exception=exception,
        )

        return self
    def applyApp4(self,
        name: str = 'applyApp4',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        self._rule__applyApp4 = self.applyAppInit(
            name=name,
            init=init,
            rule=rule,
            sanitize=sanitize,
            exception=exception,
        )

        return self
    def applyApp5(self,
        name: str = 'applyApp5',
        init = (lambda data: data),
        rule = (lambda data: not(not(data))),
        sanitize = (lambda data: data),
        exception = None
    ):
        self._rule__applyApp5 = self.applyAppInit(
            name=name,
            init=init,
            rule=rule,
            sanitize=sanitize,
            exception=exception,
        )

        return self

    def applyMapping(self, map = InitialMapFunct):
        self.map = map
        return self