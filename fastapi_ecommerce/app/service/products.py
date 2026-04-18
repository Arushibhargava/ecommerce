import json
from pathlib import Path
from typing import List,Dict
DATA_FILE=Path(__file__).parent.parent /"data"/ "products.json"

def load_products()->List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,"r",encoding="utf-8") as file:
        return json.load(file)
def get_all_products()->List[Dict]:
    return load_products()
    
def save_products(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4,ensure_ascii=False)
        
def add_product(product: Dict) -> Dict:
    products=get_all_products()

    # Check if SKU already exists
    for p in products:
        if p.get("sku") == product.get("sku"):
            raise ValueError("SKU already exists")

    # Add new product
    products.append(product)

    # Save updated products
    save_products(products)
    return product

def remove_product(id: str) -> str:
    products = get_all_products()

    # Find product index
    for index, product in enumerate(products):
        if product["id"] == str(id):
            # Delete product
            deleted=products.pop(index)

            # Save updated list
            save_products(products)
            return {"message":"product dekete successfully","data":deleted}

    
def change_product(product_id: str, update_data: Dict):
    products = get_all_products()

    for index, product in enumerate(products):
            
        if product["id"]==product_id:
            # Update fields
            for key, value in update_data.items():
                if value is None:
                   continue
                # Check if key exists in product
                
                    # Optional type check (same type as existing value)
                if isinstance(value, dict) and isinstance(product.get(key),dict):
                        product[key].update(value)
                else:
                        product[key]=value

            # Save updated products
            products[index] = product
            save_products(products)
            return product

    # If product not found
    raise ValueError(
        
        detail="Product not found with given ID"
    )   