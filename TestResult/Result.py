__author__ = 'Woody'
import unittest


class result(unittest.TextTestResult):
    successes = []
    failures = []
    errors = []
    skipped = []

    def addSuccess(self, test):
        case_id = test.case_id
        self.stream.writeln("ok")
        if case_id not in self.successes:
            self.successes.append({"case_id": case_id, "case": test, "type": "success"})

    def addFailure(self, test, err):
        self.stream.writeln("FAIL")
        case_id = test.case_id
        if case_id not in self.failures:
            self.failures.append({"case_id": case_id, "case": test, "msg": err, "type": "danger"})

    def addError(self, test, err):
        self.stream.writeln("ERROR")
        try:
            case_id = test.case_id
            if case_id not in self.errors:
                self.errors.append({"case_id": case_id, "case": test, "msg": err, "type": "warning"})
        except:
            self.errors.append({"case_id": test.description, "case": test, "msg": err, "type": "warning"})

    def addSkip(self, test, reason):
        self.stream.writeln("skipped {0!r}".format(reason))
        case_id = test.case_id
        if case_id not in self.skipped:
            self.skipped.append({"case_id": case_id, "case": test, "msg": reason, "type": "info"})

    def printErrorList(self, flavour, errors):
        pass

    def printErrors(self):
        pass