
# Assembler for the Basic Computer

This program implements a basic assembler that takes an assembly source file (`source.asm`) as input, processes it, and generates machine code in an output file named `output`. The assembler uses two passes: the **first pass** to construct a symbol table and the **second pass** to generate binary machine code. 

## Modules and Constants

- **`MEM_INSTRUCTIONS`**: A dictionary containing memory-reference instructions and their corresponding opcode values.
- **`NON_MEM_INSTRUCTIONS`**: A dictionary containing non-memory-reference instructions and their corresponding opcode values.
- **`PSEUDO_INSTRUCTIONS`**: A set of pseudo-instructions like `ORG`, `DEC`, and `HEX` that allow memory initialization and organization.

---

## Function Definitions

### `convert_hexa_to_dec(hexa_num: str)`
**Purpose**: Converts a hexadecimal string to a decimal integer.
- **Input**: A hexadecimal number as a string (e.g., `"0x1A"`).
- **Output**: The equivalent decimal integer.
- **Usage**: Used in the second pass to interpret hexadecimal addresses in the source code.

---

### `first_pass(cleaned_source_code: list[str])`
**Purpose**: Parses the assembly source code to construct a **symbol table** and prepares the code for the second pass.
- **Input**: 
  - `cleaned_source_code`: A list of strings, each representing a line of the cleaned source code.
- **Key Operations**:
  - **Location Counter (`location_counter`)**:
    - Initialized to 0 or the value specified by the `ORG` directive.
  - **Symbol Table**:
    - Stores labels (symbols) and their corresponding memory addresses.
    - A line with a label (e.g., `LABEL, INSTRUCTION`) adds the label to the symbol table.
  - Updates the source code to remove labels, keeping only instructions and operands for the second pass.
- **Output**:
  - A symbol table mapping labels to memory addresses.
  - A modified version of the source code with labels removed.

---

### `second_pass(cleaned_source_code, symbol_table)`
**Purpose**: Translates the assembly code into binary machine instructions and writes it to the output file.
- **Input**:
  - `cleaned_source_code`: A list of strings representing cleaned assembly instructions.
  - `symbol_table`: A dictionary mapping labels to memory addresses.
- **Key Operations**:
  - Processes each line of the source code and determines the appropriate binary machine code based on the type of instruction:
    1. **Non-Memory Reference Instructions**:
       - If the instruction is found in `NON_MEM_INSTRUCTIONS`, its binary opcode is written directly.
       - E.g., `CLA`, `CMA`.
    2. **Pseudo-Instructions**:
       - `ORG`: Sets the starting address for the program.
       - `DEC`: Converts a decimal value to binary.
       - `HEX`: Converts a hexadecimal value to binary.
    3. **Memory Reference Instructions**:
       - Uses the `symbol_table` to resolve label addresses.
       - Handles **indirect addressing** (indicated by the `I` suffix).
  - **Error Checking**:
    - Validates that addresses and instructions exist and fit within the word size (12 bits for addresses, 16 bits for instructions).
    - Ensures proper formatting of instructions and operands.
  - **File Output**:
    - Writes the binary instruction in the format: `<Address> <Instruction>`.

---

## Main Code Execution

### File Reading
- Opens the `source.asm` file and reads its content line by line.
- Strips comments (anything following a `/`) and empty spaces from each line.

### First Pass
- Calls the `first_pass` function to construct the symbol table and clean the source code.
- **Output**:
  - A symbol table mapping labels to addresses.
  - A list of cleaned instructions ready for the second pass.

### Second Pass
- Calls the `second_pass` function to generate the machine code using the symbol table and cleaned instructions.
- The way it works is by treating the cleaned source code as matrix with one row and multiple columns, 
where if it has only one column then it must be a non memory reference instruction or END, if it has two or three columns,
it's then either a memory reference instruction or a pseudo instruction other than END as both require additional address information.
- Writes the final machine code to `output`.

---

## Error Handling
The assembler includes robust error checks for:
1. **Instruction Validation**:
   - Checks if an instruction exists in the `MEM_INSTRUCTIONS`, `NON_MEM_INSTRUCTIONS`, or `PSEUDO_INSTRUCTIONS` dictionaries.
2. **Address Range**:
   - Ensures that addresses do not exceed the valid word size (12 bits).
3. **Indirect Addressing**:
   - Verifies the correctness of indirect addressing syntax (`I`).
4. **Undefined Symbols**:
   - Checks if an address or label is undefined or incorrectly formatted.

---

## File Output
- **Format**: Each line in the `output` file contains the memory address and its corresponding binary instruction.
  ```
  <Address in Binary>  <Instruction in Binary>
  ```
- Example Output:
  ```
  0000000000000000  0001000000000001
  0000000000000001  0001010000000010
  ```

---

## Code Flow

1. **Input Assembly File**:
   - `source.asm` containing assembly code.
2. **First Pass**:
   - Constructs the symbol table.
   - Prepares the cleaned source code.
3. **Second Pass**:
   - Generates binary machine code using the symbol table.
   - Writes machine code to `output`.

---

## Example Assembly Code

```asm
ORG 100
HLT /Halt computer 
A, DEC 83 /Decimal operand
B, DEC -23 /Decimal operand 
END
```

### Symbol Table (First Pass):
```
A -> 100
```

### Output File:
```
0000000000000000  0001000000001101
0000000000000001  0001010000010000
0000000000000010  1111111111110001
```

---
