from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import initialize, connect, transaction
from .schemas import ProductCreate, SaleCreate
from datetime import datetime
import uuid

app = FastAPI(title="RESTO-COMMERCE API", version="0.1.0")
# En production, remplacer "*" par les origines exactes des interfaces.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["GET","POST"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    initialize()

@app.get("/api/health")
def health():
    return {"status":"ok","application":"RESTO-COMMERCE","database":"SQLite"}

@app.get("/api/products")
def products():
    db=connect()
    try:
        return [dict(r) for r in db.execute(
            "SELECT id,sku,name,category,unit,purchase_price,sale_price,stock FROM products WHERE active=1 ORDER BY name"
        ).fetchall()]
    finally: db.close()

@app.post("/api/products", status_code=201)
def add_product(p: ProductCreate):
    try:
        with transaction() as db:
            cur=db.execute("""INSERT INTO products
              (sku,name,category,unit,purchase_price,sale_price,stock)
              VALUES (?,?,?,?,?,?,?)""",
              (p.sku,p.name,p.category,p.unit,p.purchase_price,p.sale_price,p.stock))
            pid=cur.lastrowid
            if p.stock:
                db.execute("INSERT INTO stock_movements(product_id,movement_type,quantity,note) VALUES (?,'in',?,'Stock initial')",(pid,p.stock))
            return {"id":pid,"message":"Produit créé"}
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(409,"Cette référence produit existe déjà")
        raise

@app.post("/api/sales", status_code=201)
def add_sale(p: SaleCreate):
    with transaction() as db:
        subtotal=0
        lines=[]
        for item in p.items:
            product=db.execute("SELECT id,name,sale_price,stock FROM products WHERE id=? AND active=1",(item.product_id,)).fetchone()
            if product is None: raise HTTPException(404,f"Produit {item.product_id} introuvable")
            if product["stock"] < item.quantity: raise HTTPException(409,f"Stock insuffisant : {product['name']}")
            amount=int(round(product["sale_price"]*item.quantity))
            subtotal+=amount
            lines.append((product,item.quantity,amount))
        if p.discount>subtotal: raise HTTPException(400,"Remise supérieure au total")
        total=subtotal-p.discount
        number="RC-"+datetime.now().strftime("%Y%m%d-%H%M%S")+"-"+uuid.uuid4().hex[:5].upper()
        cur=db.execute("""INSERT INTO sales(sale_number,channel,subtotal,discount,total,payment_method)
          VALUES (?,?,?,?,?,?)""",(number,p.channel,subtotal,p.discount,total,p.payment_method))
        sale_id=cur.lastrowid
        for product,qty,amount in lines:
            db.execute("""INSERT INTO sale_items(sale_id,product_id,product_name,quantity,unit_price,line_total)
              VALUES (?,?,?,?,?,?)""",(sale_id,product["id"],product["name"],qty,product["sale_price"],amount))
            db.execute("UPDATE products SET stock=stock-? WHERE id=?",(qty,product["id"]))
            db.execute("INSERT INTO stock_movements(product_id,movement_type,quantity,note) VALUES (?,'sale',?,?)",(product["id"],qty,number))
        return {"id":sale_id,"sale_number":number,"channel":p.channel,"subtotal":subtotal,
                "discount":p.discount,"total":total,"currency":"GNF","status":"paid"}

@app.get("/api/sales")
def sales(limit:int=100):
    limit=max(1,min(limit,500))
    db=connect()
    try:
        return [dict(r) for r in db.execute("""SELECT id,sale_number,channel,subtotal,discount,total,
          payment_method,status,created_at FROM sales ORDER BY id DESC LIMIT ?""",(limit,)).fetchall()]
    finally: db.close()
