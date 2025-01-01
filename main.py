from instructions import mem_instructions, non_mem_instructions, pseudo_instructions

file_object = open("output", "w")


def convert_hexa_to_dec(hexa_num: str):
    return int(hexa_num, 16)

def first_pass(cleaned_source_code: list[str]):
    symbol_table = {}

    location_counter = 0

    if cleaned_source_code[0].startswith("ORG"):
        location_counter = int(cleaned_source_code[0].strip()[3:])

    for idx, line in enumerate(cleaned_source_code):
        line = line.split(",")
        if len(line) > 1:
            symbol_table[line[0]] = location_counter
        location_counter += 1

        cleaned_source_code[idx] = line[-1].strip()

    return symbol_table


def second_pass(cleaned_source_code, symbol_table):
    for idx, line in enumerate(cleaned_source_code):
        column_count = len(line.split())

        if column_count == 1:
            instruction = line
            if instruction not in non_mem_instructions:
                print(f"Instruction not found on line: {idx + 1}")
                return

            file_object.write(f"{bin(idx)[2:].zfill(16)}  {bin(non_mem_instructions[instruction])[2:].zfill(16)}\n")

        if column_count == 2 or column_count == 3:
            indirect_addressing_mode = None

            if column_count == 2:
                instruction, address = line.split()
                if instruction in pseudo_instructions:
                    if instruction == "END":
                        return
                    elif instruction == "DEC":
                        file_object.write(f"{bin(idx)[2:].zfill(16)}  {int(address) & 0xFFFF:016b}\n")

                    elif instruction == "HEX":
                        file_object.write(f"{bin(idx)[2:].zfill(16)}  {bin(int(address, 16))[2:].zfill(16)}\n")

                    continue

            else:
                instruction, address, indirect_addressing_mode = line.split()
                if indirect_addressing_mode != "I":
                    print(f"Invalid indirect addressing instruction: {indirect_addressing_mode}")

            if instruction not in mem_instructions:
                print(f"Instruction not found on line: {idx + 1}")
                return

            if address in symbol_table:
                address = symbol_table[address]

            else:
                try:
                    address = convert_hexa_to_dec(address)
                except:
                    print(f"Address undefined on line: {idx + 1}")
                    return

            if int(address) > (2 ** 12 - 1):
                print(f"Address {address} is an invalid address")
                return

            if indirect_addressing_mode is not None:
                instruction = mem_instructions[instruction] + 0x8000
            else:
                instruction = mem_instructions[instruction]

            file_object.write(f"{bin(idx)[2:].zfill(16)}  {bin(instruction | int(address))[2:].zfill(16)}\n")


if __name__ == "__main__":
    with open("source.asm", "r") as f:
        lines = f.readlines()

        source_code = [line.rstrip().split("/")[0] for line in lines]
        generated_symbol_table = first_pass(source_code)
        second_pass(source_code, generated_symbol_table)
