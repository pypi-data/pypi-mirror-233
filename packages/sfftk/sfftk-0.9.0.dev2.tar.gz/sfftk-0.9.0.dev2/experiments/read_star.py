import re
import sys


def process_block(f):
    """Process a block"""
    key_value_pairs = dict()
    tables = dict()
    table_id = 0
    while True:
        row = f.readline()
        if re.match(r"^loop_", row):
            name, fields, rows = process_table(f)
            if name is None:
                name = f"table_{table_id:04d}"
                table_id += 1
            tables[name] = dict()
            tables[name]['fields'] = fields
            tables[name]['rows'] = rows
        elif re.match(r"^_.*", row):
            if re.match(r"^(_.*?)\s+(.*)\n$", row):
                k, v = process_key_value(row)
            else:  # multiline
                k = row.strip()
                v = process_multi_line_value(f)
            key_value_pairs[k] = v.strip()
        elif re.match("^[#].*", row):  # comment
            continue
        elif re.match(r"^\s$", row):  # blank line
            continue
        elif re.match(r"^$", row) or row == "":
            break
        elif re.match(r"^data_", row):
            print(f"key-value pairs: {key_value_pairs}")
            print(f"tables: {tables}")
            _key_value_pairs, _tables = process_block(f)
            print(f"_key-value pairs: {_key_value_pairs}")
            print(f"_tables: {_tables.keys()}")
            key_value_pairs.update(_key_value_pairs)
            tables.update(_tables)
    return key_value_pairs, tables


def process_table(f):
    """Process a table"""
    fields = list()
    while True:
        row = f.readline().strip()
        if re.match("^_(.*?)\s*[#].*", row):  # name with a comment; discard the comment
            fields.append(re.match("^_(.*?)\s*[#].*", row).group(1))
        elif re.match(r"^_(.*)", row):  # name without a comment
            fields.append(re.match(r"^_(.*)", row).group(1))
        else:
            break
    name = get_table_name(fields)
    # now process the table
    rows = list()
    i = 0
    while True:
        number_of_fields = len(fields)
        regex = r"^\s*(.*?)\s+" + r"\s+".join([r"(.*?)"] * (number_of_fields - 2)) + r"\s+(.*)$"
        row_regex = re.compile(regex)
        if row_regex.match(row):
            rows.append(row_regex.match(row).groups())
        else:
            break
        row = f.readline().strip()
        i += 1
    return name, fields, rows


def get_table_name(fields: list):
    """Get the table name"""
    if fields[0].startswith("rln"):
        return "_rln"
    elif fields[0].startswith("_wrp"):
        return "_wrp"
    else:
        if fields[0].split(".")[0] == fields[1].split(".")[0]:
            return fields[0].split(".")[0]


def process_key_value(row):
    """Process a key-value pair"""
    # it could be on one or more than one line
    match = re.match(r"^(.*?)\s+(.*)$", row)
    key, value = match.groups()
    return key, value


def process_multi_line_value(f):
    """Process a value that spans multiple lines"""
    row = f.readline().strip()
    value = ""
    while True:
        if re.match(r"^;([^;].+)", row):
            value += re.match(r"^;([^;].+)", row).group(1)
        elif re.match(r"^([^;].+)", row):
            value += re.match(r"^([^;].+)", row).group(1)
        elif re.match(r"^;$", row):
            break
        row = f.readline().strip()
    return value


def parse_star(star_file):
    blocks = dict()
    block_id = 0
    with open(star_file, 'r') as f:
        while True:
            row = f.readline()
            if re.match(r"^data_", row):
                name = re.match(r"^data_(?P<name>.*)", row).groupdict()['name']
                if name == "":
                    name = f"block_{block_id:04d}"
                    block_id += 1
                blocks[name] = dict()
                kv_pairs, tables = process_block(f)
                blocks[name]['key_value_pairs'] = kv_pairs
                blocks[name]['tables'] = tables
            elif row == "":
                break
    return blocks


def main():
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data3.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data4.star")
    # blocks = parse_star("/Users/pkorir/Downloads/rm.tomo/80S_Ribosomes_particlesfrom_tomomanstopgapwarpmrm_bin1.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data5.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data6.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data7.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data8.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data9.star")
    # blocks = parse_star("/Users/pkorir/PycharmProjects/sfftk/sfftk/test_data/segmentations/test_data10.star")
    blocks = parse_star("/Users/pkorir/Downloads/sta_examples/relion3/extract3d_particles.star")
    # blocks = parse_star("/Users/pkorir/Downloads/sta_examples/relion3/refine3d_particles.star")
    # blocks = parse_star("/Users/pkorir/Downloads/sta_examples/relion4/pseudosubtomo_particles.star")
    # blocks = parse_star("/Users/pkorir/Downloads/sta_examples/relion4/refine3d_run_data.star")
    for block in blocks:
        print(f"name: {block}")
        # print(f"key-value pairs: {blocks[block]['key_value_pairs']}")
        # print(f"key-value pairs: {blocks[block]['key_value_pairs']['_entity_poly.pdbx_seq_one_letter_code']}")
        # print(f"tables: {blocks[block]['tables']['_rln']['rows'][:10]}")
        # print(f"tables: {blocks[block]['tables']}")
        for table in blocks[block]['tables']:
            print(f"table: {table}")
            print(f"fields: {blocks[block]['tables'][table]['fields']}")
            print(
                f"data: {len(blocks[block]['tables'][table]['rows'])} x {len(blocks[block]['tables'][table]['fields'])}")
            # print(blocks[block]['tables'][table]['rows'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
