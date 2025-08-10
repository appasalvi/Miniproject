"""

This is where the implementation of the plugin code goes.
The CodeGenerator-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase
import os

# Setup a logger
logger = logging.getLogger('CodeGenerator')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
dirpath = os.path.dirname(os.path.abspath(__file__))
generated_python = open(os.path.join(dirpath,'domainSM.py'), 'r').read()


class CodeGenerator(PluginBase):
    def main(self):
        core = self.core
        active_node = self.active_node
        META = self.META
        logger = self.logger

        # Printing static imports and SM creation command
        model_code = "from .domainSM import StateMachine\n\n"
        model_name = core.get_attribute(active_node, 'name')
        model_code += model_name + " = StateMachine()\n"

        # Loading all nodes for easy iteration
        nodes = core.load_sub_tree(active_node)

        # Create output content
        output_content = "# Generated Python code\nprint('Hello from WebGME!')\n"

        for meta_name in nodes:
            # logger.debug("Part 1:" + core.get_attribute(meta_name, 'name'))
            if core.get_attribute(meta_name, 'name') != 'Sequence':
                # First thing to print out to .py file
                logger.debug(core.get_attribute(meta_name, 'name'))
                # logger.debug("Working directory: " + core.working_directory)

                logger.info("Part 1")
                current_attribute_names = core.get_attribute_names(meta_name)
                logger.debug(current_attribute_names)
                for attribute_name in current_attribute_names:
                    attribute_value = core.get_attribute(meta_name, attribute_name)
                    logger.debug(attribute_value)
                    if attribute_name not in ["scriptCode", "pythonCode", "name"]:
                        output_content = output_content + '\n'+ core.get_attribute(meta_name, 'name') + '(' + str(attribute_value) + ')'
                    else:
                        pass
                logger.info("Part 2")
                if current_attribute_names[0] is not None:
                    #logger.debug(core.get_children_meta(meta_name))
                    logger.debug(current_attribute_names[0])
                else:
                    logger.debug("Parameter is Null")
                logger.info("Part 3")
                if current_attribute_names[0] is not None:
                    # logger.debug(core.get_set_names(current_attribute_names[0]))
                    # logger.debug(core.load_pointer(current_attribute_names[0]))
                    # TODO: Needs to go one-level deeper to get the inputs
                    logger.info("Defining depth to extract value")
                    # Get the values for each attribute
                    attribute_values = {}
                    for attr_name in current_attribute_names[0]:
                        attr_value = core.get_attribute(meta_name, attr_name)
                        attribute_values[attr_name] = attr_value
                    logger.debug(attribute_values)
                else:
                    logger.debug("Parameter is Null")
                logger.info("Part 4")
            else:
                logger.info("Skipping Sequence")
            # for node in nodes:
            # if core.is_type_of(node, META['Turtle']) and not core.is_type_of(node, META['Sequence']):
                # model_code += model_name + ".add_state(\"" + core.get_attribute(meta_name, 'name') + "\")\n"

        artifact = {}
        artifact['generated_python.py'] = generated_python
        artifact[model_name + '.py'] = output_content
        self.add_artifact('SmToPy_' + model_name, artifact)

        # Construct path to src/common directory
        # Get the project root directory (go up from working directory)
        project_root = os.path.dirname(os.path.dirname(self.working_directory))
        src_common_path = os.path.join(project_root, "src", "common")

        # Ensure the src/common directory exists
        os.makedirs(src_common_path, exist_ok=True)

        # Define the target file path
        target_file_path = os.path.join(src_common_path, "generated_module.py")

        # Write the Python file to src/common
        with open(target_file_path, 'w') as f:
            f.write(output_content)

        self.logger.info(f"Python file saved to: {target_file_path}")

        # Optionally, also add it as an artifact for download
        self.add_artifact(target_file_path, "generated_module.py")

        self.result_set_success(True)
        return self.result

        # Printing execution initiation code
        model_code += "\n" + model_name + ".run()\n"
        logger.debug(model_code)

        logger.debug(output_content)

    # Generate your Python code content
    python_code = '''# Generated by WebGME Plugin
import json

def process_node_data():
    """Function generated from WebGME node attributes"""
    print("Processing node data...")
    return True

if __name__ == "__main__":
    process_node_data()
'''

        # Saves multiple files and bundles and attaches them to the result.
        # artifact_hash = self.add_artifact('MyArtifact', {
        # 'hello.txt': 'Hello world!',
        # 'dir/hello2.txt': 'Hello from folder!'
        # })

        # logger.info('The artifact is stored under hash: {0}'.format(artifact_hash))

        # Saves a single text file and attaches it to the result.
        # file_hash = self.add_file('myFile.txt', 'Hello again!')
        # logger.info('The file is stored under hash: {0}'.format(file_hash))

        # Create artifact file
        #artifact_file = os.path.join(self.working_directory, "generated_script.py")

        #with open(artifact_file, 'w') as f:
            #f.write(output_content)

        # Add file as downloadable artifact
        #self.add_artifact(artifact_file, "generated_script.py")

        #self.result_set_success(True)
        #return self.result

        # artifact = {}
        # artifact['domainSM.py'] = domainCode
        # artifact[model_name + '.py'] = model_code
        # self.add_artifact('SmToPy_' + model_name, artifact)
