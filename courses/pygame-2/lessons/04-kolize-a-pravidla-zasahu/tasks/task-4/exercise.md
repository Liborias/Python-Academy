### Dvě skupiny proti sobě

`dvojice_zasahu(strely, nepratele)` vrátí dict: skutečná zasažená střela → seznam všech skutečných nepřátel, které obdélníkem zasáhla. Střely bez zásahu do slovníku nepatří. Pořadí klíčů/seznamů není předepsané, každá dvojice je jen jednou. Obě skupiny a jejich objekty zachovejte. Groupcollide(..., False, False) má dva přepínače kill, jeden pro každou skupinu.
