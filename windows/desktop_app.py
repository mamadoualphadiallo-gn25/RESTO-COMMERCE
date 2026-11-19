import sys, requests
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QTableWidget,QTableWidgetItem,QMessageBox,QSpinBox,QFormLayout,QGroupBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("RESTO-COMMERCE"); self.resize(1080,700)
        self.api="http://127.0.0.1:8000"
        root=QWidget(); self.setCentralWidget(root); layout=QVBoxLayout(root)
        title=QLabel("RESTO-COMMERCE — Gestion restaurant & commerce")
        title.setStyleSheet("font-size:24px;font-weight:700;color:#173653")
        layout.addWidget(title)
        row=QHBoxLayout(); self.url=QLineEdit(self.api); row.addWidget(self.url)
        b=QPushButton("Connecter"); b.clicked.connect(self.connect_api); row.addWidget(b); layout.addLayout(row)
        box=QGroupBox("Ajouter un produit"); form=QFormLayout(box)
        self.name=QLineEdit(); self.category=QLineEdit("Général")
        self.price=QSpinBox(); self.price.setMaximum(2000000000); self.price.setSuffix(" GNF")
        self.stock=QSpinBox(); self.stock.setMaximum(1000000)
        form.addRow("Nom",self.name); form.addRow("Catégorie",self.category)
        form.addRow("Prix de vente",self.price); form.addRow("Stock",self.stock)
        add=QPushButton("Enregistrer"); add.clicked.connect(self.add_product); form.addRow(add)
        layout.addWidget(box)
        self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(["ID","Produit","Catégorie","Prix GNF","Stock"])
        self.table.horizontalHeader().setStretchLastSection(True); layout.addWidget(self.table)
        refresh=QPushButton("Actualiser"); refresh.clicked.connect(self.load_products); layout.addWidget(refresh)
        self.connect_api()
    def connect_api(self):
        self.api=self.url.text().strip().rstrip("/")
        try:
            requests.get(self.api+"/api/health",timeout=3).raise_for_status()
            self.statusBar().showMessage("API connectée"); self.load_products()
        except Exception as e: QMessageBox.warning(self,"API indisponible",str(e))
    def load_products(self):
        try:
            rows=requests.get(self.api+"/api/products",timeout=5).json(); self.table.setRowCount(len(rows))
            for i,p in enumerate(rows):
                for j,v in enumerate([p["id"],p["name"],p["category"],p["sale_price"],p["stock"]]):
                    self.table.setItem(i,j,QTableWidgetItem(str(v)))
        except Exception as e: QMessageBox.warning(self,"Erreur",str(e))
    def add_product(self):
        if not self.name.text().strip(): return
        try:
            r=requests.post(self.api+"/api/products",json={"name":self.name.text().strip(),"category":self.category.text().strip() or "Général","sale_price":self.price.value(),"stock":self.stock.value()},timeout=8)
            r.raise_for_status(); self.name.clear(); self.load_products()
        except Exception as e: QMessageBox.critical(self,"Échec",str(e))
if __name__=="__main__":
    app=QApplication(sys.argv); app.setStyle("Fusion"); w=MainWindow(); w.show(); sys.exit(app.exec())
