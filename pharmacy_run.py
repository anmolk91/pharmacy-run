from graph import Graph

class PharmacyRun :

    edges = []
    vertices = []
    prompts = []
    pharmacyGraph = None
    

    def __init__(self, file_name):
        formatted_data = self.read_input(file_name)
        self.edges = formatted_data['edges']
        self.vertices = formatted_data['vertices']
        self.prompts = formatted_data['prompts']
        self.pharmacyGraph = Graph(self.vertices, self.edges)
        self.process_prompts()

    def process_prompts(self):
        """
            process the prompts on the input files
        """
        self.clear_output_file()
        for prompt in self.prompts:
            source_index = self.vertices.index(prompt['source'])
            distance = self.pharmacyGraph.find_shortest_path(source_index)
            pharmacy_one_index = self.vertices.index(prompt['pharmacy1'])
            pharmacy_two_index = self.vertices.index(prompt['pharmacy2'])
            if distance[pharmacy_one_index] > distance[pharmacy_two_index]:
                self.print_output('Pharmacy 2', self.pharmacyGraph.path[pharmacy_two_index], distance[pharmacy_two_index])
            elif distance[pharmacy_one_index] < distance[pharmacy_two_index]:
                self.print_output('Pharmacy 1', self.pharmacyGraph.path[pharmacy_one_index], distance[pharmacy_one_index])

    def read_input(self, input_file_name):
        """
            reads raw file input and convert the raw data to
            edges and vertices
        """
        return self.format_raw_data(self.get_file_content(input_file_name))

    def format_raw_data(self, input_raw_data = ''):
        """
            formats raw input data in to edges and vertices
        """
        data = input_raw_data.split('\n')
        vertices_list = []
        edges_list = []
        prompts = []
        promptObj = {
            'source': -1,
            'pharmacy1': None,
            'pharmacy2': None
        }
        for raw_data_line in data:
            if raw_data_line != None:
                if '/' in raw_data_line:
                    data = [data_item.strip() for data_item in raw_data_line.split('/')]
                    if len(data) == 3:
                        if data[0] not in vertices_list:
                            vertices_list.append(data[0])
                        if data[1] not in vertices_list:
                            vertices_list.append(data[1])
                        new_edge_id = ''.join(sorted(data))
                        if next((edge for edge in edges_list if edge['edge_id'] == new_edge_id ), None) == None:
                            edges_list.append( { 'edge_id': new_edge_id, 'vertice_one': data[0], 'vertice_two': data[1], 'weight': data[2] } )
                elif 'House' in raw_data_line:
                    inp_list = raw_data_line.split(':')
                    promptObj['source'] = inp_list[1].strip()
                elif 'Pharmacy 1' in raw_data_line:
                    inp_list = raw_data_line.split(':')
                    promptObj['pharmacy1'] = inp_list[1].strip()
                elif 'Pharmacy 2' in raw_data_line:
                    inp_list = raw_data_line.split(':')
                    promptObj['pharmacy2'] = inp_list[1].strip()
                    prompts.append(promptObj)
                    promptObj = {
                        'source': -1,
                        'pharmacy1': None,
                        'pharmacy2': None
                    }


        return {
            'vertices': vertices_list,
            'edges': edges_list,
            'prompts': prompts
        }


    def print_output(self, safer_pharmacy, path, containment_zone_count):
        """
            creates an output string from the results and then prints the results
        """
        output = '\n\nSafer Pharmacy is: {pharmacy}\n'.format(pharmacy = safer_pharmacy)
        output += 'Path to follow: {path}\n'.format(path = ' '.join(path))
        output += 'Containment zones on this path: {zones}\n\n'.format(zones = containment_zone_count)
        self.write_output(output)

    def clear_output_file(self):
        """
            clear output file
        """
        with open('outputPS8.txt', 'a') as file:
            file.seek(0)
            file.truncate()

    def write_output(self, output):
        """
            writes the output
        """
        with open('outputPS8.txt', 'a') as file:
            file.write(output)

        
    def get_file_content(self, filePath, mode='r'):
        """
            opens file in the mode provided and returns of the file
        """
        with open(filePath, mode) as my_file:
            return my_file.read()
