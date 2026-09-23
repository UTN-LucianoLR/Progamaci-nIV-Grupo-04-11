# import json
 
# with open("data/tasks_provider_a.json", encoding="utf-8") as f:
#     data = json.load(f)

# import csv
# with open("data/task_provider_b.csv", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)

import xml.etree.ElementTree as ET
tree = ET.parse("data/task_provider_c.xml") 
root = tree.getroot()
for task in root.findall("task"):
    print({
        "title": task.find("title").text,
        "priority": task.find("priority").text,
        "status": task.find("status").text,
    })