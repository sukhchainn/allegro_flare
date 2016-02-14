import os
import sys
import glob
import sqlite3

from pygccxml import utils
from pygccxml import declarations
from pygccxml import parser


# Set the path to the path of this script
os.chdir(os.path.dirname(os.path.realpath(__file__)))




# The c++ file we want to parse
# filename_file = sys.argv[1]
# filename = "../include/allegro_flare/" + filename_file

'''
create table parsed_declarations(
           id int primary key not null
           signature varchar(255),
           header_file varchar(255),
           line_number int,
           name varchar(128),
           );
'''

def parse_file(filename):
    # Find the location of the xml generator (castxml or gccxml)
    generator_path, generator_name = utils.find_xml_generator(name='castxml')

    # Configure the xml generator
    xml_generator_config = parser.xml_generator_configuration_t(
        # cflags="-std=gnu++11",
        cflags="-Wno-c++11-extensions",
        include_paths=["/Users/markoates/Repos/allegro_flare/include"],
        xml_generator_path=generator_path,
        compiler="g++",
        xml_generator=generator_name)

    # Parse the c++ file
    decls = parser.parse([filename], xml_generator_config)


    # output some GOLD!

    global_namespace = declarations.get_global_namespace(decls)

    # Search for functions which return a double. Two functions will be found
    criteria = declarations.calldef_matcher(
         #return_type="float",
         #header_file="/Users/markoates/Repos/allegro_flare/include/allegro_flare/" + filename)
         header_file=os.path.abspath(filename))
    # criteria = declarations.calldef_matcher(return_type=double_type)

    found_items = declarations.matcher.find(criteria, global_namespace)



    # create a unique list of declaration names

    unique_item_names = set();

    for item in found_items:
        print item.location.file_name + " : " + str(item.location.line)
        unique_item_names.update({item.name})



    # cross-correlate declarations in the database

    connection = sqlite3.connect('doc_entries.db')
    connection.row_factory = sqlite3.Row
    c = connection.cursor()


    found_items = 0
    unfound_items = 0

    for item in unique_item_names:
        c.execute('SELECT * FROM entries WHERE decl=?', (item, ))
        entries = c.fetchall()
        if len(entries) == 0:
            print item
            unfound_items += 1
        else:
            print item + " - FOUND"
            found_items += 1

    print "=============================="
    print str(found_items) + " items found."
    print str(unfound_items) + " matches missing."
    print "=============================="

    return




# get a file list
header_files = glob.glob("../include/allegro_flare/*/*/*.h")
header_files += glob.glob("../include/allegro_flare/*/*.h")
header_files += glob.glob("../include/allegro_flare/*.h")



for f in header_files:
    parse_file(f)
