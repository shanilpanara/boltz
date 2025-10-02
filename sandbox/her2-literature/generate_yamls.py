from pathlib import Path



TEMPLATE = """
version: 1  # Optional, defaults to 1
sequences:
  - protein:
      id: A
      sequence: {target_seq}
      msa: empty
  - protein:
      id: B
      sequence: {binder_seq}
      msa: empty
templates:
    - pdb: /home/shanil/programs/boltz/sandbox/her2-literature/templates/P04626.pdb
constraints:
  - pocket:
      binder: B
      contacts: [{contacts}]
      max_distance: {max_distance}
"""


def generate_yamls(
    output_file: Path,
    target_seq: str,
    binder_seq: str,
    max_distance: float,
    contact_start: int,
    contact_end: int,
):
    contacts_str = ",".join([f"[A, {i}]" for i in range(contact_start, contact_end + 1)])

    data = TEMPLATE.format(
        target_seq=target_seq,
        binder_seq=binder_seq,
        contacts=contacts_str,
        max_distance=max_distance,
    )
    with open(output_file, "w") as f:
        f.write(data)
    print(f"Generated {output_file}")



if __name__ == "__main__":
    YAML_DIR = Path(".") / "yamls"
    YAML_DIR.mkdir(parents=True, exist_ok=True)

    FILE_DIR = Path(__file__).parent
    TEMPLATE_PATH = FILE_DIR / "templates" / "P04626.pdb"
    TARGET_FASTA_PATH = FILE_DIR / "templates" / "sequence.fasta"

    MAX_DISTANCE = 6.0

    # Define HER2 sequence
    with open(TARGET_FASTA_PATH, "r") as f:
        FULL_TARGET_SEQ = f.read().splitlines()[1].strip()

    domain_ranges = [
        ("D1", 39, 50),
        ("D1", 43, 50),
        ("D1", 65, 78),
        ("D1", 90, 100),
        ("D1", 126, 136),
        ("D1", 136, 146),
        ("D1", 188, 204),
        ("D1", 208, 219),
        ("D3", 341, 368),
        ("D3", 351, 357),
        ("D3", 384, 394),
        ("D3", 384, 402),
        ("D3", 394, 402),
        ("D3", 419, 427),
        ("D3", 476, 520),
        ("D3", 476, 497),
        ("D3", 500, 520),

    ]

    domain_cuts = {
        "D1": [23, 219],
        "D3": [310, 540]
    }

    binders = {
        "P023": "KEFPYLGWWNPNEYRYK",
        "P002": "KELTVSPWYK",
        "P003": "EKAAYSLGYYNPTK",
        "P001": "CKEQDVNTAVAWK",
    }

    for domain_name, pocket_start, pocket_end in domain_ranges:
        start, end = domain_cuts[domain_name]
        target_seq = FULL_TARGET_SEQ[start-1:end-1] # residue indexes are 0-indexed in the string

        for binder_name, binder_seq in binders.items():

            output_name = f"{binder_name}_{domain_name}_{pocket_start}-{pocket_end}.yaml"
            generate_yamls(
                output_file=YAML_DIR / output_name,
                target_seq=target_seq,
                binder_seq=binder_seq,
                max_distance=MAX_DISTANCE,
                contact_start=pocket_start,
                contact_end=pocket_end,
            )