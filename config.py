from configparser import ConfigParser
import os

# def config(filename="database.ini", section="postgresql@14"):
#     # Check if the file exists
#     if not os.path.exists(filename):
#         raise Exception(f'The file {filename} does not exist.')
    
#     # Create a parser
#     parser = ConfigParser()
    
#     # Read config file
#     parser.read(filename)

#     # Initialize an empty dictionary
#     db = {}
    
#     # Check if the section exists
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception(
#             f'Section {section} is not found in the {filename} file.')
    
#     return db

# # Uncomment the following code to test the config function
# # try:
# #     config()
# # except Exception as e:
# #     print(e)



def config(filename="database.ini", section="postgresql@14"):
    """Read database configuration from file"""
    # Check if the file exists
    if not os.path.exists(filename):
        raise Exception(f'The file {filename} does not exist.')
    
    # Create a parser
    parser = ConfigParser()
    
    # Read config file
    parser.read(filename)

    # Initialize an empty dictionary
    db = {}
    
    # Check if the section exists
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} is not found in the {filename} file.')
    
    return db