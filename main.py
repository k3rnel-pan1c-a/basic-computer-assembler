from instructions import MEM_INSTRUCTIONS, NON_MEM_INSTRUCTIONS, PSEUDO_INSTRUCTIONS

file_object = open("output", "w")


def convert_hexa_to_dec(hexa_num: str):
    return int(hexa_num, 16)


def first_pass(cleaned_source_code: list[str]):
    symbol_table = {}

    location_counter = 0

    if cleaned_source_code[0].startswith("ORG"):
        program_origin = int(cleaned_source_code[0].strip()[3:])
        location_counter = program_origin

    for idx, line in enumerate(cleaned_source_code):
        line = line.split(",")
        if len(line) > 1:
            symbol_table[line[0]] = location_counter
        location_counter += 1

        cleaned_source_code[idx] = line[-1].strip()

    return symbol_table, program_origin


def second_pass(cleaned_source_code, symbol_table, program_origin):
    for idx, line in enumerate(cleaned_source_code):
        column_count = len(line.split())

        if column_count == 1:
            instruction = line
            if instruction == "END":
                return

            elif instruction not in NON_MEM_INSTRUCTIONS:
                print(f"Instruction not found on line: {idx + 1}")
                return

            file_object.write(f"{bin(idx + program_origin)[2:].zfill(16)}  {bin(NON_MEM_INSTRUCTIONS[instruction])[2:].zfill(16)}\n")

        if column_count == 2 or column_count == 3:
            indirect_addressing_mode = None

            if column_count == 2:
                instruction, address = line.split()
                if instruction in PSEUDO_INSTRUCTIONS:
                    if abs(int(address)) > (2 ** 11 - 1):
                        print(f"Address exceeds word size on line: {idx + 1}")
                        return
                    if instruction == "DEC":
                        file_object.write(f"{bin(idx + program_origin)[2:].zfill(16)}  {int(address) & 0xFFFF:016b}\n")

                    elif instruction == "HEX":
                        file_object.write(f"{bin(idx + program_origin)[2:].zfill(16)}  {bin(int(address, 16))[2:].zfill(16)}\n")

                    continue

            else:
                instruction, address, indirect_addressing_mode = line.split()
                if indirect_addressing_mode != "I":
                    print(f"Invalid indirect addressing instruction: {indirect_addressing_mode}")

            if instruction not in MEM_INSTRUCTIONS:
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
                instruction = MEM_INSTRUCTIONS[instruction] + 0x8000
            else:
                instruction = MEM_INSTRUCTIONS[instruction]

            file_object.write(f"{bin(idx + program_origin)[2:].zfill(16)}  {bin(instruction | int(address))[2:].zfill(16)}\n")

    file_object.close()


if __name__ == "__main__":
    with open("source.asm", "r") as f:
        lines = f.readlines()

        source_code = [line.rstrip().split("/")[0] for line in lines]
        generated_symbol_table, program_origin = first_pass(source_code)
        print(source_code)
        second_pass(source_code, generated_symbol_table, program_origin)
