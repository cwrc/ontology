from bs4 import BeautifulSoup
import csv
import sys

attribute_ids = {}

"""
Generates CSV files for the elements and attributes in the biography.rng file
Usage: python3 bio_csv_gen.py [orland_file]
Output:
    elements.csv for the elements along with the attributes that apply to them ID form
    attributes.csv the attributes along with the choices for the value they take
"""

def dict_to_csv(dict_list):
    entity_worksheet =  csv.DictWriter(open("elements.csv", 'w'), ["name", "attributes", "documentation"])
    attribute_worksheet = csv.DictWriter(open("attributes.csv", 'w'), ["id", "name", "choices", "documentation"])
    attributes_seen = set()

    entity_worksheet.writerow({'name': 'Name', 'documentation': 'Documentation', 'attributes': 'Attribute IDs'})
    attribute_worksheet.writerow({'id': 'ID', 'name': 'Name', 'choices': 'Choices', 'documentation': 'Documentation'})
    for item in dict_list:
        attributes = ', '.join([str(attribute_ids[attr['name']]) for attr in item['attributes']])
        row = {"name": item['name'], "documentation": item['documentation'], "attributes": attributes}

        entity_worksheet.writerow(row)

        for attr in item['attributes']:
            if attr['name'] in attributes_seen:
                continue
            else:
                attributes_seen.add(attr['name'])

            
            if 'choices' not in attr:
                attr['choices'] = []
            row = {"id": str(attribute_ids[attr['name']]), "name": attr['name'], 'choices': ', '.join(item['value'] for item in attr['choices']),
                   'documentation': attr['documentation']}
            attribute_worksheet.writerow(row)



def parse_bib(filename):

    file = open(filename)
    soup = BeautifulSoup(file, "lxml")
    define = soup.find_all(["element"])


    cur_attr_id = 0
    element_list = []
    for i in define:
        element = {}
        name = i.get('name')

        element['name'] = name
        if name is None:
            continue
        attributes = i.find_all('attribute')

        documentation = i.find('a:documentation')
        if documentation and documentation.string:
            documentation = ' '.join(documentation.string.split())
        else:
            documentation = ""
        element['documentation'] = documentation if documentation is not None else ""
        element['attributes'] = []
        for a in attributes:

            attr_name = a.get("name")
            attr_default = a.get("a:defaultValue")
            documentation = a.find('a:documentation')
            if attr_name not in attribute_ids:
                attribute_ids[attr_name] = cur_attr_id
                cur_attr_id += 1

            if documentation and documentation.string:
                documentation = ' '.join(documentation.string.split())

            attribute = {
                'name': attr_name if attr_name is not None else "",
                'default': attr_default if attr_default is not None else "",
                'documentation': documentation if documentation is not None else ""
            }
            if a.choice:
                choices = a.choice.find_all('value')
                choices_doc = a.choice.find_all('a:documentation')
                attribute['choices'] = []
                for i in range(len(choices)):
                    choice = {'value': choices[i].string}
                    attribute['choices'].append(choice)
            element['attributes'].append(attribute)
        element_list.append(element)

    return element_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: %s [orlando_biography.xml]' % sys.argv[0])


    element_list = parse_bib(sys.argv[1])
    dict_to_csv(element_list)





