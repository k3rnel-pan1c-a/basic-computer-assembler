mem_instructions = {
    "AND": 0,
    "ADD": 0x1000,
    "LDA": 0x2000,
    "STA": 0x3000,
    "BUN": 0x4000,
    "BSA": 0x5000,
    "ISZ": 0x6000,
}

non_mem_instructions = {
    "CLA": 0x7800,
    "CLE": 0x7400,
    "CMA": 0x7200,
    "CME": 0x7100,
    "CIR": 0x7080,
    "CIL": 0x7040,
    "INC": 0x7020,
    "SPA": 0x7010,
    "SNA": 0x7008,
    "SZA": 0x7004,
    "SZE": 0x7002,
    "HLT": 0x7001,
    "INP": 0x8000,
}

pseudo_instructions = ["DEC", "HEX", "ORG"]