## Testy zásahů a pořadí konce

Napište testy **model.Kolo** a **sestav_sadu()**. Připravte řízené kontakty mimo zónu: nastavte hrac.pozice i hrac.rect.center, zastavte frontu vln přes vlny.cekaji=0 a vytvořte dva stojící model.Dron(..., 0). Jde o přípravu hraniční situace, ne o zásah do běžné hry.

Ověřte jeden ztracený život za dávku kontaktů, přednost smrtelného zásahu před sběrem ležícím ve stejném místě a zachování životů/skóre při přechodu z první vlny. Zbyva=0.01 a update((0,0),0.02) spustí další vlnu.

Kontrola zkusí dvojí odečtení, sběr po smrti a nechtěnou obnovu životů v nové vlně. Každou chybu musí testy odlišit od správného modelu.
