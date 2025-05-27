# File Database Construction

This directory contains scripts to compute graph IDs for crystal structures and construct a file-based database.

## Workflow

1. **Compute Graph IDs**: Use `compute.py` to compute graph IDs for CIF files
2. **Assimilate Results**: Use `assimilate.py` to organize the results into a file database

## Usage

### Step 1: Compute Graph IDs

Run the `compute.py` script to compute graph IDs for all CIF files in a directory:

```bash
python compute.py --dir /path/to/cif/files
```

This will generate a `.json` file next to each `.cif` file containing the graph IDs.

### Step 2: Assimilate Results

Run the `assimilate.py` script to organize the results into a file database:

```bash
python assimilate.py --json-dir /path/to/json/files --output-dir /path/to/output/database
```

## Database Structure

The output database follows this structure:

```
output_dir/
├── {composition_hash}/
│   ├── {filehash_prefix}/
│   │   └── entries.json
│   └── ...
└── ...
```

Where:
- `{composition_hash}` is the first two characters of the SHA-256 hash of the composition
- `{filehash_prefix}` is the first two characters of the SHA-256 hash of the CIF file
- `entries.json` contains a dictionary mapping graph IDs to metadata:

```json
{
  "{graph_id}": {
    "proprietary_id": "MP-1234",
    "datasource": "mp",
    "url": "https://materialsproject.org/materials/MP-1234",
    "filehash": "abcdef1234567890..."
  },
  ...
}
```

## Supported Data Sources

The script automatically detects the data source from the file path:

- **IZA**: Detects IZA codes (e.g., `MFI.cif`) and sets the source to "iza"
- **Materials Project**: Detects MP IDs (e.g., `mp-1234`) and sets the source to "mp"
- **Other**: Sets the source to "unknown"

## Requirements

- Python 3.6+
- pymatgen
- pandas
- parsl (for compute.py)
- graph_id (for compute.py) 