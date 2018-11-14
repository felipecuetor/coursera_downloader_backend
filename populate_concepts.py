import requests
with open("labels_en.ttl") as infile:
    first_line = True
    for line in infile:
        if first_line:
            first_line = False
        else:
            first_split = line.split("> ")
            first_uri = first_split[0][1:]
            second_uri = first_split[1][1:]
            second_split = first_split[2].split("\"")
            label = second_split[1]
            third_split = second_split[2].split(" ")
            language = third_split[0][1:]
            url = 'http://localhost:8080/concept/'
            payload = {
                'concept_uri': first_uri,
                'concept_uri_alternate': second_uri,
                'concept_label': label,
                'concept_language':language
            }
            r = requests.post(url, data=payload)
