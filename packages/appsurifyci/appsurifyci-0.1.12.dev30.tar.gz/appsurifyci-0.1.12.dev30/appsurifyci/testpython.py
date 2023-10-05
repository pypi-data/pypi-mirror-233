from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

filepath = "c:\\xml\\testAPI_junitResults_formatted_edited.xml"

try:
    with open(filepath, "r", errors="replace", encoding="utf8") as f:
        root = ET.fromstring(f.read())
        tree = ET.ElementTree()
        added_failure_type = False
        print("here-1")
        for test in root.findall('testcase'):
            failure = test.find('failure')
            if failure is None:
                continue
            else:
                if "type" not in failure.attrib:
                    failure.set("type", "AssertionError")
                    added_failure_type = True
        for test in root.findall('testcase'):
            error = test.find('error')
            if error is None:
                continue
            else:
                if "type" not in failure.attrib:
                    error.set("type", "AssertionError")
                    added_failure_type = True
        added_failure_type = False
        for test in root.findall('testcase'):
            failure = test.find('failure')
            if failure is None:
                continue
            typeoffailure = failure.find('type')
            if typeoffailure is None:
                continue
            else:
                if typeoffailure.text == "":
                    typeoffailure.text = "failure"
                    added_failure_type = True
        print("-4")
        for testsuites in root.findall('testsuite'):
            print("-5")
            for test in testsuites.findall("testcase"):
                error = test.find('error')
                if error is None:
                    continue
                typeoffailure = error.find('type')
                if typeoffailure is None:
                    continue
                
                else:
                    print("here")
                    print(typeoffailure.text)
                    if typeoffailure.text == "" or typeoffailure.text is None:
                        typeoffailure.text = "error"
                        added_failure_type = True
        if added_failure_type:
            tree._setroot(root)
            tree.write(filepath)
except:
    print("unable to set failure type")