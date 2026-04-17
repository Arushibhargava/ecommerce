from fastapi import FastAPI,HTTPException,Query,Path
from service.products import get_all_products,add_product,remove_product,change_product
app=FastAPI()
from datetime import datetime
from uuid import UUID,uuid4

from schema.product import Product,ProductUpdate
@app.get("/")
def welcome():
    return "welcome"

def get_products():
    return get_all_products();
@app.get("/products")
def search_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Enter product name to search"
    ),
    sort: bool = Query(
        default=False,
        description="Sort results or not"
    ),
    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sorting order: asc or desc"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of results to return"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of results to skip"
    )
):
    # Check if name is provided
    products=get_products()
    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name query parameter is required"
        )

    # Normalize input
    search_key = name.replace(" ", "").lower()

    # Filter products
    filtered_products = []
    for product in products:
        product_name = product["name"].replace(" ", "").lower()
        if search_key in product_name:
            filtered_products.append(product)

    # If no product found
    if not filtered_products:
        raise HTTPException(
            status_code=404,
            detail="No product found matching name"
        )

    # Sorting
    if sort:
        reverse = True if order == "desc" else False
        filtered_products.sort(
            key=lambda x: x["name"].lower(),
            reverse=reverse
        )

    # Pagination
    result = filtered_products[offset: offset + limit]

    return {
        "total": len(filtered_products),
        "limit": limit,
        "offset": offset,
        "data": result
    }

@app.get("/products/{id}")
def get_product_by_id(
    id: str = Path(
        ...,
        min_length=36,
        max_length=36,
        description="Enter product ID (UUID format, 36 characters)",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
):

    products = get_all_products()

    # Search using for loop
    for product in products:
        if product.get("id") == id:
            return product

    # If not found
    raise HTTPException(
        status_code=404,
        detail="Product not found with given ID"
    )
    
@app.post("/products", status_code=202)
def create_product(product: Product):
        product_dict=product.model_dump(mode="json")
        # Add ID (UUID)
        product_dict["id"] = str(uuid4())

        # Add created_at (UTC format)
        product_dict["created_at"] = datetime.utcnow().isoformat()+"z"
        try:
       # Add product (your service function)
            add_product(product_dict)

        # Return created product
        

        except ValueError as e:
         raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        return product.model_dump(mode="json")
    
@app.delete("/products/{product_id}")
def delete_product(product_id:UUID=Path(...,description="enter the uuid")):
    try:
            data=remove_product(str(product_id))
            return data
    except Exception as e:
         raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.put("/products/{product_id}", status_code=200)
def update_product(
    product_id: UUID = Path(
        ...,
        description="Product ID in UUID format"
    ),
    payload: ProductUpdate = ...
):
    try:
        # Convert payload (Pydantic model → dict)
        update_data = payload.model_dump(mode="json",exclude_unset=True)

        # Convert UUID → str
        updated=change_product(str(product_id), update_data)

        return {
            "message": "Product updated successfully",
            "updated_fields": updated
        }

    

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    
