from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict
from dbConn import conn
from datetime import datetime

app = FastAPI()

## Creates a class to use for the Production_ProductListPriceHistory table.
## for the endpoints
class Products(BaseModel):
    ProductID: int 
    Price: float
    Startdate: str
    Enddate: str
    Modifieddate: str 
## Same as mentioned above except this is for the Production_ProductListPriceHistory table.
class ProductsCost(BaseModel):
    ProductID: int 
    StandardCost: float
    Startdate: str
    Enddate: str
    Modifieddate: str 

@app.get("/")
def Reminder():
    return {"message": "Type /docs"}

## Route for returning 50 products (MAX) from the Production_ProductListPriceHistory table via a GET request (no parameters used).
@app.get("/products/ListPriceHistory")
def get_all_productlistpricehistory()->dict:
    cursor = conn.cursor()
    cursor.execute("SELECT ProductID, ListPrice, ModifiedDate FROM Production_ProductListPriceHistory LIMIT 50")
    result = cursor.fetchall()

## error handling for if the result is invalid.
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"Price List History": result}



## Post route for Production_ProductListPriceHistory
@app.post("/ProductionPriceListHistory/{ProductID}", response_model=Products)
def add_item(Product: Products)->Products:
    if Product.ProductID <= 0:
        raise HTTPException(status_code=400, detail="Amount must be more than 0.")
      
    cursor = conn.cursor()

    ## This code is used to try to format the dates correctly.
    format = "%Y-%m-%d %H:%M:%S.%f"
    DateStart= datetime.strptime(Product.Startdate, format).isoformat()
    DateEnd= datetime.strptime(Product.Enddate, format).isoformat()
    DateModified= datetime.strptime(Product.Modifieddate, format).isoformat()
   
    ## Error handling to stop it from crashing if the data isn't valid
    try:
        cursor.execute(f"INSERT INTO Production_ProductListPriceHistory VALUES('{Product.ProductID}', '{DateStart}','{DateEnd}','{Product.Price}','{DateModified}')")
        conn.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail="Input data was invalid")
    finally:
        cursor.close()
    return Product


## Delete route from  Production_ProductListPriceHistory
@app.delete("/products/{product_id}")
def delete_item(product_id: int)->object:
    query = f"""
        DELETE FROM Production_ProductListPriceHistory
        WHERE ProductID = {product_id};
    """
    cursor = conn.cursor()
    rows= cursor.execute(query)
    if rows == 0:
        raise HTTPException(status_code=400, detail="product not found.")
      
    conn.commit()
    cursor.close()
    return{"Successfully deleted the object!"}

## Put Route for Production_ProductListPriceHistory
@app.put("/products/{product_id}", response_model=Products)
def add_item(Product: Products)->Products:
    if Product.ProductID <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
     
    cursor = conn.cursor()

    ## This code is used to try to format the dates correctly.
    format = "%Y-%m-%d %H:%M:%S.%f"
    DateStart= datetime.strptime(Product.Startdate, format).isoformat()
    DateEnd= datetime.strptime(Product.Enddate, format).isoformat()
    DateModified= datetime.strptime(str(datetime.now()), format).isoformat()
   
    ## Error handling for this put.
    try:
        rows = cursor.execute(f"""
                   UPDATE Production_ProductListPriceHistory
                   SET ListPrice = "{Product.Price}", StartDate = "{DateStart}", 
                   EndDate = "{DateEnd}", ModifiedDate = "{DateModified}"
                   WHERE ProductID = {Product.ProductID}
                   """) 
        if rows == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail="Input data was invalid")
    finally:
        cursor.close()
    return Product

## Route for returning 50 products (MAX) from the Production_ProductCostHistory table via a GET request (no parameters used).
@app.get("/products/Production_ProductCostHistory/{sortValue}/{order}")
def get_all_ProductionProductCostHistory(sortValue: str, order: str)->dict:
    cursor = conn.cursor()

## Error handling for lowercase input.
    order = order.upper()
    if order not in ["ASC","DESC"]:
        order = "ASC"
 
    cursor.execute(f"""
                   SELECT ProductID, StandardCost, ModifiedDate 
                   FROM Production_ProductCostHistory
                   ORDER BY {sortValue} {order};""")
    result = cursor.fetchall()
    return {"Price Cost History": result}

## Post route for Production_ProductCostHistory
@app.post("/ProductionCost/{ProductID}", response_model=ProductsCost)
def add_item(Product: ProductsCost)->Products:
    if Product.ProductID <= 0:
        raise HTTPException(status_code=400, detail="Amount must be more than 0.")
  
    cursor = conn.cursor()

    ## This code is used to try to format the dates correctly.
    format = "%Y-%m-%d %H:%M:%S.%f"
    DateStart= datetime.strptime(Product.Startdate, format).isoformat()
    DateEnd= datetime.strptime(Product.Enddate, format).isoformat()
    DateModified= datetime.strptime(Product.Modifieddate, format).isoformat()
    
    ## Error handling.
    try:
        cursor.execute(f"INSERT INTO  Production_ProductCostHistory VALUES('{Product.ProductID}', '{DateStart}','{DateEnd}','{Product.StandardCost}','{DateModified}')")
        conn.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail="Input data was invalid")
    finally:
        cursor.close()
    return Product

## Delete route from Production_ProductCostHistory table.
@app.delete("/ProductsCost/{product_id}")
def delete_item(product_id: int)->object:
    query = f"""
        DELETE FROM Production_ProductCostHistory
        WHERE ProductID = {product_id};
    """
    cursor = conn.cursor()
    rows= cursor.execute(query)
    if rows == 0:
        raise HTTPException(status_code=400, detail="product not found.")

    conn.commit()
    cursor.close()
    return{"Successfully deleted the object!"}

## Put Route for Production_ProductCostHistory table.
@app.put("/ProductsCost/{product_id}", response_model=ProductsCost)
def add_item(Product: ProductsCost)->ProductsCost:
    if Product.ProductID <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
        return {"item"}
    cursor = conn.cursor()

    ## This code is used to try to format the dates correctly.
    format = "%Y-%m-%d %H:%M:%S.%f"
    DateStart= datetime.strptime(Product.Startdate, format).isoformat()
    DateEnd= datetime.strptime(Product.Enddate, format).isoformat()
    DateModified= datetime.strptime(str(datetime.now()), format).isoformat()
    try:
        rows = cursor.execute(f"""
                   UPDATE Production_ProductCostHistory
                   SET StartDate = "{DateStart}", EndDate = "{DateEnd}", 
                   StandardCost = {Product.StandardCost}, ModifiedDate = "{DateModified}"
                   WHERE ProductID = {Product.ProductID}
                   """)
        if rows == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        conn.commit()

    except ValidationError as err:
        raise HTTPException(status_code=400, detail="Input data was invalid")
    finally:
        cursor.close()
    return Product




