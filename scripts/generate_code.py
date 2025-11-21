import yaml
import os
from pathlib import Path
from typing import Dict, Any, List

# Define base paths
ROOT_DIR = Path(__file__).parent.parent
DSL_DIR = ROOT_DIR / "dsl"
ENTITIES_DIR = DSL_DIR / "entities"
MODELS_OUTPUT_DIR = ROOT_DIR / "src" / "caramello" / "models"
API_OUTPUT_DIR = ROOT_DIR / "src" / "caramello" / "api" / "generated"

def load_yaml(file_path: Path) -> Any:
    """Loads a YAML file safely."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {file_path}: {e}")
        return None

def map_type_to_python(dsl_type: str) -> str:
    """Maps DSL types to Python/SQLModel types."""
    dsl_type_lower = dsl_type.lower()
    
    if dsl_type.startswith("List["):
        inner = dsl_type[5:-1]
        # We keep the inner type as is for the string forward ref
        return f"List['{inner}']"

    type_map = {
        "uuid": "UUID",
        "string": "str",
        "str": "str",
        "text": "str",
        "integer": "int",
        "int": "int",
        "float": "float",
        "boolean": "bool",
        "bool": "bool",
        "datetime": "datetime",
        "emailstr": "EmailStr",
    }
    
    # If not in map, assume it's an entity name and return it as a string forward ref
    # unless we handle imports dynamically. For now, let's return it as a string ref if it looks like a class name.
    mapped = type_map.get(dsl_type_lower)
    if mapped:
        return mapped
    
    # Assume it's an entity class name
    return f"'{dsl_type}'"

def generate_model_content(entity_data: Dict[str, Any]) -> str:
    """Generates the Python code for a SQLModel class."""
    entity_name = entity_data['name']
    table_name = entity_data.get('table_name', entity_name.lower() + 's')
    description = entity_data.get('description', '')
    
    # Collect imports needed for link_models
    extra_imports = []
    
    fields_code = []
    for field in entity_data.get('fields', []):
        fname = field['name']
        ftype = map_type_to_python(field['type'])
        fdesc = field.get('description', '')
        
        # Build Field() arguments
        field_args = []
        if field.get('primary_key'):
            field_args.append("primary_key=True")
        if field.get('unique'):
            field_args.append("unique=True")
        
        # Nullable handling
        is_nullable = field.get('nullable', True)
        if field.get('primary_key'):
            is_nullable = False # PKs are never nullable
            
        if not is_nullable:
             field_args.append("nullable=False")
        else:
             # If nullable, wrap type in Optional and set default to None
             # Check if ftype is already a string ref like "'User'"
             is_string_ref = ftype.startswith("'") and ftype.endswith("'")
             clean_type = ftype[1:-1] if is_string_ref else ftype
             
             if not clean_type.startswith("Optional"):
                 ftype = f"Optional[{ftype}]"
                 field_args.append("default=None")
        
        if field.get('default_factory'):
            if field['default_factory'] == 'uuid4':
                field_args.append("default_factory=uuid4")
            elif field['default_factory'] == 'now_utc':
                field_args.append("default_factory=datetime.utcnow")
        
        if field.get('max_length'):
            field_args.append(f"max_length={field['max_length']}")
            
        if field.get('foreign_key'):
            field_args.append(f"foreign_key='{field['foreign_key']}'")

        field_str = f"    {fname}: {ftype} = Field({', '.join(field_args)})"
        if fdesc:
            field_str += f"  # {fdesc}"
        fields_code.append(field_str)

    # Relationships
    for rel in entity_data.get('relationships', []):
        rname = rel['name']
        rtype = map_type_to_python(rel['type'])
        rargs = []
        if rel.get('back_populates'):
            rargs.append(f"back_populates='{rel['back_populates']}'")
        if rel.get('link_model'):
            link_model_name = rel['link_model']
            rargs.append(f"link_model={link_model_name}")
            extra_imports.append(f"from caramello.models.{link_model_name.lower()} import {link_model_name}")
        
        rel_str = f"    {rname}: {rtype} = Relationship({', '.join(rargs)})"
        fields_code.append(rel_str)

    imports_section = ""
    if extra_imports:
        imports_section = "\n".join(set(extra_imports)) + "\n\n"

    return f"""{imports_section}
class {entity_name}(SQLModel, table=True):
    \"\"\"{description}\"\"\"
    __tablename__ = "{table_name}"

{chr(10).join(fields_code)}
"""

def generate_router_content(entity_data: Dict[str, Any]) -> str:
    """Generates a FastAPI router with CRUD for the entity."""
    entity_name = entity_data['name']
    var_name = entity_name.lower()
    table_name = entity_data.get('table_name', var_name + 's')
    
    # Detect Primary Key type
    pk_type = "int" # default
    pk_field = "id"
    for field in entity_data.get('fields', []):
        if field.get('primary_key'):
            pk_type = map_type_to_python(field['type'])
            pk_field = field['name']
            break
            
    # If PK is Optional[int], we want just int for the argument
    if pk_type.startswith("Optional["):
        pk_type = pk_type[9:-1]
    
    return f"""from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from caramello.database.session import get_session
from caramello.models.{var_name} import {entity_name}

router = APIRouter(prefix="/{table_name}", tags=["{entity_name}"])

@router.post("/", response_model={entity_name})
def create_{var_name}({var_name}: {entity_name}, session: Session = Depends(get_session)):
    session.add({var_name})
    session.commit()
    session.refresh({var_name})
    return {var_name}

@router.get("/", response_model=List[{entity_name}])
def read_{var_name}s(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return session.exec(select({entity_name}).offset(offset).limit(limit)).all()

@router.get("/{{{pk_field}}}", response_model={entity_name})
def read_{var_name}({pk_field}: {pk_type}, session: Session = Depends(get_session)):
    {var_name} = session.get({entity_name}, {pk_field})
    if not {var_name}:
        raise HTTPException(status_code=404, detail="{entity_name} not found")
    return {var_name}
"""

def main():
    print("Starting Code Generation...")
    
    # Ensure output directories exist
    MODELS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    API_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    (MODELS_OUTPUT_DIR / "__init__.py").touch()
    (API_OUTPUT_DIR / "__init__.py").touch()

    manifest_path = DSL_DIR / "manifest.yaml"
    manifest = load_yaml(manifest_path)
    
    if not manifest:
        return

    entity_files = manifest.get('x-caramello-entities', [])
    
    for entity_file in entity_files:
        entity_path = ENTITIES_DIR / entity_file
        print(f"Processing {entity_path}...")
        entity_data = load_yaml(entity_path)
        if not entity_data:
            continue
            
        entity_name = entity_data['name']
        file_name = entity_name.lower() + ".py"
        
        # Generate Model
        model_code = "from typing import Optional, List\nfrom uuid import UUID, uuid4\nfrom datetime import datetime\nfrom sqlmodel import SQLModel, Field, Relationship\nfrom pydantic import EmailStr\n\n"
        # We might need forward references for relationships, so we might need to import other models or use strings.
        # For now, let's assume string forward refs work in SQLModel (they do).
        
        model_code += generate_model_content(entity_data)
        
        with open(MODELS_OUTPUT_DIR / file_name, 'w') as f:
            f.write(model_code)
            
        # Generate Router
        router_code = generate_router_content(entity_data)
        with open(API_OUTPUT_DIR / f"{entity_name.lower()}_router.py", 'w') as f:
            f.write(router_code)
            
    print("Generation Complete.")

if __name__ == "__main__":
    main()
