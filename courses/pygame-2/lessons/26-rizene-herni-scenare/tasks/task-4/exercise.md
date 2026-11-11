## Souhrn cesty a konce

Vytvořte **souhrn_stopy(stopa)** nad seznamem záznamů ze snimek. Vrátí slovník kroky (počet přechodů, tedy len-1 nejméně nula), draha (součet vzdáleností sousedních pozic), maximum_dronu (největší počet v kterémkoli snímku) a konec_v_case (cas prvního snímku s konec=True, jinak None).

Cesta z (0,0) do (3,4) a zpět měří 10, ačkoli konečná poloha je opět stejná. Math.dist nebo Vector2.length měří délku jednotlivého úseku. Pro [] jsou čítače a dráha nulové a konec_v_case=None. Stopa se nemění. Připravená prehraj je v simulace.py.
