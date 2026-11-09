### Restart vytvoří novou skupinu

`NovaHra(tvorba)` uloží předanou funkci tvorba, nastaví skore=0 a zavolá ji právě jednou pro objekty. Funkce pokaždé vrací novou Group s novými sprity. `restart()` ji znovu právě jednou zavolá, nahradí objekty a vynuluje skore. Dřívější skupinu nevyprazdňujte ani jinak neměňte; může na ni odkazovat jiná proměnná. Předáváme funkci `tvorba`, nikoli její výsledek `tvorba()`. Hra tak nemusí znát konstrukci každé lodě.
