package gn.restocommerce.app
import android.app.Activity
import android.os.Bundle
import android.widget.*
import java.net.HttpURLConnection
import java.net.URL
import kotlin.concurrent.thread

class MainActivity : Activity() {
 private lateinit var status: TextView
 private lateinit var address: EditText
 private lateinit var products: TextView
 override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  val root=LinearLayout(this).apply { orientation=LinearLayout.VERTICAL; setPadding(28,36,28,24) }
  root.addView(TextView(this).apply { text="RESTO-COMMERCE"; textSize=26f; setTextColor(0xFF173653.toInt()) })
  status=TextView(this).apply { text="Serveur non vérifié"; textSize=16f }; root.addView(status)
  address=EditText(this).apply { setSingleLine(true); hint="http://192.168.1.10:8000"; setText("http://10.0.2.2:8000") }; root.addView(address)
  root.addView(Button(this).apply { text="Connecter au PC principal"; setOnClickListener { loadProducts() } })
  root.addView(TextView(this).apply { text="Catalogue produits"; textSize=20f })
  products=TextView(this).apply { text="Connecte-toi au serveur local."; textSize=15f }; root.addView(products)
  setContentView(root)
 }
 private fun loadProducts() {
  val base=address.text.toString().trim().trimEnd('/'); status.text="Connexion…"
  thread { try {
   val h=URL("$base/api/health").openConnection() as HttpURLConnection; h.connectTimeout=5000; h.readTimeout=5000
   if(h.responseCode!=200) throw Exception("Serveur indisponible"); h.disconnect()
   val c=URL("$base/api/products").openConnection() as HttpURLConnection; c.connectTimeout=5000; c.readTimeout=5000
   val body=c.inputStream.bufferedReader().use{it.readText()}; c.disconnect()
   runOnUiThread { status.text="Serveur connecté"; products.text=if(body=="[]") "Aucun produit enregistré." else body }
  } catch(e:Exception) { runOnUiThread { status.text="Connexion impossible"; products.text=e.message ?: "Erreur réseau" } } }
 }
}
