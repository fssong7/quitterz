from inputs import people

for person in people:
    print(person.get("name", "Unknown"))